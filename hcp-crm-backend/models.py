from sqlalchemy import Column, Integer, String, Text, Date, Time, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class HCP(Base):
    __tablename__ = "hcps"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    specialty = Column(String(100))
    hospital = Column(String(255))
    city = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationship
    interactions = relationship("Interaction", back_populates="hcp")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"))
    interaction_type = Column(String(50))
    interaction_date = Column(Date)
    interaction_time = Column(Time)
    attendees = Column(Text)
    topics_discussed = Column(Text)
    sentiment = Column(String(20))
    outcomes = Column(Text)
    follow_up_actions = Column(Text)
    materials_shared = Column(Text)  # Added this field
    samples_distributed = Column(Text)  # Added this field
    logged_via = Column(String(20), default="form")
    raw_chat_input = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationship
    hcp = relationship("HCP", back_populates="interactions")

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100))

class Sample(Base):
    __tablename__ = "samples"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), nullable=False)

class SuggestedFollowup(Base):
    __tablename__ = "suggested_followups"
    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"))
    suggestion_text = Column(Text)
    accepted = Column(Boolean, default=False)