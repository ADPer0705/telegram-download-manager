import asyncio
import os
import requests
from pathlib import Path
import time
from logger import Logger

class BotTelegramClient:
    """Telegram client using Bot API for file downloads."""
    
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.logger = Logger().get_logger(__name__)
        self._authenticated = False
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    async def initialize(self):
        """Initialize the bot client."""
        try:
            # Test bot token
            response = requests.get(f"{self.base_url}/getMe")
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info['ok']:
                    self.logger.info(f"Bot authenticated: @{bot_info['result']['username']}")
                    self._authenticated = True
                    return True
                else:
                    raise Exception(f"Bot authentication failed: {bot_info.get('description', 'Unknown error')}")
            else:
                raise Exception(f"HTTP {response.status_code}: Failed to connect to Telegram API")
                
        except Exception as e:
            self.logger.error(f"Error initializing bot client: {e}")
            return False
    
    async def download_file(self, file_id, download_path, progress_callback=None):
        """Download file using Bot API."""
        try:
            if not self._authenticated:
                raise Exception("Bot not authenticated")
            
            # Get file info first
            file_response = requests.get(f"{self.base_url}/getFile", params={'file_id': file_id})
            
            if file_response.status_code != 200:
                raise Exception(f"Failed to get file info: HTTP {file_response.status_code}")
            
            file_data = file_response.json()
            if not file_data['ok']:
                raise Exception(f"Telegram API error: {file_data.get('description', 'Unknown error')}")
            
            file_path = file_data['result']['file_path']
            file_size = file_data['result'].get('file_size', 0)
            
            # Download file
            download_url = f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"
            
            # Create download directory
            Path(download_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Download with progress tracking
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            downloaded = 0
            with open(download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and file_size > 0:
                            progress = (downloaded / file_size) * 100
                            progress_callback(downloaded, file_size, progress)
                        
                        # Small delay to make download cancellable
                        await asyncio.sleep(0.001)
            
            self.logger.info(f"Bot download completed: {download_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error downloading file with bot: {e}")
            raise
    
    async def get_file_info(self, file_id):
        """Get file information using Bot API."""
        try:
            if not self._authenticated:
                raise Exception("Bot not authenticated")
            
            response = requests.get(f"{self.base_url}/getFile", params={'file_id': file_id})
            
            if response.status_code != 200:
                raise Exception(f"Failed to get file info: HTTP {response.status_code}")
            
            file_data = response.json()
            if not file_data['ok']:
                raise Exception(f"Telegram API error: {file_data.get('description', 'Unknown error')}")
            
            return {
                'file_id': file_id,
                'file_unique_id': file_data['result'].get('file_unique_id'),
                'file_size': file_data['result'].get('file_size', 0),
                'file_path': file_data['result']['file_path']
            }
            
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            raise
    
    def is_authenticated(self):
        """Check if bot is authenticated."""
        return self._authenticated
    
    async def close(self):
        """Close the bot client."""
        self.logger.info("Bot client closed")


class DemoTelegramClient:
    """Demo client that works without any credentials."""
    
    def __init__(self):
        self.logger = Logger().get_logger(__name__)
        self._authenticated = True
    
    async def initialize(self):
        """Initialize demo client."""
        self.logger.info("Demo client initialized - no authentication required")
        return True
    
    async def download_file(self, file_id, download_path, progress_callback=None):
        """Demo download that creates a sample file."""
        try:
            # Create download directory
            Path(download_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Create a sample file with some content
            file_size = 1024 * 1024  # 1MB demo file
            downloaded = 0
            chunk_size = 8192
            
            with open(download_path, 'wb') as f:
                while downloaded < file_size:
                    # Simulate download delay
                    await asyncio.sleep(0.05)
                    
                    chunk = min(chunk_size, file_size - downloaded)
                    # Write some sample content
                    content = f"Demo file content - File ID: {file_id}\n".encode() * (chunk // 50 + 1)
                    f.write(content[:chunk])
                    downloaded += chunk
                    
                    if progress_callback:
                        progress = (downloaded / file_size) * 100
                        progress_callback(downloaded, file_size, progress)
            
            self.logger.info(f"Demo download completed: {download_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in demo download: {e}")
            raise
    
    async def get_file_info(self, file_id):
        """Get demo file information."""
        return {
            'file_id': file_id,
            'file_unique_id': f"demo_{file_id}",
            'file_size': 1024 * 1024,  # 1MB
            'file_path': f"demo/{file_id}"
        }
    
    def is_authenticated(self):
        """Demo client is always authenticated."""
        return True
    
    async def close(self):
        """Close demo client."""
        self.logger.info("Demo client closed")
