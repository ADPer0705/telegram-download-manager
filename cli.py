#!/usr/bin/env python3
"""
Utility script for managing Telegram downloads from command line.
"""

import sys
import asyncio
import argparse
from pathlib import Path
from config_manager import ConfigManager
from telegram_client import TelegramClient
from download_manager import DownloadManager
from database import Database

async def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Telegram Download Manager CLI")
    parser.add_argument("--file-id", required=True, help="Telegram file ID to download")
    parser.add_argument("--file-name", help="Custom filename for the download")
    parser.add_argument("--output-dir", help="Output directory (overrides config)")
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config_manager = ConfigManager()
        telegram_config = config_manager.get_telegram_config()
        download_config = config_manager.get_download_config()
        
        # Override output directory if specified
        if args.output_dir:
            download_config['download_path'] = args.output_dir
        
        # Initialize Telegram client
        client = TelegramClient(
            api_id=telegram_config['api_id'],
            api_hash=telegram_config['api_hash'],
            phone=telegram_config['phone']
        )
        
        print("Connecting to Telegram...")
        success = await client.initialize()
        
        if not success:
            print("Failed to connect to Telegram")
            return 1
        
        print("Connected successfully!")
        
        # Initialize download manager
        download_manager = DownloadManager(download_config, client)
        download_manager.start_downloads()
        
        # Add download
        file_name = args.file_name or f"file_{args.file_id[:10]}"
        download_id = download_manager.add_download(args.file_id, file_name)
        
        print(f"Added download: {file_name} (ID: {download_id})")
        print("Download started. Check the GUI for progress.")
        
        # Wait a bit for download to start
        await asyncio.sleep(2)
        
        # Cleanup
        download_manager.stop_downloads()
        await client.close()
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
