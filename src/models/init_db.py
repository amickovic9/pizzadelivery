from src.models.database import engine,Base
from src.models.user import User
from src.models.order import Order

Base.metadata.create_all(engine)
