"""
Test Manager module for the UWAutoTest application
Handles loading and saving test cases and suites
"""
import os
import json
from typing import List
from app.models import TestCase


class TestManager:
    """Manages test cases and suites"""
    
    def __init__(self):
        """Initialize the test manager"""
        pass
    
    def save_test_case(self, test_case: TestCase, file_path: str) -> None:
        """Save a test case to a JSON file
        
        Args:
            test_case: The TestCase object to save
            file_path: Path to save the file
        """
        with open(file_path, 'w') as f:
            json.dump(test_case.to_dict(), f, indent=2)
    
    def load_test_case(self, file_path: str) -> TestCase:
        """Load a test case from a JSON file
        
        Args:
            file_path: Path to the test case file
            
        Returns:
            A TestCase object
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
            return TestCase.from_dict(data)
    
    def save_test_suite(self, test_names: List[str], file_path: str) -> None:
        """Save a test suite to a JSON file
        
        Args:
            test_names: List of test case names
            file_path: Path to save the suite file
        """
        data = {
            "name": os.path.basename(file_path).split('.')[0],
            "tests": test_names
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_test_suite(self, file_path: str) -> List[str]:
        """Load a test suite from a JSON file
        
        Args:
            file_path: Path to the test suite file
            
        Returns:
            List of test case names
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get("tests", [])
