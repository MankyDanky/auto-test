"""
Test Runner module for the UWAutoTest application
Executes test cases using Selenium WebDriver
"""
import time
from typing import Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from app.models import TestCase, TestAction, ActionType


class TestRunner:
    """Runs automated test cases using Selenium WebDriver"""
    
    def __init__(self, browser="Chrome", headless=False, wait_time=10):
        """Initialize the test runner
        
        Args:
            browser: Browser to use ('Chrome', 'Firefox', or 'Edge')
            headless: Whether to run in headless mode
            wait_time: Implicit wait time in seconds
        """
        self.browser = browser
        self.headless = headless
        self.wait_time = wait_time
    
    def _create_driver(self) -> webdriver.Remote:
        """Create and configure a WebDriver instance
        
        Returns:
            Configured WebDriver instance
        """
        if self.browser == "Chrome":
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            # Set specific options for Chrome on macOS ARM (Apple Silicon)
            import platform
            import os
            
            if platform.system() == "Darwin" and platform.machine() == "arm64":
                # Set an environment variable to force ARM64 driver download for Mac
                os.environ["WDM_ARCHITECTURE"] = "arm64"
                driver = webdriver.Chrome(
                    service=ChromeService(
                        ChromeDriverManager().install()
                    ),
                    options=options
                )
            else:
                # Default case for other platforms
                driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=options
                )
        
        elif self.browser == "Firefox":
            options = webdriver.FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        
        elif self.browser == "Edge":
            options = webdriver.EdgeOptions()
            if self.headless:
                options.add_argument("--headless")
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")
            
        driver.implicitly_wait(self.wait_time)
        driver.maximize_window()
        return driver
    
    def run_test(self, test_case: TestCase, browser=None, headless=None, wait_time=None) -> Dict[str, Any]:
        """Run a test case
        
        Args:
            test_case: The TestCase to run
            browser: Override the default browser
            headless: Override the default headless setting
            wait_time: Override the default wait time
            
        Returns:
            Dictionary with test results
        """
        # Override settings if provided
        if browser is not None:
            self.browser = browser
        if headless is not None:
            self.headless = headless
        if wait_time is not None:
            self.wait_time = wait_time
            
        result = {
            "success": False,
            "error": None,
            "duration": 0,
            "screenshots": []
        }
        
        driver = None
        start_time = time.time()
        
        try:
            # Initialize driver with better error handling
            try:
                driver = self._create_driver()
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                result["error"] = f"WebDriver initialization failed: {str(e)}\n\nDetails: {error_details}"
                return result
            
            # Process each action in the test case
            for i, action in enumerate(test_case.actions):
                try:
                    self._execute_action(driver, action, test_case.base_url, i, result)
                except Exception as e:
                    result["error"] = f"Error on action #{i+1} ({action.action_type.value}): {str(e)}"
                    # Capture screenshot on error
                    self._capture_error_screenshot(driver, i, result)
                    return result
            
            # Test completed successfully
            result["success"] = True
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            result["error"] = f"Test initialization error: {str(e)}\n\nDetails: {error_details}"
            
        finally:
            if driver:
                driver.quit()
            result["duration"] = time.time() - start_time
            
        return result
    
    def _execute_action(self, driver: webdriver.Remote, action: TestAction, base_url: str, 
                       action_index: int, result: Dict[str, Any]) -> None:
        """Execute a single test action
        
        Args:
            driver: WebDriver instance
            action: The TestAction to execute
            base_url: Base URL of the test case
            action_index: Index of the current action
            result: Result dictionary to update
        """
        if action.action_type == ActionType.NAVIGATE:
            url = action.target
            if not url.startswith(('http://', 'https://')):
                # Relative URL, prepend base_url
                url = base_url + action.target
            driver.get(url)
            
        elif action.action_type == ActionType.CLICK:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, action.target))
            )
            element.click()
            
        elif action.action_type == ActionType.INPUT:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, action.target))
            )
            element.clear()
            element.send_keys(action.value)
            
        elif action.action_type == ActionType.SELECT:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, action.target))
            )
            select = Select(element)
            select.select_by_visible_text(action.value)
            
        elif action.action_type == ActionType.SUBMIT:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, action.target))
            )
            element.submit()
            
        elif action.action_type == ActionType.WAIT:
            if action.value.isdigit():
                time.sleep(int(action.value))
            else:
                # Wait for element if target is provided
                if action.target:
                    WebDriverWait(driver, self.wait_time).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, action.target))
                    )
                    
        elif action.action_type == ActionType.ASSERT_TEXT:
            element = WebDriverWait(driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, action.target))
            )
            actual_text = element.text
            if action.value not in actual_text:
                raise AssertionError(f"Text '{action.value}' not found in element. Actual text: '{actual_text}'")
                
        elif action.action_type == ActionType.ASSERT_ELEMENT:
            # Check if element exists based on CSS selector
            try:
                WebDriverWait(driver, self.wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, action.target))
                )
                if action.value.lower() == "false":
                    raise AssertionError(f"Element '{action.target}' exists but expected not to exist")
            except TimeoutException:
                if action.value.lower() != "false":
                    raise AssertionError(f"Element '{action.target}' does not exist but expected to exist")
                    
        elif action.action_type == ActionType.SCREENSHOT:
            screenshot_path = f"screenshot_{action_index}.png"
            driver.save_screenshot(screenshot_path)
            result["screenshots"].append(screenshot_path)
            
        elif action.action_type == ActionType.EXECUTE_SCRIPT:
            script = action.value
            if action.target:
                # Find element and pass to script
                element = driver.find_element(By.CSS_SELECTOR, action.target)
                driver.execute_script(script, element)
            else:
                # Execute script without element
                driver.execute_script(script)
    
    def _capture_error_screenshot(self, driver: webdriver.Remote, action_index: int, 
                                result: Dict[str, Any]) -> None:
        """Capture screenshot on error
        
        Args:
            driver: WebDriver instance
            action_index: Index of the failed action
            result: Result dictionary to update
        """
        try:
            error_screenshot = f"error_{action_index}.png"
            driver.save_screenshot(error_screenshot)
            result["screenshots"].append(error_screenshot)
        except Exception:
            # Ignore errors during screenshot capture
            pass
