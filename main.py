#!/usr/bin/env python3
"""
UWAutoTest - Automated Website Testing Tool
Main application entry point
"""
import sys

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    print("Error: Tkinter is not installed. This application requires Tkinter.")
    print("If you're using macOS, you may need to install Python with Tkinter support:")
    print("  brew install python-tk  # If using Homebrew")
    print("  # Or download Python from python.org which includes Tkinter")
    print("If you're using Linux, try:")
    print("  sudo apt-get install python3-tk  # For Debian/Ubuntu")
    print("  sudo dnf install python3-tkinter  # For Fedora")
    sys.exit(1)

from app.gui import TestingToolGUI

if __name__ == "__main__":
    print("Starting UWAutoTest...")
    root = tk.Tk()
    root.title("UWAutoTest - Web Testing Tool")
    root.geometry("1000x800")
    app = TestingToolGUI(root)
    root.mainloop()
