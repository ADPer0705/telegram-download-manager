#!/usr/bin/env python3
"""
Configuration Helper for Telegram Download Manager
This script helps users set up their configuration easily.
"""

import os
from pathlib import Path

def show_current_config():
    """Display current configuration."""
    config_path = Path("config.ini")
    if config_path.exists():
        print("=== Current Configuration ===")
        with open(config_path, 'r') as f:
            print(f.read())
    else:
        print("❌ No config.ini found. Copy from config.ini.example first.")

def create_config_from_template():
    """Create config.ini from template."""
    template_path = Path("config.ini.example")
    config_path = Path("config.ini")
    
    if not template_path.exists():
        print("❌ Template file config.ini.example not found!")
        return False
    
    if config_path.exists():
        response = input("⚠️  config.ini already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return False
    
    # Copy template to config
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    with open(config_path, 'w') as f:
        f.write(template_content)
    
    print("✅ Created config.ini from template")
    return True

def setup_bot_config():
    """Interactive bot token setup."""
    print("\n🤖 Bot Token Setup")
    print("1. Message @BotFather on Telegram")
    print("2. Use /newbot to create a new bot")
    print("3. Copy the bot token provided")
    print()
    
    bot_token = input("Enter your bot token (or press Enter to skip): ").strip()
    if not bot_token:
        return None
    
    # Read current config
    config_path = Path("config.ini")
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Update config
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if line.strip().startswith('demo_mode ='):
            new_lines.append('# demo_mode = true')
        elif line.strip().startswith('# bot_token =') or line.strip().startswith('bot_token ='):
            new_lines.append(f'bot_token = {bot_token}')
        elif line.strip().startswith('api_id ='):
            new_lines.append('# api_id = YOUR_API_ID')
        elif line.strip().startswith('api_hash ='):
            new_lines.append('# api_hash = YOUR_API_HASH')
        elif line.strip().startswith('phone ='):
            new_lines.append('# phone = YOUR_PHONE_NUMBER')
        else:
            new_lines.append(line)
    
    # Write back
    with open(config_path, 'w') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ Bot token configured!")
    return bot_token

def setup_user_api_config():
    """Interactive user API setup."""
    print("\n👤 User API Setup")
    print("1. Go to https://my.telegram.org/apps")
    print("2. Create a new application")
    print("3. Copy the api_id and api_hash")
    print()
    
    api_id = input("Enter your api_id (or press Enter to skip): ").strip()
    if not api_id:
        return None
    
    api_hash = input("Enter your api_hash: ").strip()
    phone = input("Enter your phone number (with country code, e.g., +1234567890): ").strip()
    
    if not api_hash or not phone:
        print("❌ All fields required for user API")
        return None
    
    # Read current config
    config_path = Path("config.ini")
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Update config
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if line.strip().startswith('demo_mode ='):
            new_lines.append('# demo_mode = true')
        elif line.strip().startswith('bot_token ='):
            new_lines.append('# bot_token = YOUR_BOT_TOKEN_HERE')
        elif line.strip().startswith('# api_id =') or line.strip().startswith('api_id ='):
            new_lines.append(f'api_id = {api_id}')
        elif line.strip().startswith('# api_hash =') or line.strip().startswith('api_hash ='):
            new_lines.append(f'api_hash = {api_hash}')
        elif line.strip().startswith('# phone =') or line.strip().startswith('phone ='):
            new_lines.append(f'phone = {phone}')
        else:
            new_lines.append(line)
    
    # Write back
    with open(config_path, 'w') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ User API configured!")
    return (api_id, api_hash, phone)

def enable_demo_mode():
    """Enable demo mode."""
    config_path = Path("config.ini")
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Update config
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if line.strip().startswith('# demo_mode =') or line.strip().startswith('demo_mode ='):
            new_lines.append('demo_mode = true')
        elif line.strip().startswith('bot_token ='):
            new_lines.append('# bot_token = YOUR_BOT_TOKEN_HERE')
        elif line.strip().startswith('api_id ='):
            new_lines.append('# api_id = YOUR_API_ID')
        elif line.strip().startswith('api_hash ='):
            new_lines.append('# api_hash = YOUR_API_HASH')
        elif line.strip().startswith('phone ='):
            new_lines.append('# phone = YOUR_PHONE_NUMBER')
        else:
            new_lines.append(line)
    
    # Write back
    with open(config_path, 'w') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ Demo mode enabled!")

def main():
    """Main configuration menu."""
    print("🚀 Telegram Download Manager - Configuration Helper")
    print("=" * 50)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. View current configuration")
        print("2. Create config from template")
        print("3. Setup bot token")
        print("4. Setup user API credentials")
        print("5. Enable demo mode")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            show_current_config()
        elif choice == "2":
            create_config_from_template()
        elif choice == "3":
            if not Path("config.ini").exists():
                print("❌ Please create config.ini first (option 2)")
                continue
            setup_bot_config()
        elif choice == "4":
            if not Path("config.ini").exists():
                print("❌ Please create config.ini first (option 2)")
                continue
            setup_user_api_config()
        elif choice == "5":
            if not Path("config.ini").exists():
                print("❌ Please create config.ini first (option 2)")
                continue
            enable_demo_mode()
        elif choice == "6":
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
