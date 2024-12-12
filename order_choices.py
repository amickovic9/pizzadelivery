from enum import Enum


class OrderStatusEnum(Enum):
    PENDING = 'PENDING'
    IN_TRANSIT = 'IN-TRANSIT'
    DELIVERED = 'DELIVERED'