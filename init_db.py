from database import engine,Base
from user import User
from order import Order

Base.metadata.create_all(engine)