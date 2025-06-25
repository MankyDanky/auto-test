#!/usr/bin/env python3
"""
UWAutoTest - Installation Script
This script helps users install dependencies and set up the application.
"""
import sys
import os
import subprocess
import platform

def print_header():
    print("\n===================================")
    print("  UWAutoTest - Installation Script")
    print("===================================\n")

def check_python_version():
    print("Checking Python version...")
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 6):
        print(f"Error: Python 3.6+ is required. You have Python {major}.{minor}")
        return False
    print(f"Found Python {major}.{minor} ✓")
    return True

def check_tkinter():
    print("\nChecking for Tkinter...")
    try:
        import tkinter
        print("Tkinter is installed ✓")
        return True
    except ImportError:
        print("Tkinter is not installed ✗")
        system = platform.system()
        if system == "Darwin":  # macOS
            print("\nTo install Tkinter on macOS, try:")
            print("  brew install python-tk")
            print("  # Or download Python from python.org which includes Tkinter")
        elif system == "Linux":
            distro = platform.linux_distribution()[0] if hasattr(platform, "linux_distribution") else ""
            if "Ubuntu" in distro or "Debian" in distro:
                print("\nTo install Tkinter on Ubuntu/Debian, try:")
                print("  sudo apt-get install python3-tk")
            elif "Fedora" in distro:
                print("\nTo install Tkinter on Fedora, try:")
                print("  sudo dnf install python3-tkinter")
            else:
                print("\nTo install Tkinter on Linux, try:")
                print("  sudo apt-get install python3-tk  # For Debian-based distributions")
                print("  sudo dnf install python3-tkinter  # For Fedora-based distributions")
        elif system == "Windows":
            print("\nTo install Tkinter on Windows:")
            print("  Reinstall Python and make sure to check 'tcl/tk and IDLE' during installation")
        return False

def install_dependencies():
    print("\nInstalling Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully ✓")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_directories():
    print("\nCreating necessary directories...")
    os.makedirs("test_cases", exist_ok=True)
    os.makedirs("test_suites", exist_ok=True)
    print("Directories created ✓")

def main():
    print_header()
    
    if not check_python_version():
        sys.exit(1)
    
    tkinter_available = check_tkinter()
    
    if install_dependencies():
        create_directories()
        
        print("\n===================================")
        if tkinter_available:
            print("  Installation completed successfully!")
            print("  Run the application with:")
            print("    python main.py")
        else:
            print("  Installation partially completed.")
            print("  Please install Tkinter to use the application.")
            print("  After installing Tkinter, run:")
            print("    python main.py")
        print("===================================\n")

if __name__ == "__main__":
    main()
