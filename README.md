# Telegram Download Manager

A robust download manager for Telegram files using TDLib with GUI interface.

## Features

- **Reliable Downloads**: Automatic retry mechanism and resume capability for interrupted downloads
- **Queue Management**: Download multiple files concurrently with proper queue handling
- **Progress Tracking**: Real-time download progress with visual feedback and speed monitoring
- **Resume Capability**: Automatically resume interrupted downloads from where they left off
- **GUI Interface**: User-friendly interface built with Tkinter
- **Database Storage**: Persistent storage of download history and queue state
- **Error Handling**: Comprehensive error handling, logging, and retry mechanisms
- **CLI Support**: Command-line interface for automated downloads

## Requirements

- Python 3.8+
- TDLib (Telegram Database Library) - optional, fallback mock client included
- See `requirements.txt` for full dependencies

## Quick Start

1. **Setup**: Run the interactive setup script
   ```bash
   python setup.py
   ```

2. **Test**: Verify everything works
   ```bash
   python test_setup.py
   ```

3. **Run**: Start the GUI application
   ```bash
   python main.py
   ```

## Manual Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy configuration template:
   ```bash
   cp config.ini.example config.ini
   ```
4. Edit `config.ini` with your Telegram API credentials
5. Run the application:
   ```bash
   python main.py
   ```

## Getting Telegram API Credentials

1. Go to https://my.telegram.org/
2. Log in with your phone number
3. Go to "API development tools"
4. Create a new application
5. Copy the `api_id` and `api_hash`

## Configuration

The `config.ini` file contains all settings:

```ini
[telegram]
api_id = your_api_id
api_hash = your_api_hash
phone = your_phone_number

[downloads]
download_path = ./downloads
max_concurrent_downloads = 3
chunk_size = 1048576
retry_attempts = 5
retry_delay = 5

[logging]
log_level = INFO
log_file = telegram_downloader.log
```

## Usage

### GUI Application

1. Start the application: `python main.py`
2. Click "Connect" to authenticate with Telegram
3. Enter file IDs and names to add downloads
4. Monitor progress in the downloads list
5. Use pause/resume for queue control

### Command Line Interface

```bash
# Download a specific file
python cli.py --file-id "your_file_id" --file-name "custom_name.ext"

# Download to specific directory
python cli.py --file-id "your_file_id" --output-dir "/path/to/downloads"
```

### How to Get File IDs

File IDs can be obtained from:
- Telegram Bot API
- TDLib client inspection
- Browser developer tools on Telegram Web
- Third-party Telegram tools

## Architecture

- `main.py`: GUI application entry point
- `telegram_client.py`: TDLib client wrapper with fallback mock
- `enhanced_client.py`: Enhanced client with better download features
- `download_manager.py`: Download queue and progress management
- `database.py`: SQLite database operations for persistence
- `config_manager.py`: Configuration file handling
- `logger.py`: Centralized logging setup
- `cli.py`: Command-line interface
- `setup.py`: Interactive setup script
- `test_setup.py`: Setup verification script

## Features in Detail

### Reliable Downloads
- Automatic retry on network failures
- Configurable retry attempts and delays
- Resume capability for interrupted downloads
- Partial file handling

### Queue Management
- Concurrent download support
- Priority-based queue processing
- Pause/resume functionality
- Individual download control

### Progress Tracking
- Real-time progress updates
- Download speed calculation
- Visual progress bars
- Detailed status information

### Error Handling
- Comprehensive error logging
- User-friendly error messages
- Automatic retry mechanisms
- Graceful degradation

## Development Notes

- The current implementation includes a mock client for development and testing
- For production use, proper TDLib integration is recommended
- The GUI is built with Tkinter for maximum compatibility
- SQLite database ensures download state persistence

## Troubleshooting

1. **Import Errors**: Run `python test_setup.py` to check dependencies
2. **Connection Issues**: Verify API credentials in `config.ini`
3. **Download Failures**: Check logs in the `logs/` directory
4. **Permission Errors**: Ensure write access to download directory

## License

MIT License
