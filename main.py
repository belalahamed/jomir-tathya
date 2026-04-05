#!/usr/bin/env python3
"""
BhumiApp - Property Information Lookup System
Main entry point for the application
"""

from ui.app import BhumiApp
from ui.login_window import LoginForm
import tkinter as tk

def main():
    """Initialize and run the application"""
    global root
    root = tk.Tk()
    
    def start_app(cookies):
        # Clear login UI
        for widget in root.winfo_children():
            widget.destroy()

        # Start main app with same root
        BhumiApp(root, cookies)
        
    LoginForm(root, on_login_success=start_app)
    
    root.mainloop()


if __name__ == "__main__":
    main()
