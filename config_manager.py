import configparser
import os
from logger import Logger

class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.logger = Logger().get_logger(__name__)
        self.load_config()
    
    def load_config(self):
        """Load configuration from file."""
        if not os.path.exists(self.config_file):
            self.logger.error(f"Configuration file {self.config_file} not found!")
            self.logger.info("Please copy config.ini.example to config.ini and fill in your details")
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")
        
        try:
            self.config.read(self.config_file, encoding='utf-8')
            self.logger.info(f"Configuration loaded from {self.config_file}")
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise
    
    def get_telegram_config(self):
        """Get Telegram API configuration."""
        try:
            config = {}
            
            # Check for bot token (easiest option)
            if self.config.has_option('telegram', 'bot_token'):
                config['bot_token'] = self.config.get('telegram', 'bot_token')
                config['auth_type'] = 'bot'
                return config
            
            # Check for demo mode
            if self.config.has_option('telegram', 'demo_mode'):
                if self.config.getboolean('telegram', 'demo_mode'):
                    config['auth_type'] = 'demo'
                    return config
            
            # Fall back to user authentication
            if (self.config.has_option('telegram', 'api_id') and 
                self.config.has_option('telegram', 'api_hash') and 
                self.config.has_option('telegram', 'phone')):
                
                config = {
                    'api_id': int(self.config.get('telegram', 'api_id')),
                    'api_hash': self.config.get('telegram', 'api_hash'),
                    'phone': self.config.get('telegram', 'phone'),
                    'auth_type': 'user'
                }
                return config
            
            # If nothing is configured, default to demo mode
            self.logger.warning("No authentication configured, using demo mode")
            config['auth_type'] = 'demo'
            return config
            
        except Exception as e:
            self.logger.error(f"Error reading Telegram configuration: {e}")
            # Default to demo mode on error
            return {'auth_type': 'demo'}
    
    def get_download_config(self):
        """Get download configuration."""
        try:
            return {
                'download_path': self.config.get('downloads', 'download_path', fallback='./downloads'),
                'max_concurrent_downloads': int(self.config.get('downloads', 'max_concurrent_downloads', fallback='3')),
                'chunk_size': int(self.config.get('downloads', 'chunk_size', fallback='1048576')),
                'retry_attempts': int(self.config.get('downloads', 'retry_attempts', fallback='5')),
                'retry_delay': int(self.config.get('downloads', 'retry_delay', fallback='5'))
            }
        except Exception as e:
            self.logger.error(f"Error reading download configuration: {e}")
            raise
    
    def get_logging_config(self):
        """Get logging configuration."""
        try:
            return {
                'log_level': self.config.get('logging', 'log_level', fallback='INFO'),
                'log_file': self.config.get('logging', 'log_file', fallback='telegram_downloader.log')
            }
        except Exception as e:
            self.logger.error(f"Error reading logging configuration: {e}")
            return {'log_level': 'INFO', 'log_file': 'telegram_downloader.log'}
