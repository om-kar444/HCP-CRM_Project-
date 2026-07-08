from sqlalchemy.orm import Session
from agent.llm import (
    extract_interaction_data,
    extract_edit_data,
    generate_followup_suggestions,
    check_compliance,
    summarize_history
)
from crud.interaction import (
    create_interaction_from_chat,
    get_latest_interaction_by_hcp_name,
    get_interaction_by_id,
    get_all_interactions_by_hcp_name,
    update_interaction,
    save_followup_suggestions
)


def log_interaction_tool(message: str, db: Session) -> dict:
    extracted_data = extract_interaction_data(message)
    interaction = create_interaction_from_chat(db, extracted_data, message)

    return {
        "id": interaction.id,
        "hcp_name": extracted_data.get("hcp_name"),
        "interaction_type": interaction.interaction_type,
        "topics_discussed": interaction.topics_discussed,
        "sentiment": interaction.sentiment,
        "materials_shared": extracted_data.get("materials_shared"),
        "outcomes": interaction.outcomes,
        "follow_up_actions": interaction.follow_up_actions,
    }


def edit_interaction_tool(message: str, db: Session, interaction_id: int = None, hcp_name: str = None) -> dict:
    if interaction_id:
        interaction = get_interaction_by_id(db, interaction_id)
    elif hcp_name:
        interaction = get_latest_interaction_by_hcp_name(db, hcp_name)
    else:
        return {"error": "No interaction_id or hcp_name provided to identify which interaction to edit."}

    if not interaction:
        return {"error": "No matching interaction found to edit."}

    updates = extract_edit_data(message)
    if not updates:
        return {"error": "Could not determine what to update from the message."}

    updated_interaction = update_interaction(db, interaction, updates)

    return {
        "id": updated_interaction.id,
        "interaction_type": updated_interaction.interaction_type,
        "topics_discussed": updated_interaction.topics_discussed,
        "sentiment": updated_interaction.sentiment,
        "outcomes": updated_interaction.outcomes,
        "follow_up_actions": updated_interaction.follow_up_actions,
        "updated_fields": list(updates.keys())
    }


def fetch_hcp_history_tool(db: Session, hcp_name: str) -> dict:
    if not hcp_name:
        return {"error": "No hcp_name provided."}

    interactions = get_all_interactions_by_hcp_name(db, hcp_name)
    if not interactions:
        return {"error": f"No interaction history found for {hcp_name}."}

    history_lines = []
    for i in interactions:
        history_lines.append(
            f"Date: {i.interaction_date}, Type: {i.interaction_type}, "
            f"Topics: {i.topics_discussed}, Sentiment: {i.sentiment}, Outcome: {i.outcomes}"
        )
    history_text = "\n".join(history_lines)

    summary = summarize_history(history_text)

    return {
        "hcp_name": hcp_name,
        "total_interactions": len(interactions),
        "summary": summary,
        "records": [
            {
                "id": i.id,
                "date": str(i.interaction_date),
                "interaction_type": i.interaction_type,
                "topics_discussed": i.topics_discussed,
                "sentiment": i.sentiment,
                "outcomes": i.outcomes
            } for i in interactions
        ]
    }


def suggest_followup_tool(db: Session, interaction_id: int = None, hcp_name: str = None) -> dict:
    if interaction_id:
        interaction = get_interaction_by_id(db, interaction_id)
    elif hcp_name:
        interaction = get_latest_interaction_by_hcp_name(db, hcp_name)
    else:
        return {"error": "No interaction_id or hcp_name provided."}

    if not interaction:
        return {"error": "No matching interaction found."}

    summary = (
        f"Interaction type: {interaction.interaction_type}, "
        f"Topics: {interaction.topics_discussed}, "
        f"Sentiment: {interaction.sentiment}, "
        f"Outcome: {interaction.outcomes}"
    )

    suggestions = generate_followup_suggestions(summary)
    save_followup_suggestions(db, interaction.id, suggestions)

    return {
        "interaction_id": interaction.id,
        "suggestions": suggestions
    }


def compliance_check_tool(message: str) -> dict:
    result = check_compliance(message)
    return result