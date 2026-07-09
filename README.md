# HCP CRM — AI-First CRM for Pharmaceutical Field Representatives

An AI-first Customer Relationship Management (CRM) system built for pharmaceutical field representatives to log, edit, and manage their interactions with Healthcare Professionals (HCPs). The system offers **two ways to log an interaction** — a traditional structured form and a natural-language chat interface — both backed by the same LangGraph AI agent.

---

<img width="1912" height="921" alt="Screenshot 2026-07-09 161052 - Copy" src="https://github.com/user-attachments/assets/b2af7e55-74a7-4668-a0b2-bc70a816070c" />
<img width="1912" height="921" alt="Screenshot 2026-07-09 161052" src="https://github.com/user-attachments/assets/d347317a-b2be-422b-b071-f203b5604e99" />
<img width="446" height="641" alt="Screenshot 2026-07-09 161122" src="https://github.com/user-attachments/assets/f2e324c0-068d-4bf3-baa4-4d39950ca3f2" />
<img width="1886" height="903" alt="Screenshot 2026-07-09 161136 - Copy" src="https://github.com/user-attachments/assets/72555add-4e67-4239-a797-be83f540c22d" />
<img width="1886" height="903" alt="Screenshot 2026-07-09 161136" src="https://github.com/user-attachments/assets/94834083-3bd7-45bc-850f-f4c769002e7e" />
<img width="537" height="136" alt="Screenshot 2026-07-09 161145" src="https://github.com/user-attachments/assets/0bfcd8a1-b4a9-48ee-8a1d-9528d8e3d317" />
<img width="426" height="490" alt="Screenshot 2026-07-09 161209" src="https://github.com/user-attachments/assets/19476438-5354-4821-94e1-ab363b93052d" />
<img width="1852" height="892" alt="Screenshot 2026-07-09 161347" src="https://github.com/user-attachments/assets/282bb47c-3562-4c5c-8a29-de2499317ee3" />
<img width="853" height="307" alt="Screenshot 2026-07-09 161426" src="https://github.com/user-attachments/assets/ff32e85e-df47-41f0-9fc5-b5150def0b6d" />
<img width="907" height="317" alt="Screenshot 2026-07-09 161537 - Copy" src="https://github.com/user-attachments/assets/5bc7e949-dae5-4d69-8181-39859de94992" />
<img width="987" height="215" alt="Screenshot 2026-07-09 161550 - Copy" src="https://github.com/user-attachments/assets/7ccaf8db-0e22-4a1c-9134-95c34a202831" />
<img width="1908" height="672" alt="Screenshot 2026-07-09 161608 - Copy" src="https://github.com/user-attachments/assets/3a355df3-02fc-461b-bd86-0537ea5d7744" />
<img width="1917" height="648" alt="Screenshot 2026-07-09 161630" src="https://github.com/user-attachments/assets/c22ab11c-2ae6-4a46-adb4-cbdbb5abeeab" />















## 1. Problem This Solves

Field reps typically spend a large chunk of their day manually filling CRM forms after every doctor visit. This project explores an "AI-first" alternative: a rep can simply describe the visit in plain English (or use the form), and a LangGraph agent extracts structured data, checks compliance, suggests follow-ups, and keeps the HCP's history up to date — reducing admin time so reps can focus on the actual customer relationship.

---

## 2. System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│ FRONTEND — React + Redux Toolkit                                    │
│                                                                      │
│   [ Structured Form UI ]        [ AI Chat Panel ]                   │
└────────────────────────────────────────────────────────────────────┘
                                  │
                           REST API calls
                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│ BACKEND — FastAPI                                                    │
