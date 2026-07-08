from sqlalchemy.orm import Session
from datetime import datetime
import models


def get_or_create_hcp(db: Session, hcp_name: str):
    if not hcp_name:
        return None
    hcp = db.query(models.HCP).filter(models.HCP.name == hcp_name).first()
    if not hcp:
        hcp = models.HCP(name=hcp_name)
        db.add(hcp)
        db.commit()
        db.refresh(hcp)
    return hcp


def create_interaction_from_chat(db: Session, extracted_data: dict, raw_message: str):
    hcp = get_or_create_hcp(db, extracted_data.get("hcp_name"))
    interaction = models.Interaction(
        hcp_id=hcp.id if hcp else None,
        interaction_type=extracted_data.get("interaction_type"),
        interaction_date=datetime.now().date(),
        interaction_time=datetime.now().time(),
        topics_discussed=extracted_data.get("topics_discussed"),
        sentiment=extracted_data.get("sentiment"),
        outcomes=extracted_data.get("outcomes"),
        follow_up_actions=extracted_data.get("follow_up_actions"),
        logged_via="chat",
        raw_chat_input=raw_message
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


def create_interaction_from_form(db: Session, form_data: dict):
    hcp = get_or_create_hcp(db, form_data.get("hcp_name"))
    interaction = models.Interaction(
        hcp_id=hcp.id if hcp else None,
        interaction_type=form_data.get("interaction_type"),
        interaction_date=form_data.get("interaction_date"),
        interaction_time=form_data.get("interaction_time"),
        attendees=form_data.get("attendees"),
        topics_discussed=form_data.get("topics_discussed"),
        sentiment=form_data.get("sentiment"),
        outcomes=form_data.get("outcomes"),
        follow_up_actions=form_data.get("follow_up_actions"),
        logged_via="form"
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


def get_latest_interaction_by_hcp_name(db: Session, hcp_name: str):
    hcp = db.query(models.HCP).filter(models.HCP.name.ilike(f"%{hcp_name}%")).first()
    if not hcp:
        return None
    return (
        db.query(models.Interaction)
        .filter(models.Interaction.hcp_id == hcp.id)
        .order_by(models.Interaction.created_at.desc())
        .first()
    )


def get_interaction_by_id(db: Session, interaction_id: int):
    return db.query(models.Interaction).filter(models.Interaction.id == interaction_id).first()


def get_all_interactions_by_hcp_name(db: Session, hcp_name: str, limit: int = 5):
    hcp = db.query(models.HCP).filter(models.HCP.name.ilike(f"%{hcp_name}%")).first()
    if not hcp:
        return []
    return (
        db.query(models.Interaction)
        .filter(models.Interaction.hcp_id == hcp.id)
        .order_by(models.Interaction.created_at.desc())
        .limit(limit)
        .all()
    )


def update_interaction(db: Session, interaction, updates: dict):
    for field, value in updates.items():
        if field == "hcp_name":
            hcp = get_or_create_hcp(db, value)
            interaction.hcp_id = hcp.id if hcp else interaction.hcp_id
        elif hasattr(interaction, field):
            setattr(interaction, field, value)
    db.commit()
    db.refresh(interaction)
    return interaction


def save_followup_suggestions(db: Session, interaction_id: int, suggestions: list):
    saved = []
    for text in suggestions:
        s = models.SuggestedFollowup(interaction_id=interaction_id, suggestion_text=text)
        db.add(s)
        saved.append(s)
    db.commit()
    return saved