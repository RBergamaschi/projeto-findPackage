from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class UserRole(str, Enum):
    CUSTOMER = "Customer"
    DRIVER = "Driver"
    ADMIN = "Admin"