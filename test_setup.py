#!/usr/bin/env python3
"""
Simple test script to verify the Telegram Download Manager setup.
"""

import sys
import asyncio
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from logger import Logger
        print("✓ Logger imported successfully")
        
        from config_manager import ConfigManager
        print("✓ ConfigManager imported successfully")
        
        from database import Database
        print("✓ Database imported successfully")
        
        from telegram_client import TelegramClient
        print("✓ TelegramClient imported successfully")
        
        from download_manager import DownloadManager
        print("✓ DownloadManager imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("\\nTesting configuration...")
    
    try:
        from config_manager import ConfigManager
        config = ConfigManager()
        
        telegram_config = config.get_telegram_config()
        download_config = config.get_download_config()
        
        print("✓ Configuration loaded successfully")
        print(f"  Download path: {download_config['download_path']}")
        print(f"  Max concurrent downloads: {download_config['max_concurrent_downloads']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_database():
    """Test database initialization."""
    print("\\nTesting database...")
    
    try:
        from database import Database
        db = Database("test.db")
        
        # Test adding a download
        download_id = db.add_download(
            file_id="test_file_123",
            file_name="test_file.txt",
            file_size=1024
        )
        
        # Test retrieving the download
        download_info = db.get_download("test_file_123")
        
        if download_info and download_info['file_name'] == "test_file.txt":
            print("✓ Database operations working correctly")
            
            # Clean up test data
            db.delete_download("test_file_123")
            Path("test.db").unlink(missing_ok=True)
            
            return True
        else:
            print("✗ Database operations failed")
            return False
            
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

async def test_telegram_client():
    """Test Telegram client initialization."""
    print("\\nTesting Telegram client...")
    
    try:
        from telegram_client import TelegramClient
        
        client = TelegramClient(
            api_id=12345678,
            api_hash="test_hash",
            phone="+1234567890"
        )
        
        success = await client.initialize()
        
        if success and client.is_authenticated():
            print("✓ Telegram client initialized successfully (using mock)")
            await client.close()
            return True
        else:
            print("✗ Telegram client initialization failed")
            return False
            
    except Exception as e:
        print(f"✗ Telegram client error: {e}")
        return False

def main():
    """Run all tests."""
    print("Telegram Download Manager - Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_database,
        lambda: asyncio.run(test_telegram_client())
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print("\\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\\n🎉 All tests passed! The setup is working correctly.")
        print("\\nTo get started:")
        print("1. Update config.ini with your actual Telegram API credentials")
        print("2. Run: python main.py")
    else:
        print("\\n❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
