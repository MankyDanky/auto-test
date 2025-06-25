# UWAutoTest - Web Testing Tool

UWAutoTest is an automated website testing tool built with Python, Selenium, and Tkinter. It allows you to create, save, and run test cases for web applications without writing code.

## Features

- User-friendly GUI built with Tkinter
- Create test cases with multiple actions
- Save and load test cases
- Group test cases into test suites
- Execute tests with different browsers (Chrome, Firefox, Edge)
- Detailed test results and screenshots

## Installation

1. Clone this repository
2. Run the installation script:

```bash
python install.py
```

This script will:
- Check if Python 3.6+ is installed
- Verify if Tkinter is available (required for the GUI)
- Install the required packages from requirements.txt
- Create necessary directories

**Note:** Tkinter is required for this application. If it's not installed, the installation script will provide instructions for your operating system.

## Usage

1. Run the application:

```bash
python main.py
```

2. The application has three main tabs:
   - Test Editor: Create and edit test cases
   - Test Runner: Run test cases individually or in suites
   - Settings: Configure browser settings and directories

### Creating a Test Case

1. In the Test Editor tab, click "New"
2. Enter a test name and base URL
3. Add actions to your test case:
   - Select an action type (Navigate, Click, Input, etc.)
   - Enter a target (CSS selector or URL for navigate)
   - Enter a value (if needed, e.g., text for input fields)
   - Click "Add Action"
4. Save your test case by clicking "Save"

### Running Tests

1. In the Test Runner tab, select one or more test cases
2. Click "Run Selected" to execute the tests
3. View the results in the right panel

### Available Actions

- **Navigate**: Go to a URL (absolute or relative to base URL)
- **Click**: Click on an element
- **Input**: Enter text into an input field
- **Select**: Select an option from a dropdown
- **Submit**: Submit a form
- **Wait**: Wait for a specified time or element
- **Assert Text**: Verify text content in an element
- **Assert Element**: Verify element exists or does not exist
- **Screenshot**: Take a screenshot
- **Execute Script**: Run JavaScript

## Example Test Case

A simple login test case might include:

1. Navigate to "/login"
2. Input username in "#username" field
3. Input password in "#password" field
4. Click on "#loginButton"
5. Assert Text "Welcome" in ".welcome-message"

## Directory Structure

- `/app`: Main application code
  - `gui.py`: Main GUI implementation
  - `models.py`: Data models for test cases
  - `test_manager.py`: Handles saving/loading tests
  - `test_runner.py`: Runs tests with Selenium
- `main.py`: Main entry point
- `test_cases/`: Directory for saved test cases
- `test_suites/`: Directory for saved test suites

## Requirements

- Python 3.6+
- Selenium
- Tkinter (usually comes with Python)
- Chrome, Firefox, or Edge browser

## License

MIT License
