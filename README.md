# AutoTest - Web Testing Tool

UWAutoTest is an automated website testing tool built with Python, Selenium, and Tkinter. It allows you to create, save, and run test cases for web applications without writing code.

## How to Use the Program

UWAutoTest provides a user-friendly GUI with three main tabs:

1. **Test Editor**: Create and edit individual test cases by adding a sequence of actions
2. **Test Runner**: Execute test cases individually or run multiple tests as a suite
3. **Settings**: Configure browser preferences, timeouts, and other testing parameters

The workflow is simple:
1. Create a test case in the Test Editor by specifying a name, base URL, and sequence of actions
2. Save your test case to the `test_cases/` directory
3. Run your test case from the Test Runner tab
4. View results, screenshots, and error reports

You can also group multiple test cases into test suites for batch execution, making it easy to run comprehensive testing scenarios.

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

UWAutoTest supports the following action types for building comprehensive test cases:

#### **Navigate**
- **Purpose**: Navigate to a URL (can be absolute or relative to the base URL)
- **Target**: URL to navigate to (e.g., "/login", "https://example.com/page")
- **Value**: Not used
- **Usage**: Use this as the first action to go to a specific page, or to navigate between pages during testing

#### **Click**
- **Purpose**: Click on an element (buttons, links, etc.)
- **Target**: CSS selector of the element to click (e.g., "#submit-btn", ".menu-item")
- **Value**: Not used
- **Usage**: Interact with buttons, links, or any clickable elements on the page

#### **Input**
- **Purpose**: Enter text into input fields
- **Target**: CSS selector of the input field (e.g., "#username", "input[name='email']")
- **Value**: Text to enter into the field
- **Usage**: Fill out forms, search boxes, or any text input fields

#### **Select**
- **Purpose**: Select an option from a dropdown menu
- **Target**: CSS selector of the select element (e.g., "#country", "select[name='category']")
- **Value**: Visible text of the option to select
- **Usage**: Choose options from dropdown menus or select lists

#### **Submit**
- **Purpose**: Submit a form
- **Target**: CSS selector of the form or submit button (e.g., "#login-form", "form")
- **Value**: Not used
- **Usage**: Submit forms after filling out required fields

#### **Wait**
- **Purpose**: Wait for a specified time or for an element to appear
- **Target**: CSS selector of element to wait for (optional)
- **Value**: Number of seconds to wait (if no target specified)
- **Usage**: Add delays for page loading, animations, or wait for dynamic content

#### **Assert Text**
- **Purpose**: Verify that specific text appears in an element
- **Target**: CSS selector of the element to check (e.g., ".success-message", "h1")
- **Value**: Text that should be present in the element
- **Usage**: Validate that expected content appears after actions (success messages, page titles, etc.)

#### **Assert Element**
- **Purpose**: Verify that an element exists or doesn't exist on the page
- **Target**: CSS selector of the element to check
- **Value**: "true" to assert element exists, "false" to assert it doesn't exist
- **Usage**: Verify page structure, confirm elements appear/disappear after actions

#### **Screenshot**
- **Purpose**: Take a screenshot of the current page
- **Target**: Not used
- **Value**: Not used
- **Usage**: Capture visual evidence of test execution, useful for debugging and reporting

#### **Execute Script**
- **Purpose**: Run custom JavaScript code
- **Target**: CSS selector of element to pass to script (optional)
- **Value**: JavaScript code to execute
- **Usage**: Perform advanced interactions, manipulate page state, or execute custom logic

### Tips for Using Actions

- **CSS Selectors**: Use specific selectors like IDs (#element-id) when possible for reliability
- **Wait Strategy**: Add Wait actions before interacting with dynamic content or after page navigation
- **Assertions**: Use Assert actions to verify expected outcomes and catch test failures
- **Screenshots**: Take screenshots at key points to document test execution
- **Error Handling**: The test runner will automatically capture error screenshots if an action fails

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
