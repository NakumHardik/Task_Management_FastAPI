
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey 
from src.utils.db import Base

class taskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_complated = Column(Boolean, default=False)

    user_id = Column(Integer,ForeignKey("user_table.id",ondelete="CASCADE"))