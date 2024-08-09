from enum import Enum

"""
The menu category enum serves a better implementation and easier crud utilities
for menu items.
"""


class UserType(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class MenuCategory(str, Enum):
    MAIN_COURSES = "main_courses"
    DRINKS = "drinks"
    OTHER = "other"
    # I shall add the enum types later


class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class NotificationStatus(str, Enum):
    READ = "read"
    UNREAD = "unread"
