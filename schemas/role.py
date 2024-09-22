from sqlalchemy import Column, Integer, String, ForeignKey
from core.database import Base

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    org_id = Column(Integer, ForeignKey('organization.id', ondelete='CASCADE'), nullable=False)
