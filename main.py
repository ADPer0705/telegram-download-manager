import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import asyncio
from pathlib import Path
import webbrowser
from config_manager import ConfigManager
from telegram_client import TelegramClient
from download_manager import DownloadManager
from logger import Logger

class TelegramDownloadManagerGUI:
    """Main GUI application for Telegram Download Manager."""
    
    def __init__(self):
        self.logger = Logger().get_logger(__name__)
        self.config_manager = None
        self.telegram_client = None
        self.download_manager = None
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Telegram Download Manager")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.status_var = tk.StringVar(value="Not connected")
        self.download_path_var = tk.StringVar()
        
        # Initialize GUI
        self.create_gui()
        
        # Initialize application
        self.initialize_app()
    
    def create_gui(self):
        """Create the GUI layout."""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding=10)
        status_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Label(status_frame, text="Connection:").grid(row=0, column=0, sticky="w")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=1, sticky="w", padx=(10, 0))
        
        self.connect_button = ttk.Button(status_frame, text="Connect", command=self.connect_telegram)
        self.connect_button.grid(row=0, column=2, padx=(20, 0))
        
        # Download path frame
        path_frame = ttk.LabelFrame(main_frame, text="Download Settings", padding=10)
        path_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        path_frame.columnconfigure(1, weight=1)
        
        ttk.Label(path_frame, text="Download Path:").grid(row=0, column=0, sticky="w")
        path_entry = ttk.Entry(path_frame, textvariable=self.download_path_var)
        path_entry.grid(row=0, column=1, sticky="ew", padx=(10, 10))
        
        ttk.Button(path_frame, text="Browse", command=self.browse_download_path).grid(row=0, column=2)
        
        # Add download frame
        add_frame = ttk.LabelFrame(main_frame, text="Add Download", padding=10)
        add_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        add_frame.columnconfigure(1, weight=1)
        
        ttk.Label(add_frame, text="File ID:").grid(row=0, column=0, sticky="w")
        self.file_id_entry = ttk.Entry(add_frame)
        self.file_id_entry.grid(row=0, column=1, sticky="ew", padx=(10, 10))
        
        ttk.Button(add_frame, text="Add Download", command=self.add_download).grid(row=0, column=2)
        
        ttk.Label(add_frame, text="File Name:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.file_name_entry = ttk.Entry(add_frame)
        self.file_name_entry.grid(row=1, column=1, sticky="ew", padx=(10, 10), pady=(10, 0))
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.pause_button = ttk.Button(control_frame, text="Pause All", command=self.toggle_pause)
        self.pause_button.pack(side="left", padx=(0, 5))
        
        ttk.Button(control_frame, text="Clear Completed", command=self.clear_completed).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Refresh", command=self.refresh_downloads).pack(side="left", padx=5)
        
        # Downloads list frame
        downloads_frame = ttk.LabelFrame(main_frame, text="Downloads", padding=10)
        downloads_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        downloads_frame.columnconfigure(0, weight=1)
        downloads_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Treeview for downloads
        columns = ("File Name", "Status", "Progress", "Size", "Speed")
        self.downloads_tree = ttk.Treeview(downloads_frame, columns=columns, show="tree headings")
        
        # Configure columns
        self.downloads_tree.heading("#0", text="ID")
        self.downloads_tree.column("#0", width=50, minwidth=50)
        
        for col in columns:
            self.downloads_tree.heading(col, text=col)
            if col == "File Name":
                self.downloads_tree.column(col, width=200, minwidth=150)
            elif col == "Progress":
                self.downloads_tree.column(col, width=100, minwidth=80)
            else:
                self.downloads_tree.column(col, width=80, minwidth=60)
        
        # Scrollbars for treeview
        v_scrollbar = ttk.Scrollbar(downloads_frame, orient="vertical", command=self.downloads_tree.yview)
        h_scrollbar = ttk.Scrollbar(downloads_frame, orient="horizontal", command=self.downloads_tree.xview)
        
        self.downloads_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for treeview and scrollbars
        self.downloads_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Context menu for downloads
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Retry", command=self.retry_selected)
        self.context_menu.add_command(label="Cancel", command=self.cancel_selected)
        self.context_menu.add_command(label="Remove", command=self.remove_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Open Folder", command=self.open_folder)
        
        self.downloads_tree.bind("<Button-3>", self.show_context_menu)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding=10)
        log_frame.grid(row=5, column=0, columnspan=2, sticky="ew")
        log_frame.columnconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, state="disabled")
        self.log_text.grid(row=0, column=0, sticky="ew")
        
        # Status bar
        self.status_bar = ttk.Label(main_frame, text="Ready", relief="sunken", anchor="w")
        self.status_bar.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 0))
    
    def initialize_app(self):
        """Initialize the application."""
        try:
            # Load configuration
            self.config_manager = ConfigManager()
            download_config = self.config_manager.get_download_config()
            self.download_path_var.set(download_config['download_path'])
            
            self.log_message("Application initialized successfully")
            
        except Exception as e:
            self.log_message(f"Error initializing application: {e}")
            messagebox.showerror("Initialization Error", 
                               f"Error loading configuration: {e}\\n\\n"
                               "Please check config.ini file")
    
    def connect_telegram(self):
        """Connect to Telegram."""
        if self.telegram_client and self.telegram_client.is_authenticated():
            self.disconnect_telegram()
            return
        
        def connect_thread():
            try:
                self.root.after(0, lambda: self.status_var.set("Connecting..."))
                self.root.after(0, lambda: self.connect_button.configure(state="disabled"))
                
                # Get Telegram configuration
                telegram_config = self.config_manager.get_telegram_config()
                
                # Initialize Telegram client
                self.telegram_client = TelegramClient(
                    api_id=telegram_config['api_id'],
                    api_hash=telegram_config['api_hash'],
                    phone=telegram_config['phone']
                )
                
                # Connect to Telegram
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                success = loop.run_until_complete(self.telegram_client.initialize())
                loop.close()
                
                if success:
                    # Initialize download manager
                    download_config = self.config_manager.get_download_config()
                    self.download_manager = DownloadManager(download_config, self.telegram_client)
                    self.download_manager.add_status_callback(self.on_download_status_change)
                    self.download_manager.start_downloads()
                    
                    self.root.after(0, lambda: self.status_var.set("Connected"))
                    self.root.after(0, lambda: self.connect_button.configure(text="Disconnect", state="normal"))
                    self.root.after(0, lambda: self.log_message("Connected to Telegram successfully"))
                    self.root.after(0, self.refresh_downloads)
                else:
                    raise Exception("Failed to connect to Telegram")
                
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set("Connection failed"))
                self.root.after(0, lambda: self.connect_button.configure(state="normal"))
                self.root.after(0, lambda: self.log_message(f"Connection error: {e}"))
                self.root.after(0, lambda: messagebox.showerror("Connection Error", f"Failed to connect: {e}"))
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def disconnect_telegram(self):
        """Disconnect from Telegram."""
        try:
            if self.download_manager:
                self.download_manager.stop_downloads()
                self.download_manager = None
            
            if self.telegram_client:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.telegram_client.close())
                loop.close()
                self.telegram_client = None
            
            self.status_var.set("Disconnected")
            self.connect_button.configure(text="Connect")
            self.log_message("Disconnected from Telegram")
            
        except Exception as e:
            self.log_message(f"Error disconnecting: {e}")
    
    def browse_download_path(self):
        """Browse for download directory."""
        path = filedialog.askdirectory(initialdir=self.download_path_var.get())
        if path:
            self.download_path_var.set(path)
            if self.download_manager:
                self.download_manager.download_path = Path(path)
    
    def add_download(self):
        """Add a new download."""
        if not self.download_manager:
            messagebox.showwarning("Not Connected", "Please connect to Telegram first")
            return
        
        file_id = self.file_id_entry.get().strip()
        file_name = self.file_name_entry.get().strip()
        
        if not file_id:
            messagebox.showwarning("Missing Information", "Please enter a file ID")
            return
        
        if not file_name:
            file_name = f"file_{file_id[:10]}"
        
        try:
            self.download_manager.add_download(file_id, file_name)
            self.file_id_entry.delete(0, tk.END)
            self.file_name_entry.delete(0, tk.END)
            self.log_message(f"Added download: {file_name}")
            self.refresh_downloads()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add download: {e}")
            self.log_message(f"Error adding download: {e}")
    
    def toggle_pause(self):
        """Toggle pause/resume downloads."""
        if not self.download_manager:
            return
        
        if self.pause_button["text"] == "Pause All":
            self.download_manager.pause_downloads()
            self.pause_button.configure(text="Resume All")
        else:
            self.download_manager.resume_downloads()
            self.pause_button.configure(text="Pause All")
    
    def clear_completed(self):
        """Clear completed downloads from the list."""
        # This would remove completed downloads from database
        self.log_message("Clear completed downloads - not yet implemented")
    
    def refresh_downloads(self):
        """Refresh the downloads list."""
        if not self.download_manager:
            return
        
        # Clear current items
        for item in self.downloads_tree.get_children():
            self.downloads_tree.delete(item)
        
        # Get all downloads
        downloads = self.download_manager.get_all_downloads()
        
        for download in downloads:
            progress_text = f"{download['progress']:.1f}%" if download['progress'] else "0%"
            size_text = self.format_file_size(download['file_size']) if download['file_size'] else "Unknown"
            
            self.downloads_tree.insert("", "end", 
                                     text=str(download['id']),
                                     values=(download['file_name'],
                                            download['status'],
                                            progress_text,
                                            size_text,
                                            ""))  # Speed placeholder
    
    def show_context_menu(self, event):
        """Show context menu for downloads."""
        item = self.downloads_tree.selection()
        if item:
            self.context_menu.post(event.x_root, event.y_root)
    
    def retry_selected(self):
        """Retry selected download."""
        selected = self.downloads_tree.selection()
        if selected and self.download_manager:
            item = self.downloads_tree.item(selected[0])
            file_id = item['values'][0]  # This would need proper mapping
            self.log_message("Retry download - not yet fully implemented")
    
    def cancel_selected(self):
        """Cancel selected download."""
        self.log_message("Cancel download - not yet fully implemented")
    
    def remove_selected(self):
        """Remove selected download."""
        self.log_message("Remove download - not yet fully implemented")
    
    def open_folder(self):
        """Open download folder."""
        try:
            import subprocess
            import sys
            
            path = self.download_path_var.get()
            if sys.platform == "win32":
                subprocess.run(f'explorer "{path}"')
            elif sys.platform == "darwin":
                subprocess.run(f'open "{path}"', shell=True)
            else:
                subprocess.run(f'xdg-open "{path}"', shell=True)
                
        except Exception as e:
            self.log_message(f"Error opening folder: {e}")
    
    def on_download_status_change(self, event_type, download_item):
        """Handle download status changes."""
        self.root.after(0, lambda: self.log_message(f"Download {event_type}: {download_item.get('file_name', 'Unknown') if download_item else ''}"))
        self.root.after(0, self.refresh_downloads)
    
    def log_message(self, message):
        """Add message to log."""
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, f"{message}\\n")
        self.log_text.configure(state="disabled")
        self.log_text.see(tk.END)
        
        # Update status bar
        self.status_bar.configure(text=message)
    
    def format_file_size(self, size_bytes):
        """Format file size in human readable format."""
        if not size_bytes:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def on_closing(self):
        """Handle application closing."""
        try:
            if self.download_manager:
                self.download_manager.stop_downloads()
            
            if self.telegram_client:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.telegram_client.close())
                loop.close()
                
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
        
        self.root.destroy()
    
    def run(self):
        """Run the application."""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


if __name__ == "__main__":
    app = TelegramDownloadManagerGUI()
    app.run()
