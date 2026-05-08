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

class VehicleType(str, Enum):
    CAR = "Car"
    MOTORCYCLE = "Motorcycle"
    TRUCK = "Truck"
    VAN = "Van"

class LiscenseType(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"