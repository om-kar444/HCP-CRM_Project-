from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class InteractionFormCreate(BaseModel):
    hcp_name: str
    interaction_type: str
    interaction_date: date
    interaction_time: time
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None

class InteractionChatCreate(BaseModel):
    message: str

class InteractionResponse(BaseModel):
    id: int
    hcp_id: Optional[int]
    interaction_type: Optional[str]
    interaction_date: Optional[date]
    interaction_time: Optional[time]
    attendees: Optional[str]
    topics_discussed: Optional[str]
    sentiment: Optional[str]
    outcomes: Optional[str]
    follow_up_actions: Optional[str]
    logged_via: Optional[str]
    raw_chat_input: Optional[str]

    class Config:
        from_attributes = True