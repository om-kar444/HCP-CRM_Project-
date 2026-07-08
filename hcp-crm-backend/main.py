from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from agent.tools import log_interaction_tool, edit_interaction_tool
from agent.graph import run_agent
from crud.interaction import create_interaction_from_form
from pydantic import BaseModel
from typing import Optional
from datetime import date, time

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HCP CRM Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    message: str


class EditMessage(BaseModel):
    message: str
    interaction_id: Optional[int] = None
    hcp_name: Optional[str] = None


class AgentMessage(BaseModel):
    message: str
    hcp_name: Optional[str] = None
    interaction_id: Optional[int] = None


class FormInteraction(BaseModel):
    hcp_name: str
    interaction_type: str
    interaction_date: date
    interaction_time: time
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None


@app.get("/")
def root():
    return {"message": "HCP CRM backend running"}


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    hcps = db.query(models.HCP).all()
    return {"hcps_count": len(hcps)}


@app.get("/api/interactions/all")
def get_all_interactions(db: Session = Depends(get_db)):
    # Get interactions with proper ordering and relationship loading
    interactions = db.query(models.Interaction).order_by(models.Interaction.id.desc()).limit(20).all()
    
    return {
        "total_interactions": len(interactions),
        "interactions": [
            {
                "id": i.id,
                "hcp_name": i.hcp.name if i.hcp else "Unknown",
                "interaction_type": i.interaction_type,
                "interaction_date": str(i.interaction_date),
                "topics_discussed": i.topics_discussed,
                "sentiment": i.sentiment,
                "outcomes": i.outcomes,
                "follow_up_actions": i.follow_up_actions,
                "materials_shared": i.materials_shared,
                "samples_distributed": i.samples_distributed,
                "logged_via": i.logged_via,
                "created_at": str(i.created_at)
            } for i in interactions
        ]
    }


@app.post("/api/interactions/chat")
def log_via_chat(payload: ChatMessage, db: Session = Depends(get_db)):
    return log_interaction_tool(payload.message, db)


@app.post("/api/interactions/edit")
def edit_via_chat(payload: EditMessage, db: Session = Depends(get_db)):
    return edit_interaction_tool(
        message=payload.message, db=db,
        interaction_id=payload.interaction_id,
        hcp_name=payload.hcp_name
    )


@app.post("/api/interactions/form")
def log_via_form(payload: FormInteraction, db: Session = Depends(get_db)):
    interaction = create_interaction_from_form(db, payload.dict())
    return {
        "id": interaction.id,
        "interaction_type": interaction.interaction_type,
        "topics_discussed": interaction.topics_discussed,
        "sentiment": interaction.sentiment,
        "logged_via": interaction.logged_via
    }


@app.post("/api/agent/message")
def agent_message(payload: AgentMessage, db: Session = Depends(get_db)):
    return run_agent(
        message=payload.message, db=db,
        hcp_name=payload.hcp_name,
        interaction_id=payload.interaction_id
    )