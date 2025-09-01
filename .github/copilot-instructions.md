# Copilot Instructions for Telegram Download Manager

## Project Overview
This is a clean, well-organized Python project for managing Telegram file downloads with a GUI interface. The project has been cleaned up from previous clutter and now focuses on a single, robust application.

## Project Structure
- `main.py` - Main GUI application entry point
- `telegram_client.py` - Telegram API client wrapper
- `download_manager.py` - Download queue and progress management
- `database.py` - SQLite database operations for persistence
- `config_manager.py` - Configuration file handling
- `logger.py` - Centralized logging setup
- `config.ini.example` - Configuration template
- `requirements.txt` - Python dependencies (clean, minimal)

## Key Features
- GUI interface built with Tkinter
- Robust download management with resume capability
- Database-backed persistence
- Queue management for multiple concurrent downloads
- Comprehensive error handling and logging
- Progress tracking with visual feedback

## Development Guidelines
- Keep the codebase clean and minimal
- Use the existing logger for all logging
- Follow the established configuration management pattern
- Maintain database schema consistency
- Ensure proper error handling throughout
- GUI should be user-friendly and responsive

## Architecture Notes
- Single client implementation (no multiple client variants)
- Configuration-driven behavior
- Database persistence for download state
- Async/await pattern for Telegram operations
- Tkinter for cross-platform GUI compatibility

## Documentation
- README.md contains comprehensive usage guide and FAQ
- All configuration options are documented
- Troubleshooting section covers common issues
- Clear setup instructions for new users
