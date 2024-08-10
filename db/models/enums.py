from enum import Enum

"""
The menu category enum serves a better implementation and easier crud utilities
for menu items.
"""


class UserType(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class MenuCategory(Enum):
    MAIN_COURSES = "main_courses"
    DRINKS = "drinks"
    OTHER = "other"
    # I shall add the enum types later


class OrderStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class NotificationStatus(Enum):
    READ = "read"
    UNREAD = "unread"
