#!/usr/bin/env python3
"""
Setup script to help users configure the Telegram Download Manager.
"""

import os
import sys
from pathlib import Path

def create_config():
    """Create configuration file with user input."""
    print("Telegram Download Manager Setup")
    print("=" * 40)
    print()
    
    # Check if config already exists
    if Path("config.ini").exists():
        response = input("config.ini already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return False
    
    print("You'll need to get your API credentials from https://my.telegram.org/")
    print()
    
    # Get API credentials
    while True:
        try:
            api_id = input("Enter your API ID: ").strip()
            if api_id:
                int(api_id)  # Validate it's a number
                break
            else:
                print("API ID cannot be empty")
        except ValueError:
            print("API ID must be a number")
    
    api_hash = input("Enter your API Hash: ").strip()
    while not api_hash:
        api_hash = input("API Hash cannot be empty. Enter your API Hash: ").strip()
    
    phone = input("Enter your phone number (with country code, e.g., +1234567890): ").strip()
    while not phone:
        phone = input("Phone number cannot be empty. Enter your phone number: ").strip()
    
    # Get download settings
    print()
    download_path = input("Enter download directory [./downloads]: ").strip()
    if not download_path:
        download_path = "./downloads"
    
    max_downloads = input("Maximum concurrent downloads [3]: ").strip()
    if not max_downloads:
        max_downloads = "3"
    
    # Create config file
    config_content = f"""[telegram]
api_id = {api_id}
api_hash = {api_hash}
phone = {phone}

[downloads]
download_path = {download_path}
max_concurrent_downloads = {max_downloads}
chunk_size = 1048576
retry_attempts = 5
retry_delay = 5

[logging]
log_level = INFO
log_file = telegram_downloader.log"""

    with open("config.ini", "w") as f:
        f.write(config_content)
    
    print()
    print("✓ Configuration saved to config.ini")
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    print("\\nChecking dependencies...")
    
    required_packages = [
        'tkinter',
        'sqlite3',
        'asyncio',
        'threading',
        'queue',
        'pathlib'
    ]
    
    optional_packages = [
        'python-telegram-bot',
        'pytdlib'
    ]
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing_required.append(package)
            print(f"✗ {package} (required)")
    
    for package in optional_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            missing_optional.append(package)
            print(f"⚠ {package} (optional)")
    
    if missing_required:
        print(f"\\nMissing required packages: {', '.join(missing_required)}")
        print("Please install them and try again.")
        return False
    
    if missing_optional:
        print(f"\\nMissing optional packages: {', '.join(missing_optional)}")
        print("The application will work with limited functionality.")
        print("Install them with: pip install " + " ".join(missing_optional))
    
    return True

def main():
    """Main setup function."""
    print("Welcome to Telegram Download Manager Setup!")
    print()
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Create configuration
    if not create_config():
        return 1
    
    print()
    print("🎉 Setup completed successfully!")
    print()
    print("Next steps:")
    print("1. Run 'python test_setup.py' to verify everything works")
    print("2. Run 'python main.py' to start the GUI application")
    print("3. Or run 'python cli.py --help' for command-line usage")
    print()
    print("Note: For full functionality, you may need to install TDLib:")
    print("pip install python-telegram-bot pytdlib")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
