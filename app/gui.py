"""
GUI module for the UWAutoTest application
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from app.test_manager import TestManager
from app.test_runner import TestRunner
from app.models import TestCase, TestAction, ActionType

class TestingToolGUI:
    def __init__(self, root):
        self.root = root
        self.test_manager = TestManager()
        self.test_runner = TestRunner()
        
        # Current test case being edited
        self.current_test_case = None
        
        # Setup the GUI components
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the main GUI components"""
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        
        # Create main tabs
        self.test_editor_frame = ttk.Frame(self.notebook)
        self.test_runner_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)
        
        # Add the tabs to the notebook
        self.notebook.add(self.test_editor_frame, text="Test Editor")
        self.notebook.add(self.test_runner_frame, text="Test Runner")
        self.notebook.add(self.settings_frame, text="Settings")
        self.notebook.pack(expand=1, fill="both")
        
        # Setup each tab
        self.setup_test_editor()
        self.setup_test_runner()
        self.setup_settings()
        
        # Create a status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_test_editor(self):
        """Setup the test editor tab"""
        frame = self.test_editor_frame
        
        # Left panel - Test cases list
        left_panel = ttk.LabelFrame(frame, text="Test Cases")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=0, padx=5, pady=5)
        
        # Test cases listbox with scrollbar
        self.test_cases_listbox = tk.Listbox(left_panel, width=30, height=20)
        scrollbar = ttk.Scrollbar(left_panel)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.test_cases_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.test_cases_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.test_cases_listbox.yview)
        
        # Buttons for test case management
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="New", command=self.new_test_case).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Load", command=self.load_test_case).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Save", command=self.save_test_case).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_test_case).pack(side=tk.LEFT, padx=2)
        
        # Right panel - Test case editor
        right_panel = ttk.LabelFrame(frame, text="Test Case Editor")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1, padx=5, pady=5)
        
        # Test case details
        details_frame = ttk.Frame(right_panel)
        details_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(details_frame, text="Test Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.test_name_entry = ttk.Entry(details_frame, width=40)
        self.test_name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(details_frame, text="Base URL:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.base_url_entry = ttk.Entry(details_frame, width=40)
        self.base_url_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Test actions
        actions_frame = ttk.LabelFrame(right_panel, text="Test Actions")
        actions_frame.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)
        
        # Action list with scrollbar
        self.actions_tree = ttk.Treeview(actions_frame, columns=("Type", "Target", "Value"), show="headings")
        self.actions_tree.heading("Type", text="Action Type")
        self.actions_tree.heading("Target", text="Target")
        self.actions_tree.heading("Value", text="Value")
        self.actions_tree.column("Type", width=100)
        self.actions_tree.column("Target", width=250)
        self.actions_tree.column("Value", width=250)
        
        actions_scrollbar = ttk.Scrollbar(actions_frame, orient=tk.VERTICAL, command=self.actions_tree.yview)
        self.actions_tree.configure(yscrollcommand=actions_scrollbar.set)
        
        self.actions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        actions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action editor frame
        action_editor_frame = ttk.LabelFrame(right_panel, text="Action Editor")
        action_editor_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(action_editor_frame, text="Action Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.action_type_combo = ttk.Combobox(action_editor_frame, width=20)
        self.action_type_combo['values'] = [action_type.value for action_type in ActionType]
        self.action_type_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(action_editor_frame, text="Target (CSS Selector):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.target_entry = ttk.Entry(action_editor_frame, width=40)
        self.target_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(action_editor_frame, text="Value:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.value_entry = ttk.Entry(action_editor_frame, width=40)
        self.value_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Action buttons
        action_btn_frame = ttk.Frame(action_editor_frame)
        action_btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(action_btn_frame, text="Add Action", command=self.add_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_btn_frame, text="Update Action", command=self.update_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_btn_frame, text="Delete Action", command=self.delete_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_btn_frame, text="Move Up", command=self.move_action_up).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_btn_frame, text="Move Down", command=self.move_action_down).pack(side=tk.LEFT, padx=5)
        
        # Bind event for selecting test case
        self.test_cases_listbox.bind('<<ListboxSelect>>', self.on_test_case_select)
        
        # Bind event for selecting action
        self.actions_tree.bind('<<TreeviewSelect>>', self.on_action_select)
    
    def setup_test_runner(self):
        """Setup the test runner tab"""
        frame = self.test_runner_frame
        
        # Left panel - Test cases to run
        left_panel = ttk.LabelFrame(frame, text="Test Suite")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=0, padx=5, pady=5)
        
        # Test suite listbox with scrollbar
        self.test_suite_listbox = tk.Listbox(left_panel, width=30, height=20, selectmode=tk.MULTIPLE)
        scrollbar = ttk.Scrollbar(left_panel)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.test_suite_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.test_suite_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.test_suite_listbox.yview)
        
        # Buttons for test suite management
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Load All Tests", command=self.load_all_test_cases).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Run Selected", command=self.run_selected_tests).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Save Suite", command=self.save_test_suite).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Load Suite", command=self.load_test_suite).pack(side=tk.LEFT, padx=2)
        
        # Right panel - Results
        right_panel = ttk.LabelFrame(frame, text="Test Results")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1, padx=5, pady=5)
        
        # Results text area with scrollbar
        self.results_text = tk.Text(right_panel, wrap=tk.WORD)
        results_scrollbar = ttk.Scrollbar(right_panel)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.pack(fill=tk.BOTH, expand=1)
        self.results_text.config(yscrollcommand=results_scrollbar.set)
        results_scrollbar.config(command=self.results_text.yview)
        
        # Button to clear results
        ttk.Button(right_panel, text="Clear Results", command=self.clear_results).pack(pady=5)
    
    def setup_settings(self):
        """Setup the settings tab"""
        frame = self.settings_frame
        
        settings_frame = ttk.LabelFrame(frame, text="WebDriver Settings")
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Browser selection
        ttk.Label(settings_frame, text="Browser:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.browser_var = tk.StringVar(value="Chrome")
        ttk.Radiobutton(settings_frame, text="Chrome", variable=self.browser_var, value="Chrome").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(settings_frame, text="Firefox", variable=self.browser_var, value="Firefox").grid(row=0, column=2, sticky=tk.W)
        ttk.Radiobutton(settings_frame, text="Edge", variable=self.browser_var, value="Edge").grid(row=0, column=3, sticky=tk.W)
        
        # Headless mode
        self.headless_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="Run in headless mode", variable=self.headless_var).grid(row=1, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)
        
        # Implicit wait
        ttk.Label(settings_frame, text="Implicit wait (seconds):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.wait_var = tk.IntVar(value=10)
        ttk.Spinbox(settings_frame, from_=0, to=60, textvariable=self.wait_var, width=5).grid(row=2, column=1, sticky=tk.W)
        
        # Save directory
        save_frame = ttk.LabelFrame(frame, text="Save Locations")
        save_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(save_frame, text="Test Cases Directory:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.test_dir_var = tk.StringVar(value=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_cases"))
        test_dir_entry = ttk.Entry(save_frame, textvariable=self.test_dir_var, width=40)
        test_dir_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Button(save_frame, text="Browse", command=lambda: self.browse_directory(self.test_dir_var)).grid(row=0, column=2)
        
        ttk.Label(save_frame, text="Test Suites Directory:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.suite_dir_var = tk.StringVar(value=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_suites"))
        suite_dir_entry = ttk.Entry(save_frame, textvariable=self.suite_dir_var, width=40)
        suite_dir_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Button(save_frame, text="Browse", command=lambda: self.browse_directory(self.suite_dir_var)).grid(row=1, column=2)
        
        # Apply settings button
        ttk.Button(frame, text="Apply Settings", command=self.apply_settings).pack(pady=10)
    
    # Test Editor methods
    def new_test_case(self):
        """Create a new test case"""
        self.current_test_case = TestCase(name="New Test Case", base_url="")
        self.test_name_entry.delete(0, tk.END)
        self.test_name_entry.insert(0, self.current_test_case.name)
        self.base_url_entry.delete(0, tk.END)
        self.actions_tree.delete(*self.actions_tree.get_children())
        self.status_var.set("New test case created")
    
    def load_test_case(self):
        """Load a test case from file"""
        test_dir = self.test_dir_var.get()
        os.makedirs(test_dir, exist_ok=True)
        
        file_path = filedialog.askopenfilename(
            initialdir=test_dir,
            title="Select Test Case",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        
        if file_path:
            try:
                self.current_test_case = self.test_manager.load_test_case(file_path)
                self.test_name_entry.delete(0, tk.END)
                self.test_name_entry.insert(0, self.current_test_case.name)
                self.base_url_entry.delete(0, tk.END)
                self.base_url_entry.insert(0, self.current_test_case.base_url)
                
                # Update actions tree
                self.actions_tree.delete(*self.actions_tree.get_children())
                for action in self.current_test_case.actions:
                    self.actions_tree.insert("", "end", values=(action.action_type.value, action.target, action.value))
                
                self.status_var.set(f"Loaded test case: {self.current_test_case.name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load test case: {str(e)}")
    
    def save_test_case(self):
        """Save the current test case to file"""
        if not self.current_test_case:
            messagebox.showwarning("Warning", "No test case to save")
            return
            
        test_dir = self.test_dir_var.get()
        os.makedirs(test_dir, exist_ok=True)
        
        # Update test case with current values
        self.current_test_case.name = self.test_name_entry.get()
        self.current_test_case.base_url = self.base_url_entry.get()
        
        # Check if test case name is provided
        if not self.current_test_case.name:
            messagebox.showwarning("Warning", "Test case must have a name")
            return
        
        file_path = filedialog.asksaveasfilename(
            initialdir=test_dir,
            title="Save Test Case",
            defaultextension=".json",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
            initialfile=f"{self.current_test_case.name}.json"
        )
        
        if file_path:
            try:
                self.test_manager.save_test_case(self.current_test_case, file_path)
                self.status_var.set(f"Saved test case: {self.current_test_case.name}")
                self.load_all_test_cases()  # Refresh the test case list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save test case: {str(e)}")
    
    def delete_test_case(self):
        """Delete the selected test case"""
        selection = self.test_cases_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No test case selected")
            return
        
        test_name = self.test_cases_listbox.get(selection[0])
        test_dir = self.test_dir_var.get()
        test_path = os.path.join(test_dir, f"{test_name}.json")
        
        if os.path.exists(test_path):
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {test_name}?")
            if confirm:
                try:
                    os.remove(test_path)
                    self.status_var.set(f"Deleted test case: {test_name}")
                    self.load_all_test_cases()  # Refresh the test case list
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete test case: {str(e)}")
    
    def add_action(self):
        """Add a new action to the current test case"""
        if not self.current_test_case:
            messagebox.showwarning("Warning", "Create or load a test case first")
            return
        
        action_type_str = self.action_type_combo.get()
        target = self.target_entry.get()
        value = self.value_entry.get()
        
        if not action_type_str:
            messagebox.showwarning("Warning", "Select an action type")
            return
            
        try:
            action_type = ActionType(action_type_str)
            action = TestAction(action_type=action_type, target=target, value=value)
            self.current_test_case.actions.append(action)
            
            # Add to tree view
            self.actions_tree.insert("", "end", values=(action_type.value, target, value))
            
            # Clear input fields
            self.action_type_combo.set("")
            self.target_entry.delete(0, tk.END)
            self.value_entry.delete(0, tk.END)
            
            self.status_var.set(f"Added {action_type.value} action")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add action: {str(e)}")
    
    def update_action(self):
        """Update the selected action"""
        selection = self.actions_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "No action selected")
            return
        
        if not self.current_test_case:
            return
            
        index = self.actions_tree.index(selection[0])
        action_type_str = self.action_type_combo.get()
        target = self.target_entry.get()
        value = self.value_entry.get()
        
        if not action_type_str:
            messagebox.showwarning("Warning", "Select an action type")
            return
            
        try:
            action_type = ActionType(action_type_str)
            self.current_test_case.actions[index].action_type = action_type
            self.current_test_case.actions[index].target = target
            self.current_test_case.actions[index].value = value
            
            # Update tree view
            self.actions_tree.item(selection[0], values=(action_type.value, target, value))
            
            self.status_var.set(f"Updated action at position {index+1}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update action: {str(e)}")
    
    def delete_action(self):
        """Delete the selected action"""
        selection = self.actions_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "No action selected")
            return
        
        if not self.current_test_case:
            return
            
        index = self.actions_tree.index(selection[0])
        
        # Remove from test case
        del self.current_test_case.actions[index]
        
        # Remove from tree view
        self.actions_tree.delete(selection[0])
        
        self.status_var.set(f"Deleted action at position {index+1}")
    
    def move_action_up(self):
        """Move the selected action up in the list"""
        selection = self.actions_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "No action selected")
            return
        
        if not self.current_test_case:
            return
            
        index = self.actions_tree.index(selection[0])
        if index > 0:
            # Swap actions in the test case
            self.current_test_case.actions[index], self.current_test_case.actions[index-1] = \
                self.current_test_case.actions[index-1], self.current_test_case.actions[index]
            
            # Refresh tree view
            self.actions_tree.delete(*self.actions_tree.get_children())
            for action in self.current_test_case.actions:
                self.actions_tree.insert("", "end", values=(action.action_type.value, action.target, action.value))
            
            # Select the moved item
            item = self.actions_tree.get_children()[index-1]
            self.actions_tree.selection_set(item)
            self.actions_tree.focus(item)
            
            self.status_var.set(f"Moved action up")
    
    def move_action_down(self):
        """Move the selected action down in the list"""
        selection = self.actions_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "No action selected")
            return
        
        if not self.current_test_case:
            return
            
        index = self.actions_tree.index(selection[0])
        if index < len(self.current_test_case.actions) - 1:
            # Swap actions in the test case
            self.current_test_case.actions[index], self.current_test_case.actions[index+1] = \
                self.current_test_case.actions[index+1], self.current_test_case.actions[index]
            
            # Refresh tree view
            self.actions_tree.delete(*self.actions_tree.get_children())
            for action in self.current_test_case.actions:
                self.actions_tree.insert("", "end", values=(action.action_type.value, action.target, action.value))
            
            # Select the moved item
            item = self.actions_tree.get_children()[index+1]
            self.actions_tree.selection_set(item)
            self.actions_tree.focus(item)
            
            self.status_var.set(f"Moved action down")
    
    def on_test_case_select(self, event):
        """Handle test case selection event"""
        selection = self.test_cases_listbox.curselection()
        if not selection:
            return
            
        test_name = self.test_cases_listbox.get(selection[0])
        test_dir = self.test_dir_var.get()
        test_path = os.path.join(test_dir, f"{test_name}.json")
        
        if os.path.exists(test_path):
            try:
                self.current_test_case = self.test_manager.load_test_case(test_path)
                self.test_name_entry.delete(0, tk.END)
                self.test_name_entry.insert(0, self.current_test_case.name)
                self.base_url_entry.delete(0, tk.END)
                self.base_url_entry.insert(0, self.current_test_case.base_url)
                
                # Update actions tree
                self.actions_tree.delete(*self.actions_tree.get_children())
                for action in self.current_test_case.actions:
                    self.actions_tree.insert("", "end", values=(action.action_type.value, action.target, action.value))
                
                self.status_var.set(f"Loaded test case: {self.current_test_case.name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load test case: {str(e)}")
    
    def on_action_select(self, event):
        """Handle action selection event"""
        selection = self.actions_tree.selection()
        if not selection or not self.current_test_case:
            return
            
        index = self.actions_tree.index(selection[0])
        action = self.current_test_case.actions[index]
        
        # Update the action editor fields
        self.action_type_combo.set(action.action_type.value)
        self.target_entry.delete(0, tk.END)
        self.target_entry.insert(0, action.target)
        self.value_entry.delete(0, tk.END)
        self.value_entry.insert(0, action.value)
    
    # Test Runner methods
    def load_all_test_cases(self):
        """Load all test cases from the test directory"""
        test_dir = self.test_dir_var.get()
        os.makedirs(test_dir, exist_ok=True)
        
        # Clear test cases list
        self.test_cases_listbox.delete(0, tk.END)
        self.test_suite_listbox.delete(0, tk.END)
        
        # List all JSON files in the test directory
        try:
            for file in os.listdir(test_dir):
                if file.endswith('.json'):
                    test_name = os.path.splitext(file)[0]
                    self.test_cases_listbox.insert(tk.END, test_name)
                    self.test_suite_listbox.insert(tk.END, test_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load test cases: {str(e)}")
        
        self.status_var.set("Loaded all test cases")
    
    def run_selected_tests(self):
        """Run the selected tests"""
        selection = self.test_suite_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No tests selected")
            return
        
        # Get selected test names
        test_names = [self.test_suite_listbox.get(i) for i in selection]
        
        # Clear results
        self.clear_results()
        
        # Get the browser and headless settings
        browser = self.browser_var.get()
        headless = self.headless_var.get()
        wait_time = self.wait_var.get()
        
        # Run tests
        test_dir = self.test_dir_var.get()
        
        self.results_text.insert(tk.END, f"Running {len(test_names)} test(s) with {browser} browser...\n\n")
        self.root.update()
        
        success_count = 0
        
        for test_name in test_names:
            try:
                test_path = os.path.join(test_dir, f"{test_name}.json")
                test_case = self.test_manager.load_test_case(test_path)
                
                self.results_text.insert(tk.END, f"=== Running test: {test_name} ===\n")
                self.results_text.insert(tk.END, f"Base URL: {test_case.base_url}\n")
                self.results_text.insert(tk.END, f"Actions: {len(test_case.actions)}\n\n")
                self.root.update()
                
                # Run the test
                result = self.test_runner.run_test(
                    test_case, 
                    browser=browser, 
                    headless=headless,
                    wait_time=wait_time
                )
                
                if result["success"]:
                    self.results_text.insert(tk.END, "TEST PASSED\n")
                    self.results_text.insert(tk.END, f"Duration: {result['duration']:.2f} seconds\n\n")
                    success_count += 1
                else:
                    self.results_text.insert(tk.END, "TEST FAILED\n")
                    self.results_text.insert(tk.END, f"Error: {result['error']}\n\n")
                
            except Exception as e:
                self.results_text.insert(tk.END, f"ERROR: {str(e)}\n\n")
        
        self.results_text.insert(tk.END, f"=== Test Run Complete ===\n")
        self.results_text.insert(tk.END, f"Passed: {success_count}/{len(test_names)}\n")
        self.status_var.set(f"Test run complete. Passed: {success_count}/{len(test_names)}")
        
        # Scroll to the top
        self.results_text.see("1.0")
    
    def save_test_suite(self):
        """Save the current test suite to file"""
        selection = self.test_suite_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No tests selected")
            return
        
        # Get selected test names
        test_names = [self.test_suite_listbox.get(i) for i in selection]
        
        suite_dir = self.suite_dir_var.get()
        os.makedirs(suite_dir, exist_ok=True)
        
        file_path = filedialog.asksaveasfilename(
            initialdir=suite_dir,
            title="Save Test Suite",
            defaultextension=".json",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        
        if file_path:
            try:
                self.test_manager.save_test_suite(test_names, file_path)
                self.status_var.set(f"Saved test suite with {len(test_names)} tests")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save test suite: {str(e)}")
    
    def load_test_suite(self):
        """Load a test suite from file"""
        suite_dir = self.suite_dir_var.get()
        os.makedirs(suite_dir, exist_ok=True)
        
        file_path = filedialog.askopenfilename(
            initialdir=suite_dir,
            title="Select Test Suite",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        
        if file_path:
            try:
                test_names = self.test_manager.load_test_suite(file_path)
                
                # Update test suite listbox
                self.test_suite_listbox.selection_clear(0, tk.END)
                
                for i in range(self.test_suite_listbox.size()):
                    test_name = self.test_suite_listbox.get(i)
                    if test_name in test_names:
                        self.test_suite_listbox.selection_set(i)
                
                self.status_var.set(f"Loaded test suite with {len(test_names)} tests")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load test suite: {str(e)}")
    
    def clear_results(self):
        """Clear the results text area"""
        self.results_text.delete("1.0", tk.END)
        self.status_var.set("Results cleared")
    
    # Settings methods
    def browse_directory(self, string_var):
        """Browse for a directory and update the StringVar"""
        directory = filedialog.askdirectory()
        if directory:
            string_var.set(directory)
    
    def apply_settings(self):
        """Apply the settings"""
        # Create directories if they don't exist
        os.makedirs(self.test_dir_var.get(), exist_ok=True)
        os.makedirs(self.suite_dir_var.get(), exist_ok=True)
        
        # Update test runner with browser settings
        if hasattr(self, 'test_runner'):
            self.test_runner.browser = self.browser_var.get()
            self.test_runner.headless = self.headless_var.get()
            self.test_runner.wait_time = self.wait_var.get()
        
        messagebox.showinfo("Settings", "Settings applied successfully")
        self.status_var.set("Settings applied")
