#!/usr/bin/env python3
"""
Database viewer for HCP CRM - Check logged interactions
"""
import sys
import os
sys.path.append('hcp-crm-backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime

# Load environment
load_dotenv('hcp-crm-backend/.env')

# Import models
from hcp_crm_backend.models import HCP, Interaction, SuggestedFollowup
from hcp_crm_backend.database import Base

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def view_hcps():
    """View all HCPs in database"""
    db = SessionLocal()
    try:
        hcps = db.query(HCP).all()
        print(f"\n📋 HCPs in Database ({len(hcps)} total):")
        print("-" * 60)
        for hcp in hcps:
            print(f"ID: {hcp.id} | Name: {hcp.name} | Specialty: {hcp.specialty or 'N/A'}")
            print(f"Hospital: {hcp.hospital or 'N/A'} | City: {hcp.city or 'N/A'}")
            print(f"Created: {hcp.created_at}")
            print("-" * 60)
    finally:
        db.close()

def view_interactions(limit=10):
    """View recent interactions"""
    db = SessionLocal()
    try:
        interactions = (
            db.query(Interaction, HCP)
            .join(HCP, Interaction.hcp_id == HCP.id, isouter=True)
            .order_by(Interaction.created_at.desc())
            .limit(limit)
            .all()
        )
        
        print(f"\n💬 Recent Interactions ({len(interactions)} shown):")
        print("=" * 80)
        
        for interaction, hcp in interactions:
            print(f"\n🆔 ID: {interaction.id}")
            print(f"👤 HCP: {hcp.name if hcp else 'Unknown'}")
            print(f"📅 Date: {interaction.interaction_date} at {interaction.interaction_time}")
            print(f"📞 Type: {interaction.interaction_type}")
            print(f"😊 Sentiment: {interaction.sentiment}")
            print(f"💭 Topics: {interaction.topics_discussed or 'N/A'}")
            print(f"🎯 Outcomes: {interaction.outcomes or 'N/A'}")
            print(f"📝 Follow-ups: {interaction.follow_up_actions or 'N/A'}")
            print(f"📱 Logged via: {interaction.logged_via}")
            if interaction.raw_chat_input:
                print(f"🗨️ Chat input: {interaction.raw_chat_input}")
            print(f"⏰ Created: {interaction.created_at}")
            print("-" * 80)
            
    finally:
        db.close()

def view_suggestions():
    """View AI suggestions"""
    db = SessionLocal()
    try:
        suggestions = (
            db.query(SuggestedFollowup, Interaction, HCP)
            .join(Interaction, SuggestedFollowup.interaction_id == Interaction.id)
            .join(HCP, Interaction.hcp_id == HCP.id, isouter=True)
            .order_by(SuggestedFollowup.id.desc())
            .limit(20)
            .all()
        )
        
        print(f"\n💡 AI Suggestions ({len(suggestions)} shown):")
        print("=" * 80)
        
        for suggestion, interaction, hcp in suggestions:
            print(f"🆔 Suggestion ID: {suggestion.id}")
            print(f"👤 For HCP: {hcp.name if hcp else 'Unknown'}")
            print(f"📝 Suggestion: {suggestion.suggestion_text}")
            print(f"✅ Accepted: {suggestion.accepted}")
            print(f"🔗 Interaction ID: {interaction.id}")
            print("-" * 40)
            
    finally:
        db.close()

def search_hcp(name):
    """Search for specific HCP"""
    db = SessionLocal()
    try:
        hcp = db.query(HCP).filter(HCP.name.ilike(f"%{name}%")).first()
        if hcp:
            print(f"\n🔍 Found HCP: {hcp.name}")
            interactions = (
                db.query(Interaction)
                .filter(Interaction.hcp_id == hcp.id)
                .order_by(Interaction.created_at.desc())
                .all()
            )
            print(f"📊 Total interactions: {len(interactions)}")
            
            for interaction in interactions:
                print(f"\n📅 {interaction.interaction_date} - {interaction.interaction_type}")
                print(f"😊 Sentiment: {interaction.sentiment}")
                print(f"💭 Topics: {interaction.topics_discussed or 'N/A'}")
        else:
            print(f"\n❌ No HCP found with name containing '{name}'")
    finally:
        db.close()

def main():
    """Main function"""
    print("🏥 HCP CRM Database Viewer")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "hcps":
            view_hcps()
        elif command == "interactions":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            view_interactions(limit)
        elif command == "suggestions":
            view_suggestions()
        elif command == "search":
            if len(sys.argv) > 2:
                search_hcp(sys.argv[2])
            else:
                print("❌ Please provide HCP name to search")
        else:
            print("❌ Unknown command")
            print_help()
    else:
        # Show everything by default
        view_hcps()
        view_interactions(5)
        view_suggestions()

def print_help():
    """Print help message"""
    print("\n📖 Usage:")
    print("python check_db.py                    # View all data")
    print("python check_db.py hcps              # View all HCPs")
    print("python check_db.py interactions [N]  # View N recent interactions")
    print("python check_db.py suggestions       # View AI suggestions")
    print("python check_db.py search [name]     # Search for HCP by name")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure:")
        print("- Backend server is running")
        print("- Database is accessible")
        print("- .env file has correct DATABASE_URL")