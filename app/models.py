
# import uuid
from sqlalchemy import Column, Float, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
# from sqlalchemy.sql.functions import func
# from sqlalchemy.orm import validates
# import re

# from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from .database import Base

class User(Base):
    __tablename__ = 'User'

    # College ID (UUID) - Auto-generated using gen_random_uuid() in PostgreSQL
    user_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))

    # College Name - Unique and not null
    user_name = Column(String, unique=True, nullable=False)

    # Official email - Unique, valid email format, and not null
    email = Column(String, unique=True, primary_key=True, nullable=False)

    # Official phone - Unique, valid phone number format, and not null
    password = Column(String, unique=True, nullable=False)
    
    email_verified = Column(Boolean, nullable=False, server_default=text('false') ) 
    
    created_at = Column(DateTime,server_default=text('now()') , nullable=False)
    
    # feedback = relationship("user_feedback", back_populates="UserID")

# class Feedback(Base):
#     __tablename__ = 'Feedback'
    
#     feedback_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
#     # user_id = Column(UUID(as_uuid=True), ForeignKey("User.user_id"))    
#     user_id = relationship("UserID", back_populates="user_feedback")
#     subject = Column(String, nullable=False)
#     body = Column(String, nullable=False)
    


    
    
    
    
    
class verification_otps(Base):
    __tablename__ = 'Verify_OTPs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    email = Column(String, ForeignKey("User.email"))
    otp = Column(String, nullable=False)    
    creation_time = Column(DateTime,server_default=text('now()') , nullable=False)
    

# class MediaFiles(Base):
#     __tablename__ = "Media"
    
#     media_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
#     filename = Column(String, nullable=False)
#     size = Column(Float, nullable=False)
#     upload_date = Column(DateTime,server_default=text('now()') , nullable=False)
    
    

    

    