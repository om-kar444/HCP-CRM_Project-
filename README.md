# HCP CRM - Healthcare Professional Customer Relationship Management

An AI-first CRM system for pharmaceutical field representatives to log and manage interactions with Healthcare Professionals (HCPs).

## Tech Stack

- **Frontend**: React with Redux Toolkit, Google Inter font
- **Backend**: Python FastAPI
- **AI Framework**: LangGraph with Groq LLM (gemma2-9b-it model)
- **Database**: SQLAlchemy with PostgreSQL/MySQL support
- **State Management**: Redux Toolkit

## Features

### Dual Interface Logging
- **Form-based**: Traditional structured form for detailed interaction logging
- **Chat-based**: Conversational AI interface for natural language interaction logging

### AI-Powered Tools (LangGraph Agent)
1. **Log Interaction Tool**: Extract structured data from natural language descriptions
2. **Edit Interaction Tool**: Modify previously logged interactions via chat commands
3. **Fetch HCP History Tool**: Retrieve and summarize past interactions with specific HCPs
4. **Suggest Followup Tool**: AI-generated follow-up recommendations based on interaction context
5. **Compliance Check Tool**: Validate messages for pharmaceutical marketing compliance

### Key Capabilities
- Entity extraction and sentiment analysis
- Automatic HCP record creation and management
- Follow-up suggestion generation
- Compliance validation for pharma industry
- Real-time chat interface with AI assistant
- Complete CRUD operations for interactions

## Project Structure

```
├── hcp-crm-backend/           # FastAPI Python backend
│   ├── agent/                 # LangGraph AI agent implementation
│   │   ├── graph.py          # Agent workflow and routing
│   │   ├── llm.py            # Groq LLM integration
│   │   └── tools.py          # 5 core AI tools
│   ├── crud/                 # Database operations
│   ├── models.py             # SQLAlchemy database models
│   ├── main.py               # FastAPI application
│   └── requirements.txt      # Python dependencies
├── hcp-crm-frontend/         # React (Create React App) frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── store/            # Redux store and slices
│   │   └── App.js            # Main application
│   └── package.json          # Node.js dependencies
├── hcp-crm-vite/             # React (Vite) frontend - RECOMMENDED
│   ├── src/
│   │   ├── components/       # React components (JSX)
│   │   ├── store/            # Redux store and slices
│   │   └── App.jsx           # Main application
│   ├── vite.config.js        # Vite configuration
│   └── package.json          # Node.js dependencies
└── README.md
```

## Frontend Options

### Option 1: Vite Frontend (Recommended - Faster Development)
```bash
cd hcp-crm-vite
npm install
npm run dev
```

### Option 2: Create React App Frontend
```bash
cd hcp-crm-frontend  
npm install
npm start
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL or MySQL database
- Groq API key

### Environment Configuration

1. Create `.env` file in `hcp-crm-backend/`:
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/hcp_crm
GROQ_API_KEY=your_groq_api_key_here
```

### Backend Setup

1. **Install dependencies**:
```bash
cd hcp-crm-backend
pip install -r requirements.txt
```

2. **Start the backend**:
```bash
python -m uvicorn main:app --reload --port 8000
```

Or use the startup script:
```bash
python start_backend.py
```

### Frontend Setup (Vite - Recommended)

1. **Install dependencies**:
```bash
cd hcp-crm-vite
npm install
```

2. **Start the frontend**:
```bash
npm run dev
```

Or use the startup script:
```bash
node start_vite_frontend.js
```

### Quick Start (Both Services)

Backend will run on: `http://localhost:8000`
Frontend will run on: `http://localhost:3000` (Vite) or `http://localhost:3001` (CRA)

## API Endpoints

- `POST /api/interactions/chat` - Log interaction via natural language
- `POST /api/interactions/form` - Log interaction via structured form
- `POST /api/interactions/edit` - Edit existing interaction via chat
- `POST /api/agent/message` - Send message to AI agent for processing
- `GET /test-db` - Test database connectivity

## Usage Examples

### Chat Interface Examples:
- **Log**: "Met Dr. Smith today, discussed OncoBoost efficacy, positive response, shared Phase III brochure"
- **Edit**: "Change the sentiment to negative for the last Dr. Smith interaction"
- **History**: "Show me history with Dr. Johnson"
- **Suggestions**: "What should I follow up on for the last meeting?"
- **Compliance**: "Is it okay to say our drug cures cancer?"

### Form Interface:
- Fill out structured fields for detailed interaction logging
- Select sentiment, interaction type, date/time
- Add attendees, topics, outcomes, and follow-up actions

## LangGraph Agent Workflow

The AI agent uses intent classification to route messages to appropriate tools:
1. **Classify** user intent (log, edit, history, followup, compliance)
2. **Route** to appropriate tool based on classification
3. **Execute** tool with relevant parameters
4. **Return** structured response to frontend

## Database Schema

- **HCPs**: Healthcare professional records
- **Interactions**: Logged interactions with HCPs
- **Materials**: Marketing materials shared
- **Samples**: Product samples distributed
- **SuggestedFollowups**: AI-generated follow-up recommendations

## Development Notes

- Uses Google Inter font for typography
- Redux state management for reactive UI updates
- Real-time chat interface with loading states
- Error handling and user feedback
- Responsive design following GitHub's design language
- Compliance-focused features for pharmaceutical industry

## Demo Requirements

For the assignment demo video (10-15 minutes), showcase:
1. Frontend walkthrough (both form and chat interfaces)
2. All 5 LangGraph tools working
3. Code structure explanation
4. Task understanding summary

## Future Enhancements

- Voice note integration
- Advanced search and filtering
- Analytics dashboard
- Mobile-responsive design
- Multi-language support
- Advanced compliance rules engine