#!/usr/bin/env python3
"""
BhumiApp - Property Information Lookup System
Main entry point for the application
"""

from ui.app import BhumiApp
import tkinter as tk


def main():
    """Initialize and run the application"""
    root = tk.Tk()
    app = BhumiApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
