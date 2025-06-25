"""
Data models for the UWAutoTest application
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any
import json


class ActionType(Enum):
    """Types of actions that can be performed in a test case"""
    NAVIGATE = "Navigate"
    CLICK = "Click"
    INPUT = "Input"
    SELECT = "Select"
    SUBMIT = "Submit"
    WAIT = "Wait"
    ASSERT_TEXT = "Assert Text"
    ASSERT_ELEMENT = "Assert Element"
    SCREENSHOT = "Screenshot"
    EXECUTE_SCRIPT = "Execute Script"


@dataclass
class TestAction:
    """Represents a single action in a test case"""
    action_type: ActionType
    target: str = ""  # CSS selector or URL for navigate
    value: str = ""   # Value for input or text to assert
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "action_type": self.action_type.value,
            "target": self.target,
            "value": self.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestAction':
        """Create TestAction from dictionary"""
        return cls(
            action_type=ActionType(data["action_type"]),
            target=data["target"],
            value=data["value"]
        )


@dataclass
class TestCase:
    """Represents a test case with a sequence of actions"""
    name: str
    base_url: str
    actions: List[TestAction] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "base_url": self.base_url,
            "actions": [action.to_dict() for action in self.actions]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestCase':
        """Create TestCase from dictionary"""
        test_case = cls(
            name=data["name"],
            base_url=data["base_url"]
        )
        
        test_case.actions = [TestAction.from_dict(action) for action in data["actions"]]
        return test_case
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'TestCase':
        """Create TestCase from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)
