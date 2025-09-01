import sqlite3
import threading
import json
from datetime import datetime
from logger import Logger

class Database:
    """Database manager for storing download information."""
    
    def __init__(self, db_path="downloads.db"):
        self.db_path = db_path
        self.logger = Logger().get_logger(__name__)
        self._lock = threading.Lock()
        self.init_database()
    
    def init_database(self):
        """Initialize database tables."""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Downloads table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS downloads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_id TEXT UNIQUE NOT NULL,
                        file_name TEXT NOT NULL,
                        file_size INTEGER,
                        download_path TEXT,
                        status TEXT DEFAULT 'pending',
                        progress REAL DEFAULT 0.0,
                        downloaded_bytes INTEGER DEFAULT 0,
                        error_message TEXT,
                        retry_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        started_at TIMESTAMP,
                        completed_at TIMESTAMP,
                        chat_id TEXT,
                        message_id INTEGER,
                        metadata TEXT
                    )
                ''')
                
                # Download sessions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS download_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ended_at TIMESTAMP
                    )
                ''')
                
                conn.commit()
                conn.close()
                self.logger.info("Database initialized successfully")
                
            except Exception as e:
                self.logger.error(f"Error initializing database: {e}")
                raise
    
    def add_download(self, file_id, file_name, file_size=None, download_path=None, 
                    chat_id=None, message_id=None, metadata=None):
        """Add a new download to the database."""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO downloads 
                    (file_id, file_name, file_size, download_path, chat_id, message_id, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (file_id, file_name, file_size, download_path, chat_id, message_id,
                      json.dumps(metadata) if metadata else None))
                
                conn.commit()
                download_id = cursor.lastrowid
                conn.close()
                
                self.logger.info(f"Added download: {file_name} (ID: {download_id})")
                return download_id
                
            except Exception as e:
                self.logger.error(f"Error adding download: {e}")
                raise
    
    def update_download_progress(self, file_id, progress, downloaded_bytes):
        """Update download progress."""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE downloads 
                    SET progress = ?, downloaded_bytes = ?
                    WHERE file_id = ?
                ''', (progress, downloaded_bytes, file_id))
                
                conn.commit()
                conn.close()
                
            except Exception as e:
                self.logger.error(f"Error updating progress: {e}")
    
    def update_download_status(self, file_id, status, error_message=None):
        """Update download status."""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                timestamp_field = None
                if status == 'downloading':
                    timestamp_field = 'started_at'
                elif status in ['completed', 'failed']:
                    timestamp_field = 'completed_at'
                
                if timestamp_field:
                    cursor.execute(f'''
                        UPDATE downloads 
                        SET status = ?, error_message = ?, {timestamp_field} = CURRENT_TIMESTAMP
                        WHERE file_id = ?
                    ''', (status, error_message, file_id))
                else:
                    cursor.execute('''
                        UPDATE downloads 
                        SET status = ?, error_message = ?
                        WHERE file_id = ?
                    ''', (status, error_message, file_id))
                
                conn.commit()
                conn.close()
                
                self.logger.info(f"Updated download status: {file_id} -> {status}")
                
            except Exception as e:
                self.logger.error(f"Error updating status: {e}")
    
    def increment_retry_count(self, file_id):
        """Increment retry count for a download."""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE downloads 
                    SET retry_count = retry_count + 1
                    WHERE file_id = ?
                ''', (file_id,))
                
                conn.commit()
                conn.close()
                
            except Exception as e:
                self.logger.error(f"Error incrementing retry count: {e}")
    
    def get_download(self, file_id):
        """Get download information by file_id."""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM downloads WHERE file_id = ?
                ''', (file_id,))
                
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, result))
                return None
                
            except Exception as e:
                self.logger.error(f"Error getting download: {e}")
                return None
    
    def get_pending_downloads(self):
        """Get all pending downloads."""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM downloads 
                    WHERE status IN ('pending', 'paused', 'failed')
                    ORDER BY created_at ASC
                ''')
                
                results = cursor.fetchall()
                conn.close()
                
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in results]
                
            except Exception as e:
                self.logger.error(f"Error getting pending downloads: {e}")
                return []
    
    def get_all_downloads(self):
        """Get all downloads."""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM downloads ORDER BY created_at DESC
                ''')
                
                results = cursor.fetchall()
                conn.close()
                
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in results]
                
            except Exception as e:
                self.logger.error(f"Error getting all downloads: {e}")
                return []
    
    def delete_download(self, file_id):
        """Delete a download from database."""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM downloads WHERE file_id = ?', (file_id,))
                
                conn.commit()
                conn.close()
                
                self.logger.info(f"Deleted download: {file_id}")
                
            except Exception as e:
                self.logger.error(f"Error deleting download: {e}")
    
    def delete_completed_downloads(self):
        """Delete all completed and cancelled downloads from database."""
        with self._lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM downloads WHERE status IN (?, ?)', ('completed', 'cancelled'))
                deleted_count = cursor.rowcount
                
                conn.commit()
                conn.close()
                
                self.logger.info(f"Deleted {deleted_count} completed/cancelled downloads")
                return deleted_count
                
            except Exception as e:
                self.logger.error(f"Error deleting completed downloads: {e}")
                return 0