│                                                                      │
│   POST /api/interactions/form                                       │
│   POST /api/interactions/chat                                       │
│   POST /api/interactions/edit                                       │
│   POST /api/agent/message                                           │
└────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│ LANGGRAPH AI AGENT                                                   │
│                                                                      │
│                       Intent Classifier Node                        │
│                                                                      │
│   1. Log Interaction     → extract & create record                  │
│   2. Edit Interaction    → modify existing record                   │
│   3. Fetch HCP History   → summarize past visits                    │
│   4. Suggest Followup    → recommend next actions                   │
│   5. Compliance Check    → validate messaging                       │
└────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│ GROQ LLM LAYER                                                       │
│                                                                      │
│   gemma2-9b-it (primary — fast extraction)                          │
│   llama-3.3-70b-versatile (fallback — complex reasoning)            │
└────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│ DATABASE — MySQL / PostgreSQL (SQLAlchemy ORM)                       │
│                                                                      │
│   hcps · interactions · materials · samples ·                       │
│   suggested_followups · interaction_materials ·                     │
│   interaction_samples                                               │
└────────────────────────────────────────────────────────────────────┘
```

### Request flow (chat-based logging example)

1. Rep types a free-text message in the AI Chat Panel — e.g. *"Met Dr. Smith today, discussed OncoBoost efficacy, positive response, shared Phase III brochure."*
2. React/Redux dispatches the message to `POST /api/agent/message`.
3. FastAPI hands the message to the **LangGraph agent**.
4. The **Intent Classifier Node** decides which of the 5 tools should handle it.
5. The selected tool calls the **Groq LLM** (`gemma2-9b-it`, or `llama-3.3-70b-versatile` for heavier reasoning) to extract structured fields or generate a response.
6. The tool performs the DB operation via SQLAlchemy — create/update HCP, interaction, or follow-up.
7. A structured JSON response, plus a human-readable summary, is returned to the frontend.
8. Redux updates, and both the chat log and form fields reflect the new state instantly.

---

## 3. Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite recommended, CRA also supported), Redux Toolkit, Google Inter font |
| Backend | Python, FastAPI |
| AI Agent Framework | LangGraph |
| LLM Provider | Groq — `gemma2-9b-it` (primary), `llama-3.3-70b-versatile` (context/fallback) |
| Database | SQLAlchemy ORM — MySQL or PostgreSQL |
| State Management | Redux Toolkit |

---

## 4. The LangGraph Agent & Its 5 Tools

The LangGraph agent is the "brain" of the HCP module. Every message — whether typed into the chat panel or triggered by a form action like "Get AI Suggestions" — is routed through a single graph that classifies intent and dispatches to the right tool. This keeps all AI reasoning in one place instead of scattering LLM calls across the codebase, and makes it easy to add new tools later (e.g. voice-note summarization).

### Graph workflow

```
User message
     │
     ▼
Intent Classifier Node
     │
     ├── log        → Log Interaction Tool         ─┐
     ├── edit        → Edit Interaction Tool        ─┤
     ├── history    → Fetch HCP History Tool         ─┼──►  Structured JSON + chat reply
     ├── followup  → Suggest Followup Tool          ─┤
     └── compliance → Compliance Check Tool          ─┘
