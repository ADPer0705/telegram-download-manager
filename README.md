# 🚀 Telegram Download Manager

<div align="center">

![Telegram Download Manager](https://img.shields.io/badge/Telegram-Download_Manager-2CA5E0?style=for-the-badge&logo=telegram)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-FF6B35?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**The coolest way to download files from Telegram!** 🎉

[📥 Download](#quick-start) • [📚 Documentation](DOCS.md) • [🐛 Report Issues](https://github.com/ADPer0705/telegram-download-manager/issues)

---

</div>

## ✨ Why Choose Telegram Download Manager?

🎯 **Multiple Authentication Methods** - Choose what works best for you!  
⚡ **Lightning Fast Downloads** - Queue management with progress tracking  
🔄 **Resume Interrupted Downloads** - Never lose progress again  
💾 **Smart Database** - Persistent download history and queue state  
🎨 **Beautiful GUI** - User-friendly interface that just works  

## 🌟 Features

<div align="center">

| Feature | Description |
|---------|-------------|
| 🤖 **Bot Token Support** | Easy setup with Telegram bots |
| 🔑 **API Credentials** | Full access to all your files |
| 🎮 **Demo Mode** | Test without any setup |
| 📊 **Progress Tracking** | Real-time download progress |
| 🔄 **Resume Downloads** | Continue interrupted downloads |
| 📋 **Queue Management** | Handle multiple downloads efficiently |
| 💾 **Database Storage** | Persistent download history |
| 🛡️ **Error Handling** | Robust retry mechanisms |

</div>

## 🚀 Quick Start

<div align="center">

### ⚡ Get Started in 3 Steps!

</div>

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Configure Authentication
```bash
cp config.ini.example config.ini
# Edit config.ini - choose your preferred method below
```

### 3️⃣ Launch the App
```bash
python main.py
```

<div align="center">

🎉 **That's it! You're ready to download!**

</div>

---

## 🔐 Authentication Methods

Choose the method that fits your needs:

### 🤖 Bot Token (⭐ Recommended)
<div align="center">

**Perfect for most users - No phone verification needed!**

</div>

```ini
[telegram]
bot_token = YOUR_BOT_TOKEN_HERE
```

**Setup:**
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy your bot token to `config.ini`
4. **Done!** 🎯

**Best for:** Public files, group downloads, easy sharing

---

### 🔑 API Credentials (Full Access)
<div align="center">

**Complete access to all files you can see in Telegram**

</div>

```ini
[telegram]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
phone = YOUR_PHONE_NUMBER
```

**Setup:**
1. Visit [my.telegram.org](https://my.telegram.org/)
2. Login and go to "API development tools"
3. Create application and copy credentials
4. Add to `config.ini`

**Best for:** Private files, personal downloads, full control

---

### 🎮 Demo Mode (Zero Setup)
<div align="center">

**Test the app without any credentials!**

</div>

```ini
[telegram]
demo_mode = true
```

**Setup:** Just uncomment the line above!  
**Best for:** Testing, demos, trying out features

---

## 📸 Screenshots

<div align="center">

*Coming soon - beautiful screenshots of the GUI in action!*

</div>

---

## 🏗️ Project Structure

```
telegram_download_manager/
├── 🎯 main.py              # Main GUI application
├── 🤖 telegram_client.py   # User API client
├── 🔧 bot_client.py        # Bot API & demo clients
├── 📥 download_manager.py  # Download queue management
├── 💾 database.py          # SQLite persistence
├── ⚙️ config_manager.py    # Configuration handling
├── 📝 logger.py            # Logging system
├── 📋 config.ini.example   # Configuration template
├── 📦 requirements.txt     # Python dependencies
├── 📚 DOCS.md              # Detailed documentation
└── 📄 README.md            # This file
```

---

## 🎯 Usage Examples

### Basic Download
```bash
python main.py
# 1. Click "Connect"
# 2. Enter file ID
# 3. Click "Add Download"
# 4. Watch progress!
```

### Batch Downloads
- Add multiple file IDs
- Queue manages concurrent downloads
- Automatic retry on failures

### Resume Downloads
- Interrupted downloads resume automatically
- No progress lost on network issues
- Smart chunk-based resuming

---

## 🔧 Configuration

### Advanced Settings

```ini
[downloads]
download_path = ~/Downloads          # Where to save files (supports ~ for home directory)
max_concurrent_downloads = 3         # Parallel downloads
chunk_size = 1048576                 # Download chunk size
retry_attempts = 5                   # Retry failed downloads
retry_delay = 5                      # Delay between retries

[logging]
log_level = INFO                     # DEBUG, INFO, WARNING, ERROR
log_file = logs/telegram_downloader.log
```

### Download Path Configuration

- **Relative paths**: `./downloads`, `downloads/` 
- **Absolute paths**: `/home/user/Downloads`, `C:\Downloads\`
- **Home directory**: `~/Downloads` (automatically expanded)
- **Environment variables**: Supported via shell expansion

### Performance Tuning

- **Concurrent Downloads**: Balance speed vs. bandwidth
- **Chunk Size**: Larger = faster, smaller = more stable
- **Retry Settings**: Adjust based on your connection

---

## ❓ Quick FAQ

**Q: Which authentication method should I use?**  
A: Start with **Bot Token** - it's easiest! Use API credentials for full access.

**Q: Can I download private files?**  
A: Yes, with API credentials. Bot tokens work with public files only.

**Q: What file sizes are supported?**  
A: API credentials: No limit. Bot tokens: Up to 20MB (Telegram limit).

**Q: Does it resume interrupted downloads?**  
A: Yes! Automatically resumes from where it left off.

**Q: Can I download multiple files?**  
A: Absolutely! The queue handles multiple concurrent downloads.

---

## 🛠️ Development

### Requirements
- Python 3.8+
- Tkinter (usually included with Python)
- Internet connection

### Running Tests
```bash
python -c "import main; print('✅ All good!')"
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📈 Roadmap

- [ ] 📸 Add screenshots and demo GIFs
- [ ] 🌐 Web interface option
- [ ] 📱 Mobile app version
- [ ] 🔍 File search functionality
- [ ] 📊 Download analytics
- [ ] 🎨 Dark mode theme
- [ ] 🌍 Multi-language support

---

## 🤝 Support & Community

<div align="center">

**Need help? Found a bug? Have a suggestion?**

🐛 [Report Issues](https://github.com/ADPer0705/telegram-download-manager/issues)  
💬 [Discussions](https://github.com/ADPer0705/telegram-download-manager/discussions)  
📧 [Contact](mailto:your.email@example.com)

</div>

---

## 📄 License

<div align="center">

**MIT License** - Free to use, modify, and distribute!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

<div align="center">

**Made with ❤️ for the Telegram community**

⭐ **Star this repo if you found it useful!**

[⬆️ Back to Top](#-telegram-download-manager)

</div>
