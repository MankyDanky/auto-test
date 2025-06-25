#!/usr/bin/env python3
"""
Test script to verify ChromeDriver functionality
"""
import sys
import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import OperationSystemManager

print(f"Python version: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Architecture: {platform.machine()}")

print("\nAttempting to initialize Chrome WebDriver...")

try:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        print("Detected macOS with ARM64 architecture (Apple Silicon)")
        # Set an environment variable to force ARM64 driver download
        os.environ["WDM_ARCHITECTURE"] = "arm64"
        driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            ),
            options=options
        )
    else:
        print(f"Using default ChromeDriver for {platform.system()}")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    
    print("\nWebDriver initialized successfully!")
    print(f"Chrome version: {driver.capabilities['browserVersion']}")
    print(f"ChromeDriver version: {driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]}")
    
    driver.get("https://www.google.com")
    print(f"Page title: {driver.title}")
    
    driver.quit()
    print("Test completed successfully!")
    
except Exception as e:
    print(f"\nError initializing WebDriver: {e}")
    import traceback
    print("\nDetailed error information:")
    traceback.print_exc()
    sys.exit(1)
