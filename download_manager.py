import asyncio
import threading
import queue
import time
from pathlib import Path
from datetime import datetime
from database import Database
from telegram_client import TelegramClient
from logger import Logger

class DownloadManager:
    """Manages download queue and handles concurrent downloads."""
    
    def __init__(self, config, telegram_client):
        self.config = config
        self.telegram_client = telegram_client
        self.database = Database()
        self.logger = Logger().get_logger(__name__)
        
        # Download configuration
        self.max_concurrent = config['max_concurrent_downloads']
        self.retry_attempts = config['retry_attempts']
        self.retry_delay = config['retry_delay']
        self.download_path = Path(config['download_path']).expanduser()
        
        # Queue management
        self.download_queue = queue.Queue()
        self.active_downloads = {}
        self.download_threads = []
        self.is_running = False
        self.pause_event = threading.Event()
        self.pause_event.set()  # Start unpaused
        
        # Progress callbacks
        self.progress_callbacks = {}
        self.status_callbacks = []
        
        # Speed tracking
        self.download_speeds = {}  # file_id -> current speed in bytes/sec
        self.download_start_times = {}  # file_id -> start timestamp
        self.last_progress_update = {}  # file_id -> (timestamp, bytes_downloaded)
        
        # Create download directory
        self.download_path.mkdir(parents=True, exist_ok=True)
    
    def add_download(self, file_id, file_name, chat_id=None, message_id=None, metadata=None):
        """Add a download to the queue."""
        try:
            download_file_path = self.download_path / file_name
            
            # Add to database
            download_id = self.database.add_download(
                file_id=file_id,
                file_name=file_name,
                download_path=str(download_file_path),
                chat_id=chat_id,
                message_id=message_id,
                metadata=metadata
            )
            
            # Add to queue
            download_item = {
                'id': download_id,
                'file_id': file_id,
                'file_name': file_name,
                'download_path': str(download_file_path),
                'retry_count': 0
            }
            
            self.download_queue.put(download_item)
            self.logger.info(f"Added download to queue: {file_name}")
            
            # Notify status callbacks
            self._notify_status_change("download_added", download_item)
            
            return download_id
            
        except Exception as e:
            self.logger.error(f"Error adding download: {e}")
            raise
    
    def start_downloads(self):
        """Start the download manager."""
        if self.is_running:
            self.logger.warning("Download manager is already running")
            return
        
        self.is_running = True
        self.logger.info("Starting download manager")
        
        # Load pending downloads from database
        self._load_pending_downloads()
        
        # Start worker threads
        for i in range(self.max_concurrent):
            thread = threading.Thread(target=self._download_worker, name=f"DownloadWorker-{i}")
            thread.daemon = True
            thread.start()
            self.download_threads.append(thread)
        
        self.logger.info(f"Started {self.max_concurrent} download worker threads")
    
    def stop_downloads(self):
        """Stop the download manager."""
        if not self.is_running:
            return
        
        self.logger.info("Stopping download manager")
        self.is_running = False
        
        # Stop all active downloads
        for file_id in list(self.active_downloads.keys()):
            self.cancel_download(file_id)
        
        # Wait for threads to finish (with timeout)
        for thread in self.download_threads:
            thread.join(timeout=5.0)
        
        self.download_threads.clear()
        self.logger.info("Download manager stopped")
    
    def pause_downloads(self):
        """Pause all downloads."""
        self.pause_event.clear()
        self.logger.info("Downloads paused")
        self._notify_status_change("downloads_paused", None)
    
    def resume_downloads(self):
        """Resume all downloads."""
        self.pause_event.set()
        self.logger.info("Downloads resumed")
        self._notify_status_change("downloads_resumed", None)
    
    def cancel_download(self, file_id):
        """Cancel a specific download."""
        try:
            # Cancel active download
            if file_id in self.active_downloads:
                download_info = self.active_downloads[file_id]
                download_info['cancelled'] = True
                self.database.update_download_status(file_id, 'cancelled')
                self._cleanup_download_tracking(file_id)
                self.logger.info(f"Cancelled active download: {file_id}")
                self._notify_status_change("download_cancelled", download_info)
            else:
                # Cancel pending download by updating status in database
                download_info = self.database.get_download(file_id)
                if download_info and download_info['status'] in ['pending', 'downloading']:
                    self.database.update_download_status(file_id, 'cancelled')
                    self._cleanup_download_tracking(file_id)
                    self.logger.info(f"Cancelled pending download: {file_id}")
                    self._notify_status_change("download_cancelled", download_info)
                
        except Exception as e:
            self.logger.error(f"Error cancelling download: {e}")
    
    def retry_download(self, file_id):
        """Retry a failed download."""
        try:
            download_info = self.database.get_download(file_id)
            if download_info and download_info['status'] == 'failed':
                # Reset status and add back to queue
                self.database.update_download_status(file_id, 'pending')
                
                download_item = {
                    'id': download_info['id'],
                    'file_id': file_id,
                    'file_name': download_info['file_name'],
                    'download_path': download_info['download_path'],
                    'retry_count': download_info['retry_count']
                }
                
                self.download_queue.put(download_item)
                self.logger.info(f"Retrying download: {download_info['file_name']}")
                
        except Exception as e:
            self.logger.error(f"Error retrying download: {e}")
    
    def get_download_status(self, file_id):
        """Get current status of a download."""
        return self.database.get_download(file_id)
    
    def get_all_downloads(self):
        """Get all downloads from database."""
        return self.database.get_all_downloads()
    
    def clear_completed_downloads(self):
        """Clear all completed downloads from database."""
        return self.database.delete_completed_downloads()
    
    def add_progress_callback(self, file_id, callback):
        """Add a progress callback for a specific download."""
        self.progress_callbacks[file_id] = callback
    
    def add_status_callback(self, callback):
        """Add a status callback for general events."""
        self.status_callbacks.append(callback)
    
    def get_download_speed(self, file_id):
        """Get current download speed for a file."""
        return self.download_speeds.get(file_id, 0)
    
    def _update_download_speed(self, file_id, downloaded_bytes):
        """Update download speed calculation."""
        current_time = time.time()
        
        if file_id not in self.download_start_times:
            self.download_start_times[file_id] = current_time
            self.last_progress_update[file_id] = (current_time, downloaded_bytes)
            self.download_speeds[file_id] = 0
            return
        
        # Calculate speed based on recent progress
        last_time, last_bytes = self.last_progress_update.get(file_id, (current_time, 0))
        time_diff = current_time - last_time
        
        if time_diff > 0.5:  # Update speed every 0.5 seconds
            bytes_diff = downloaded_bytes - last_bytes
            speed = bytes_diff / time_diff if time_diff > 0 else 0
            
            # Smooth the speed calculation (running average)
            current_speed = self.download_speeds.get(file_id, 0)
            self.download_speeds[file_id] = (current_speed * 0.7) + (speed * 0.3)
            
            self.last_progress_update[file_id] = (current_time, downloaded_bytes)
    
    def _cleanup_download_tracking(self, file_id):
        """Clean up tracking data for a completed/cancelled download."""
        self.download_speeds.pop(file_id, None)
        self.download_start_times.pop(file_id, None)
        self.last_progress_update.pop(file_id, None)
    
    def _load_pending_downloads(self):
        """Load pending downloads from database."""
        try:
            pending_downloads = self.database.get_pending_downloads()
            
            for download in pending_downloads:
                download_item = {
                    'id': download['id'],
                    'file_id': download['file_id'],
                    'file_name': download['file_name'],
                    'download_path': download['download_path'],
                    'retry_count': download['retry_count']
                }
                self.download_queue.put(download_item)
            
            self.logger.info(f"Loaded {len(pending_downloads)} pending downloads")
            
        except Exception as e:
            self.logger.error(f"Error loading pending downloads: {e}")
    
    def _download_worker(self):
        """Worker thread for processing downloads."""
        while self.is_running:
            try:
                # Wait for pause event
                self.pause_event.wait()
                
                if not self.is_running:
                    break
                
                # Get next download from queue (with timeout)
                try:
                    download_item = self.download_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                # Process the download
                self._process_download(download_item)
                self.download_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Error in download worker: {e}")
    
    def _process_download(self, download_item):
        """Process a single download."""
        file_id = download_item['file_id']
        file_name = download_item['file_name']
        download_path = download_item['download_path']
        
        try:
            # Check if already cancelled
            if download_item.get('cancelled'):
                return
            
            # Mark as active
            self.active_downloads[file_id] = download_item
            
            # Update status to downloading
            self.database.update_download_status(file_id, 'downloading')
            self._notify_status_change("download_started", download_item)
            
            # Create progress callback
            def progress_callback(downloaded_bytes, total_bytes, progress_percent):
                # Update speed tracking
                self._update_download_speed(file_id, downloaded_bytes)
                
                # Update database
                self.database.update_download_progress(file_id, progress_percent, downloaded_bytes)
                
                # Call registered progress callback if exists
                if file_id in self.progress_callbacks:
                    self.progress_callbacks[file_id](downloaded_bytes, total_bytes, progress_percent)
            
            # Start download
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            success = loop.run_until_complete(
                self.telegram_client.download_file(file_id, download_path, progress_callback)
            )
            
            loop.close()
            
            if success and not download_item.get('cancelled'):
                # Download completed successfully
                self.database.update_download_status(file_id, 'completed')
                self.logger.info(f"Download completed: {file_name}")
                self._cleanup_download_tracking(file_id)
                self._notify_status_change("download_completed", download_item)
            else:
                raise Exception("Download was cancelled or failed")
                
        except Exception as e:
            self.logger.error(f"Download failed: {file_name} - {e}")
            
            # Handle retry logic
            if download_item['retry_count'] < self.retry_attempts:
                self.database.increment_retry_count(file_id)
                download_item['retry_count'] += 1
                
                # Wait before retry
                time.sleep(self.retry_delay)
                
                # Add back to queue for retry
                self.download_queue.put(download_item)
                self.logger.info(f"Retrying download ({download_item['retry_count']}/{self.retry_attempts}): {file_name}")
            else:
                # Max retries reached
                self.database.update_download_status(file_id, 'failed', str(e))
                self._cleanup_download_tracking(file_id)
                self._notify_status_change("download_failed", download_item)
        
        finally:
            # Remove from active downloads
            if file_id in self.active_downloads:
                del self.active_downloads[file_id]
    
    def _notify_status_change(self, event_type, download_item):
        """Notify all status callbacks about an event."""
        try:
            for callback in self.status_callbacks:
                callback(event_type, download_item)
        except Exception as e:
            self.logger.error(f"Error in status callback: {e}")
