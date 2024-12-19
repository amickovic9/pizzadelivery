from src.enum.order_choices import OrderStatusEnum
from src.enum.pizza_sizes import Pizza_Size
from src.models.database import Base
from sqlalchemy import Column, Integer, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship


class Order(Base):

    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    status = Column(SQLEnum(OrderStatusEnum), nullable=False)
    size = Column(SQLEnum(Pizza_Size), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')

    def __repr__(self):
        return f"<Order {self.id}>"
    
    def to_dict(self):
        return {
            'id' : self.id,
            'quantity': self. quantity,
            'status' : self.status.name,
            'size' : self.size.name
        }