```

(See the architecture diagram above for the visual version of this same flow.)

### Tool 1 — Log Interaction Tool
**Purpose:** Convert an unstructured, natural-language description of a visit into a structured `Interaction` record.

- Takes the rep's raw text (e.g. *"Met Dr. Rajesh Kumar at Apollo Hospital, discussed OncoBoost Phase III results, very positive response, shared clinical trial brochure and gave 3 sample packs"*).
- Sends it to the Groq LLM with a prompt instructing it to extract: `hcp_name`, `interaction_type`, `topics_discussed`, `sentiment`, `materials_shared`, `samples_distributed`, `outcomes`, `follow_up_actions`.
- Performs **entity resolution**: checks if the HCP already exists (fuzzy match on name); creates a new `hcps` row if not.
- Writes a new row to `interactions`, linking `hcp_id`, and stores the original text in `raw_chat_input` with `logged_via = 'chat'`.
- Returns the structured JSON back to the UI so the form fields auto-populate alongside the chat confirmation.

### Tool 2 — Edit Interaction Tool
**Purpose:** Modify a previously logged interaction using a follow-up chat command, without the rep needing to reopen the form.

- Parses commands like *"Change the last interaction sentiment to neutral and add that we scheduled a follow-up meeting next Tuesday."*
- Resolves **which interaction** is being referenced (most recent by default, or by HCP name / date if specified).
- Uses the LLM to map the instruction to specific column updates (e.g. `sentiment`, `follow_up_actions`).
- Performs a partial `UPDATE` on the `interactions` row (only touching the fields mentioned) and bumps `updated_at`.
- Returns a JSON diff — `updated_fields` — plus the full updated record, so the UI can highlight exactly what changed.

### Tool 3 — Fetch HCP History Tool
**Purpose:** Retrieve and summarize a specific HCP's past interactions on demand (e.g. *"Show me history with Dr. Johnson"*).

- Looks up the HCP by name (fuzzy match).
- Queries all related `interactions` rows, ordered by date.
- Passes the raw history to the LLM to produce a short natural-language summary (recent sentiment trend, last topics discussed, outstanding follow-ups) alongside the raw list for the UI.

### Tool 4 — Suggest Followup Tool
**Purpose:** Generate AI-recommended next steps for a given interaction (powers the "Get AI Suggestions" button and the *"What should I follow up on?"* chat command).

- Takes the interaction's `topics_discussed`, `sentiment`, and `outcomes` as context.
- Prompts the LLM to propose 2–4 concrete follow-up actions (e.g. send a trial summary, schedule a call, invite to a speaker program).
- Persists each suggestion to `suggested_followups` (linked via `interaction_id`) with `accepted = false` by default.
- Rep can accept a suggestion from the UI, which flips `accepted = true` and optionally copies it into `follow_up_actions`.

### Tool 5 — Compliance Check Tool
**Purpose:** Validate that a rep's proposed message or claim is compliant with pharmaceutical marketing regulations before it's used with an HCP (e.g. *"Is it okay to say our drug cures cancer?"*).

- Sends the proposed statement to the LLM with a compliance-focused system prompt covering common regulatory red flags (unapproved claims, off-label promotion, missing safety information, absolute/superlative language).
- Returns a verdict (`compliant` / `non-compliant` / `needs revision`) with a plain-language explanation and, where possible, a compliant rewording.
- This tool does not write to the database — it's an advisory check, though flagged interactions could optionally be logged for audit purposes.

> Note: `llama-3.3-70b-versatile` is used as a fallback for tools that benefit from stronger reasoning (e.g. Compliance Check, or ambiguous Edit commands), while `gemma2-9b-it` handles the higher-volume, lower-latency extraction tasks (Log, History, Followup).

---

## 5. Database Schema

```sql
CREATE DATABASE IF NOT EXISTS hcp_crm;
USE hcp_crm;

-- 1. HCPs
CREATE TABLE hcps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    specialty VARCHAR(100),
    hospital VARCHAR(255),
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Interactions
CREATE TABLE interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hcp_id INT,
    interaction_type VARCHAR(50),
    interaction_date DATE,
    interaction_time TIME,
    attendees TEXT,
    topics_discussed TEXT,
    sentiment VARCHAR(20),
    outcomes TEXT,
    follow_up_actions TEXT,
    logged_via VARCHAR(20) DEFAULT 'form',
    raw_chat_input TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    materials_shared VARCHAR(255),
    samples_distributed VARCHAR(255),
    FOREIGN KEY (hcp_id) REFERENCES hcps(id)
);

-- 3. Materials
CREATE TABLE materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100)
);

-- 4. Samples
CREATE TABLE samples (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL
);

-- 5. Suggested Followups
CREATE TABLE suggested_followups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interaction_id INT,
    suggestion_text TEXT,
    accepted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (interaction_id) REFERENCES interactions(id)
);

-- 6. Interaction <-> Materials (junction)
CREATE TABLE interaction_materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interaction_id INT,
    material_id INT,
    FOREIGN KEY (interaction_id) REFERENCES interactions(id),
    FOREIGN KEY (material_id) REFERENCES materials(id)
);

