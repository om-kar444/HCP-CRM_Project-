#!/usr/bin/env python3
"""
Test script to verify HCP CRM backend functionality
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test basic health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Health check passed:", response.json())
            return True
        else:
            print("❌ Health check failed:", response.status_code)
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🔍 Testing database connection...")
    try:
        response = requests.get(f"{BASE_URL}/test-db")
        if response.status_code == 200:
            print("✅ Database connection successful:", response.json())
            return True
        else:
            print("❌ Database connection failed:", response.status_code)
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_chat_logging():
    """Test chat-based interaction logging"""
    print("\n🔍 Testing chat interaction logging...")
    payload = {
        "message": "Met Dr. Smith today, discussed OncoBoost efficacy data, positive response, shared Phase III brochure"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/interactions/chat", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat logging successful:", result)
            return result.get("id")
        else:
            print("❌ Chat logging failed:", response.status_code, response.text)
            return None
    except Exception as e:
        print(f"❌ Chat logging error: {e}")
        return None

def test_form_logging():
    """Test form-based interaction logging"""
    print("\n🔍 Testing form interaction logging...")
    payload = {
        "hcp_name": "Dr. Johnson",
        "interaction_type": "Meeting",
        "interaction_date": "2024-04-19",
        "interaction_time": "14:30",
        "attendees": "Dr. Johnson, Sales Rep",
        "topics_discussed": "Product efficacy and safety profile",
        "sentiment": "Positive",
        "outcomes": "Agreed to consider prescribing",
        "follow_up_actions": "Send additional clinical data"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/interactions/form", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Form logging successful:", result)
            return result.get("id")
        else:
            print("❌ Form logging failed:", response.status_code, response.text)
            return None
    except Exception as e:
        print(f"❌ Form logging error: {e}")
        return None

def test_agent_message():
    """Test AI agent message processing"""
    print("\n🔍 Testing AI agent message processing...")
    payload = {
        "message": "Show me follow-up suggestions for Dr. Smith",
        "hcp_name": "Dr. Smith"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/agent/message", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Agent message successful:", result)
            return True
        else:
            print("❌ Agent message failed:", response.status_code, response.text)
            return False
    except Exception as e:
        print(f"❌ Agent message error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting HCP CRM Backend Tests\n")
    
    results = []
    results.append(test_health_check())
    results.append(test_database_connection())
    
    # Only proceed with API tests if basic connectivity works
    if all(results):
        interaction_id = test_chat_logging()
        form_id = test_form_logging()
        results.append(interaction_id is not None)
        results.append(form_id is not None)
        
        # Test agent if we have interactions
        if interaction_id:
            results.append(test_agent_message())
    
    print(f"\n📊 Test Summary: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        print("\n💡 Common issues:")
        print("- Make sure the backend server is running (uvicorn main:app --reload)")
        print("- Check your .env file has correct DATABASE_URL and GROQ_API_KEY")
        print("- Ensure your database is running and accessible")

if __name__ == "__main__":
    main()