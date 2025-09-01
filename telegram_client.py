import asyncio
import os
from pathlib import Path
import json
import time
from logger import Logger

class TelegramClient:
    """Telegram client wrapper for file downloads."""
    
    def __init__(self, api_id, api_hash, phone):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.logger = Logger().get_logger(__name__)
        self._authenticated = False
        self._client = None
    
    async def initialize(self):
        """Initialize the Telegram client."""
        try:
            # Try to import and initialize TDLib
            try:
                from pytdlib import Client
                
                self._client = Client(
                    api_id=self.api_id,
                    api_hash=self.api_hash,
                    phone_number=self.phone,
                    database_encryption_key="",
                    files_directory="tdlib_files/"
                )
                
                await self._client.start()
                self._authenticated = True
                self.logger.info("TDLib client initialized successfully")
                return True
                
            except ImportError as ie:
                self.logger.warning(f"TDLib not available ({ie}), using fallback implementation")
                # Fallback to a mock client for development
                self._client = MockTelegramClient()
                self._authenticated = True
                self.logger.info("Using mock client for development")
                return True
            
        except Exception as e:
            self.logger.error(f"Error initializing Telegram client: {e}")
            return False
    
    async def download_file(self, file_id, download_path, progress_callback=None):
        """Download a file from Telegram."""
        try:
            if not self._authenticated:
                raise Exception("Client not authenticated")
            
            if hasattr(self._client, 'download_file'):
                return await self._client.download_file(file_id, download_path, progress_callback)
            else:
                # Fallback implementation
                return await self._mock_download(file_id, download_path, progress_callback)
            
        except Exception as e:
            self.logger.error(f"Error downloading file {file_id}: {e}")
            raise
    
    async def _mock_download(self, file_id, download_path, progress_callback):
        """Mock download for testing purposes."""
        try:
            # Create download directory if it doesn't exist
            Path(download_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Simulate file download with progress
            file_size = 10 * 1024 * 1024  # 10MB mock file
            downloaded = 0
            chunk_size = 1024 * 1024  # 1MB chunks
            
            with open(download_path, 'wb') as f:
                while downloaded < file_size:
                    # Simulate download delay
                    await asyncio.sleep(0.1)
                    
                    chunk = min(chunk_size, file_size - downloaded)
                    f.write(b'0' * chunk)  # Write dummy data
                    downloaded += chunk
                    
                    progress = (downloaded / file_size) * 100
                    if progress_callback:
                        progress_callback(downloaded, file_size, progress)
            
            self.logger.info(f"Mock download completed: {download_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in mock download: {e}")
            raise
    
    async def get_file_info(self, file_id):
        """Get file information."""
        try:
            if not self._authenticated:
                raise Exception("Client not authenticated")
            
            # Mock file info for development
            return {
                'file_id': file_id,
                'file_unique_id': f"unique_{file_id}",
                'file_size': 10 * 1024 * 1024,  # 10MB
                'file_path': f"mock_path/{file_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            raise
    
    def is_authenticated(self):
        """Check if client is authenticated."""
        return self._authenticated
    
    async def close(self):
        """Close the client connection."""
        try:
            if hasattr(self._client, 'stop'):
                await self._client.stop()
            self.logger.info("Telegram client closed")
        except Exception as e:
            self.logger.error(f"Error closing client: {e}")


class MockTelegramClient:
    """Mock Telegram client for development and testing."""
    
    def __init__(self):
        self.logger = Logger().get_logger(__name__)
    
    async def download_file(self, file_id, download_path, progress_callback=None):
        """Mock file download."""
        try:
            # Create download directory if it doesn't exist
            Path(download_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Simulate file download with progress
            file_size = 10 * 1024 * 1024  # 10MB mock file
            downloaded = 0
            chunk_size = 1024 * 1024  # 1MB chunks
            
            with open(download_path, 'wb') as f:
                while downloaded < file_size:
                    # Simulate download delay
                    await asyncio.sleep(0.1)
                    
                    chunk = min(chunk_size, file_size - downloaded)
                    f.write(b'0' * chunk)  # Write dummy data
                    downloaded += chunk
                    
                    progress = (downloaded / file_size) * 100
                    if progress_callback:
                        progress_callback(downloaded, file_size, progress)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in mock download: {e}")
            raise