-- 7. Interaction <-> Samples (junction)
CREATE TABLE interaction_samples (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interaction_id INT,
    sample_id INT,
    FOREIGN KEY (interaction_id) REFERENCES interactions(id),
    FOREIGN KEY (sample_id) REFERENCES samples(id)
);
```

**Relationships:** one `hcp` has many `interactions` → each `interaction` can generate many `suggested_followups`, and links to any number of `materials` / `samples` via the two junction tables.

---

## 6. Project Structure

```
├── hcp-crm-backend/            # FastAPI Python backend
│   ├── agent/                  # LangGraph AI agent implementation
│   │   ├── graph.py            # Agent workflow, intent classifier, routing
│   │   ├── llm.py              # Groq LLM integration (gemma2-9b-it / llama-3.3-70b)
│   │   └── tools.py            # 5 core AI tools
│   ├── crud/                   # Database operations
│   ├── routers/                # FastAPI route definitions
│   ├── models.py                # SQLAlchemy database models
│   ├── schemas.py               # Pydantic request/response schemas
│   ├── database.py              # DB engine/session setup
│   ├── main.py                  # FastAPI application entrypoint
│   ├── migrate_db.py            # DB migration helper
│   ├── test_gorq.py             # Groq API connectivity test script
│   ├── .env.example             # Environment variable template
│   └── requirements.txt         # Python dependencies
│
├── hcp-crm-vite/                # React (Vite) frontend — RECOMMENDED
│   ├── src/
│   │   ├── components/          # React components (form + chat UI)
│   │   ├── store/                # Redux store and slices
│   │   └── App.jsx               # Main application
│   ├── vite.config.js
│   └── package.json
│
├── hcp-crm-frontend/            # React (Create React App) frontend — alternative
│   ├── src/
│   │   ├── components/
│   │   ├── store/
│   │   └── App.js
│   └── package.json
│
├── check_db.py                  # Quick DB connectivity/sanity check script
├── start_backend.py             # Backend startup helper
├── start_vite_frontend.js       # Frontend startup helper
└── README.md
```

---

## 7. Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL or PostgreSQL server running locally
- A Groq API key ([console.groq.com](https://console.groq.com))

### Environment Configuration

Create a `.env` file inside `hcp-crm-backend/`:

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/hcp_crm
GROQ_API_KEY=your_groq_api_key_here
```

> Never commit your real `.env` file. Only `.env.example` (with placeholder values) should be pushed to GitHub — `.env` should be listed in `.gitignore`.

---

### 🖥️ Backend Setup & Run

```bash
# Navigate to backend
cd hcp-crm-backend

# Install dependencies (first time only)
pip install -r requirements.txt

# Run backend
python -m uvicorn main:app --reload --port 8000
```

Backend will run on: **http://localhost:8000**

---

### 🎨 Frontend Setup & Run

Open a **new terminal window**, then:

```bash
# Navigate to frontend
cd hcp-crm-vite

# Install dependencies (first time only)
npm install

# Run frontend
npm run dev
```

Frontend will run on: **http://localhost:3000**

---

### 📊 Database Setup

```bash
# Login to MySQL
mysql -u root -p

# Run the database queries from db.txt or:
source hcp-crm-backend/db.txt
```

---

### ⚡ Quick Start (All in One)

**Terminal 1 — Backend:**
```bash
cd C:\Users\omkar\OneDrive\Desktop\crm_hcp\hcp-crm-backend
python -m uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd C:\Users\omkar\OneDrive\Desktop\crm_hcp\hcp-crm-vite
npm run dev
```

Then open **http://localhost:3000** in your browser! 🎯

---

### ✅ Verify Everything is Running

```bash
# Check backend
curl http://localhost:8000

# Check frontend
# Just open http://localhost:3000 in browser
```

That's it — both services should now be running! 🚀

---

### Running Both Services — Summary

| Service | URL |
|---|---|
| Backend (FastAPI) | `http://localhost:8000` |
| Frontend (Vite) | `http://localhost:3000` |
| Frontend (CRA) | `http://localhost:3001` |

---

