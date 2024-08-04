from enum import Enum

"""
The menu category enum serves a better implementation and easier crud utilities
for menu items.
"""

class MenuCategory(Enum):
    MAIN_COURSES = "main_courses"
    DRINKS = "drinks"
    # I shall add the enum types later
    

class OrderStatus(Enum):
    PENDING = "Pending"
    DELIVERED = "Delivered"
    PAID = "Paid"
    CANCELLED = "Cancelled"