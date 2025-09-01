# Documentation

## Table of Contents

- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [FAQ](#frequently-asked-questions)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

## Configuration

### Basic Configuration

The `config.ini` file supports multiple authentication methods. Choose one:

**Method 1: Bot Token**
```ini
[telegram]
bot_token = your_bot_token_here

[downloads]
download_path = ./downloads
# ... other settings
```

**Method 2: API Credentials**
```ini
[telegram]
api_id = your_api_id
api_hash = your_api_hash  
phone = your_phone_number

[downloads]
download_path = ./downloads
# ... other settings
```

**Method 3: Demo Mode**
```ini
[telegram]
demo_mode = true

[downloads]
download_path = ./downloads
# ... other settings
```

### Configuration Options

| Section | Option | Description | Default | Type |
|---------|--------|-------------|---------|------|
| telegram | api_id | Your Telegram API ID | Required | int |
| telegram | api_hash | Your Telegram API Hash | Required | string |  
| telegram | phone | Phone number with country code | Required | string |
| downloads | download_path | Directory to save downloads | ./downloads | string |
| downloads | max_concurrent_downloads | Maximum simultaneous downloads | 3 | int |
| downloads | chunk_size | Download chunk size in bytes | 1048576 | int |
| downloads | retry_attempts | Number of retry attempts | 5 | int |
| downloads | retry_delay | Delay between retries in seconds | 5 | int |
| logging | log_level | Logging level | INFO | string |
| logging | log_file | Log file path | logs/telegram_downloader.log | string |

### Advanced Configuration

- **Chunk Size**: Larger chunks (e.g., 2MB) may improve speed but use more memory
- **Concurrent Downloads**: More concurrent downloads may saturate bandwidth
- **Retry Settings**: Adjust based on your network stability

## Usage Guide

### Starting the Application

1. Launch the GUI: `python main.py`
2. Click **"Connect"** to authenticate with Telegram
3. Enter your phone verification code when prompted

### Adding Downloads

1. Get a File ID (see [How to Get File IDs](#how-to-get-file-ids))
2. Enter the File ID in the input field
3. Optionally enter a custom filename
4. Click "Add Download" to queue the file
5. Downloads will start automatically

### Managing Downloads

- **Pause/Resume**: Control individual downloads
- **Remove**: Delete completed or failed downloads
- **Clear All**: Clear the entire download history
- **Monitor Progress**: Real-time progress bars and speed indicators

## Frequently Asked Questions

### Authentication Methods

**Q: What are the different ways to authenticate?**

A: There are 3 authentication methods:

1. **Bot Token** (Easiest):
   - Get token from @BotFather on Telegram
   - No phone verification needed
   - Works with most public files
   - Best for regular users

2. **API Credentials** (Full access):
   - Get from https://my.telegram.org/
   - Requires phone verification  
   - Access to all files you can see
   - Best for personal downloads

3. **Demo Mode** (No setup):
   - No credentials needed
   - Creates sample files for testing
   - Perfect for trying the app

### Getting Bot Token

**Q: How do I get a bot token?**

A: Follow these simple steps:
1. Open Telegram and message @BotFather
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "My Download Bot")
4. Choose a username ending in "bot" (e.g., "mydownload_bot")
5. Copy the bot token that BotFather gives you
6. Put it in config.ini: `bot_token = YOUR_TOKEN_HERE`

**Q: What can I download with a bot token?**

A: Bot tokens can download:
- Files shared in public channels
- Files shared in groups where your bot is added
- Files sent directly to your bot
- Most media files under 20MB (Bot API limit)

**Q: What are the limitations of bot tokens?**

A: Bot token limitations:
- 20MB file size limit (Bot API limitation)
- Can't access private conversations (unless bot is added)
- Can't access restricted/private channels
- Requires bot to be added to groups/channels

### Getting API Credentials

**Q: How do I get Telegram API credentials?**

A: Follow these steps:
1. Go to https://my.telegram.org/
2. Login with your phone number
3. Go to "API development tools"
4. Create a new application:
   - App title: Any name (e.g., "My Download Manager")
   - Short name: Any short identifier
   - Platform: Desktop
   - Other fields: Optional
5. Copy the api_id and api_hash to your config.ini

**Q: Are API credentials safe to use?**

A: Yes, but treat them like passwords:
- Never share them publicly
- Don't commit config.ini to version control
- Use them only in trusted applications

### Getting File IDs

**Q: What is a File ID?**

A: A File ID is a unique identifier that Telegram assigns to every file. It looks like a long string of characters.

**Q: How do I get File IDs?**

A: Several methods:

**Method 1: Telegram Bots**
- Create a simple bot
- Send files to it
- Bot shows the file ID

**Method 2: Browser Developer Tools**
- Open Telegram Web
- Find the file
- Right-click → Inspect Element
- Look for file-related data in HTML

**Method 3: Third-party Tools**
- telegram-cli
- Other Telegram API tools
- Browser extensions

**Method 4: Bot API**
```python
message.document.file_id  # Documents
message.photo[-1].file_id  # Photos
message.video.file_id     # Videos
```

### Application Usage

**Q: Can I download multiple files at once?**

A: Yes, the application supports concurrent downloads. Set `max_concurrent_downloads` in config.ini.

**Q: Can I resume interrupted downloads?**

A: Yes, the application automatically resumes interrupted downloads from where they left off.

**Q: Where are files saved?**

A: Files are saved to the directory specified in `download_path` in config.ini (default: ./downloads).

**Q: Can I change the filename?**

A: Yes, enter a custom filename when adding the download, or it will use the original filename.

### Authentication

**Q: Why do I need to enter a verification code?**

A: Telegram requires phone verification for security. This is a one-time setup per device.

**Q: How often do I need to authenticate?**

A: Usually just once. The application saves session data for future use.

**Q: Can I use a bot token instead?**

A: This version uses user authentication. Bot tokens have limited file access compared to user accounts.

## Troubleshooting

### Installation Issues

**Problem**: "Module not found" errors
**Solution**: 
```bash
pip install -r requirements.txt
```

**Problem**: Python version errors
**Solution**: Ensure you're using Python 3.8 or higher:
```bash
python --version
```

### Authentication Issues

**Problem**: Authentication failed
**Solutions**:
- Double-check api_id and api_hash in config.ini
- Ensure phone number includes country code (+1234567890)
- Verify credentials are valid at my.telegram.org

**Problem**: "Invalid phone number"
**Solution**: Use international format: +[country code][number]

### Download Issues

**Problem**: Downloads failing
**Solutions**:
- Check internet connection
- Verify file ID is correct
- Check logs in logs/telegram_downloader.log
- Increase retry_attempts in config

**Problem**: "File not found"
**Solutions**:
- Verify you have access to the file in Telegram
- Check if file was deleted by sender
- Ensure file ID format is correct

**Problem**: Slow download speeds
**Solutions**:
- Increase chunk_size in config
- Check network connection
- Try downloading at different times

### Permission Issues

**Problem**: Permission denied errors
**Solutions**:
- Ensure download directory is writable
- Check file system permissions
- Try running as administrator (Windows) or with sudo (Linux/Mac)

**Problem**: "Cannot create directory"
**Solution**: Create the download directory manually or check parent directory permissions

### Database Issues

**Problem**: Database errors
**Solutions**:
- Delete downloads.db and restart (loses history)
- Check file permissions on database file
- Ensure SQLite is properly installed

## Development

### Code Structure

```
main.py                 # GUI application entry point
├── TelegramDownloadManagerGUI class
    ├── GUI setup and event handling
    ├── Telegram client integration
    └── Download manager coordination

telegram_client.py      # Telegram API wrapper
├── TelegramClient class
    ├── Authentication handling
    ├── File download methods
    └── Error handling

download_manager.py     # Download queue management
├── DownloadManager class
    ├── Queue processing
    ├── Progress tracking
    └── Retry logic

database.py            # Data persistence
├── Database class
    ├── SQLite operations
    ├── Download history
    └── Queue state

config_manager.py      # Configuration handling
├── ConfigManager class
    ├── Config file parsing
    ├── Default values
    └── Validation

logger.py              # Logging setup
├── Logger class
    ├── File logging
    ├── Console output
    └── Log rotation
```

### Adding Features

1. **New Download Sources**: Extend TelegramClient
2. **UI Improvements**: Modify TelegramDownloadManagerGUI
3. **Database Changes**: Update Database class and migrations
4. **Configuration**: Add options to ConfigManager

### Testing

Run basic import test:
```bash
python -c "import main; print('✓ Success')"
```

### Debugging

Enable debug logging in config.ini:
```ini
[logging]
log_level = DEBUG
```

Check logs for detailed information:
```bash
tail -f logs/telegram_downloader.log
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the existing code style
4. Test thoroughly
5. Submit a pull request

## Security Considerations

- **API Credentials**: Never commit config.ini to version control
- **Session Data**: Stored locally, keep secure
- **Log Files**: May contain sensitive info, secure appropriately
- **File Permissions**: Ensure appropriate access controls

## Performance Tips

- **Concurrent Downloads**: Balance between speed and system resources
- **Chunk Size**: Larger chunks for better speed, smaller for stability
- **Network**: Stable connection improves success rate
- **Storage**: Ensure adequate disk space for downloads
