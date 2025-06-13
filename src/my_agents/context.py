from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    """Enum for user roles in the company."""
    ADMIN = "admin"
    DEVELOPER = "developer"
    SUPPORT = "support"
    SALES = "sales"
    CHAT_USER = "chat_user"

# Predefined users with their roles
KNOWN_USERS = {
    "John Smith": UserRole.ADMIN,
    "Alice Johnson": UserRole.DEVELOPER,
    "Bob Wilson": UserRole.SUPPORT,
    "Emma Davis": UserRole.SALES
}

@dataclass
class UserContext:
    """Context class to hold user-specific information and state."""
    user_id: str
    user_name: str
    role: UserRole = UserRole.CHAT_USER
    is_premium_user: bool = False
    last_interaction: Optional[datetime] = None
    user_preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.user_preferences is None:
            self.user_preferences = {}
    
    def update_last_interaction(self):
        """Update the last interaction timestamp."""
        self.last_interaction = datetime.now()
    
    def get_user_greeting(self) -> str:
        """Get a personalized greeting based on user context."""
        if self.role == UserRole.ADMIN:
            return f"Welcome back, {self.user_name}! Your administrative privileges are active."
        elif self.role == UserRole.DEVELOPER:
            return f"Hello {self.user_name}! Ready to tackle some development tasks?"
        elif self.role == UserRole.SUPPORT:
            return f"Hi {self.user_name}! How can we help our users today?"
        elif self.role == UserRole.SALES:
            return f"Welcome {self.user_name}! Let's make some sales magic happen!"
        else:
            return f"Hello {self.user_name}! How can I assist you today?"
    
    def is_first_interaction(self) -> bool:
        """Check if this is the user's first interaction."""
        return self.last_interaction is None

    @classmethod
    def create_from_name(cls, name: str) -> 'UserContext':
        """Create a UserContext instance based on the user's name."""
        # Check if the user is in our known users list
        role = KNOWN_USERS.get(name, UserRole.CHAT_USER)
        
        # Create context with appropriate role
        return cls(
            user_id=f"user_{name.lower().replace(' ', '_')}",
            user_name=name,
            role=role,
            is_premium_user=role != UserRole.CHAT_USER  # Premium for known users
        ) 