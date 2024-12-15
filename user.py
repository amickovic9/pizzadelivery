from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String
from sqlalchemy.orm import relationship
from order import Order

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True,nullable=False)
    email = Column(String(50), unique=True,nullable=False)
    password = Column(Text, nullable=False)
    token = Column(Text)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    orders = relationship('Order', back_populates='user')

    def __reppr__(self):
        return f"<User {self.username}"
    
    def to_dict(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.username,
            'is_staff' : self.is_staff,
            'is_active' : self.is_active
        }