## 8. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/interactions/form` | Log interaction via structured form |
| POST | `/api/interactions/chat` | Log interaction via natural language |
| POST | `/api/interactions/edit` | Edit an existing interaction via chat |
| POST | `/api/agent/message` | Send any message to the LangGraph agent (auto-routes to the right tool) |
| GET | `/test-db` | Test database connectivity |

---

## 9. Usage Examples

### Chat Interface
- **Log:** *"Met Dr. Smith today, discussed OncoBoost efficacy, positive response, shared Phase III brochure"*
- **Edit:** *"Change the last interaction sentiment to negative"*
- **History:** *"Show me history with Dr. Johnson"*
- **Suggestions:** *"What should I follow up on for the last meeting?"*
- **Compliance:** *"Is it okay to say our drug cures cancer?"*

### Form Interface
- Fill structured fields: HCP name, interaction type, date/time, attendees, topics discussed, sentiment, outcomes.
- Add materials shared / samples distributed.
- Click **"Get AI Suggestions"** to have the Suggest Followup Tool propose next steps.
- Optionally use **"Summarize from Voice Note"** to transcribe/summarize a recorded visit note into the Topics Discussed field.

---

## 10. Verifying Your Data — Useful SQL Queries

These queries are handy for sanity-checking that logging, editing, and follow-up suggestions are actually persisting correctly during a demo or testing session.

**Quick summary (row counts):**
```sql
SELECT 'HCPs' as table_name, COUNT(*) as count FROM hcps
UNION ALL
SELECT 'Interactions', COUNT(*) FROM interactions
UNION ALL
SELECT 'Suggestions', COUNT(*) FROM suggested_followups;
```

**View all HCPs:**
```sql
SELECT * FROM hcps ORDER BY created_at DESC;
```

**View all interactions with HCP names:**
```sql
SELECT 
    i.id,
    h.name as hcp_name,
    i.interaction_type,
    i.interaction_date,
    i.interaction_time,
    i.sentiment,
    i.topics_discussed,
    i.outcomes,
    i.follow_up_actions,
    i.logged_via,
    i.created_at
FROM interactions i
LEFT JOIN hcps h ON i.hcp_id = h.id
ORDER BY i.created_at DESC;
```

**View AI-generated follow-up suggestions:**
```sql
SELECT 
    sf.id,
    h.name as hcp_name,
    sf.suggestion_text,
    sf.accepted,
    i.interaction_type,
    i.created_at
FROM suggested_followups sf
JOIN interactions i ON sf.interaction_id = i.id
LEFT JOIN hcps h ON i.hcp_id = h.id
ORDER BY sf.id DESC;
```

**Latest 5 interactions (detailed):**
```sql
SELECT 
    i.id,
    h.name as hcp_name,
    i.interaction_type,
    i.sentiment,
    i.topics_discussed,
    i.materials_shared,
    i.samples_distributed,
    i.logged_via,
    i.raw_chat_input,
    i.created_at
FROM interactions i
LEFT JOIN hcps h ON i.hcp_id = h.id
ORDER BY i.created_at DESC
LIMIT 5;
```

---

## 11. Demo Video Checklist

For the assignment demo (10–15 minutes), cover:
1. Frontend walkthrough — both the structured form and the AI chat interface.
2. All 5 LangGraph tools demonstrated live (Log, Edit, History, Followup, Compliance).
3. A brief explanation of the code structure (agent graph, tools, routers, models).
4. A short summary of your understanding of the task.

---

## 12. Development Notes

- Uses Google Inter font for typography across the UI.
- Redux Toolkit manages reactive state for both the form and chat panels.
- Real-time chat interface with loading/typing indicators.
- Structured error handling and user-facing feedback on both API and UI layers.
- Compliance-focused design choices throughout, given the pharma industry context.

## 13. Future Enhancements

- Voice note integration (native audio capture → transcription → summarization).
- Advanced search and filtering across HCPs and interactions.
- Analytics dashboard (sentiment trends, rep activity, follow-up conversion rate).
- Mobile-responsive design.
- Multi-language support.
- Advanced, configurable compliance rules engine.
