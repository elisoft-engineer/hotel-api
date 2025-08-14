from enum import Enum


class UserType(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class MenuCategory(Enum):
    MAIN_COURSES = "main_courses"
    DRINKS = "drinks"
    OTHER = "other"
    # TODO: Add the enum types later


class OrderStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class NotificationStatus(Enum):
    READ = "read"
    UNREAD = "unread"
