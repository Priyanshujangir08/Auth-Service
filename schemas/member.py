from sqlalchemy import Column, Integer, ForeignKey, JSON, BigInteger
from sqlalchemy.orm import relationship
from core.database import Base

class Member(Base):
    __tablename__ = 'member'
    
    id = Column(Integer, primary_key=True, index=True)  # Define a primary key
    org_id = Column(Integer, ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id", ondelete="CASCADE"), nullable=False)
    status = Column(Integer, default=0, nullable=False)
    settings = Column(JSON, default={}, nullable=True)
    created_at = Column(BigInteger, nullable=True)
    updated_at = Column(BigInteger, nullable=True)

    # Relationships
    organization = relationship("Organization")  
    user = relationship("User")  
    role = relationship("Role")  