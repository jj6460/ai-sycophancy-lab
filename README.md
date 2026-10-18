# AI Sycophancy Lab

A psychology research platform for studying AI sycophancy behaviors in controlled experimental settings.

## About This Project

This project implements a web-based experiment platform for psychology research on AI "sycophancy" - where AI systems may excessively agree with, flatter, or validate users beyond what is warranted. The platform enables researchers to:

- Conduct controlled experiments with different AI manipulation strategies
- Collect reproducible data for psychology research
- Test five experimental conditions (C0-C4) representing different sycophancy approaches

**Important Notes:**
- This is a research tool, not a production chatbot
- The system implements manipulation strategies for research purposes only
- Actual effects on participants must be validated through proper psychological pre-experiments
- No strategy has been proven to effectively manipulate real participants

## What This Project Does

### Core Features

- **Chat Interface**: Web-based interface for participants to interact with AI
- **Five Experimental Conditions**: 
  - C0: Neutral baseline (balanced, polite advice)
  - C1: Semantic/stance manipulation (validates user preferences)
  - C2: Response structure manipulation (controlled response format)
  - C3: Goal-directed instructions (engagement-focused)
  - C4: Dynamic trigger (context-sensitive activation)
- **Backend API**: Complete REST API for session management and data collection
- **LLM Support**: 
  - Mock LLM Mode: Offline demonstration without real AI API keys
  - DeepSeek Integration: Real LLM support with configurable API
  - Extensible: Easy to add OpenAI, Azure, or other providers
- **Data Export**: Anonymous experiment data export for analysis
- **Strategy System**: Modular, extensible strategy architecture

### What It Does NOT Do

- No model fine-tuning or reinforcement learning
- No real purchases or payments
- No dynamic manipulation intensity upgrades based on user behavior
- No automated ethics approval or real participant recruitment
- No multi-tenant researcher dashboard
- No production-grade identity system

## Installation

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or pnpm package manager

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment configuration:
```bash
cp ../.env.example .env
```

5. Edit `.env` and configure:
```
LLM_PROVIDER=mock  # Use 'mock' for testing, 'deepseek' for real LLM
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### Start Frontend Server

```bash
cd frontend
npm run dev
```

The frontend will be available at: http://localhost:3000

### Quick Test

1. Open http://localhost:3000 in your browser
2. A session will be created automatically
3. Send messages to the AI
4. Observe responses based on the assigned condition
5. Click "End Session" when finished

## Configuration

### Switching Between Mock and Real LLM

**Mock Mode (Default):**
```env
LLM_PROVIDER=mock
```

**DeepSeek Mode (Real LLM):**
```env
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your-deepseek-api-key-here
DEEPSEEK_MODEL=deepseek-chat
```

**OpenAI Mode:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

### Testing Different Conditions

In development mode, you can specify the condition in the frontend code:

```typescript
// In App.tsx, modify createSession call:
await apiClient.createSession({
  study_id: 'study4_pilot',
  test_mode: true,
  condition: 'C1',  // Change to C0, C1, C2, C3, C4
});
```

Or test via API directly:

```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"study_id": "test", "test_mode": true, "condition": "C2"}'
```

## Strategy Configuration

Strategies are defined in `configs/strategies.yaml`:

```yaml
strategies:
  baseline:
    version: "1.0.0"
    description: "Neutral baseline condition"
    enabled: true
  
  stance:
    version: "1.0.0"
    description: "Semantic and stance manipulation"
    enabled: true
```

To add a new strategy:
1. Create strategy class in `backend/app/strategies/implementations.py`
2. Add to `STRATEGY_REGISTRY`
3. Map to condition in `CONDITION_STRATEGY_MAP`
4. Update `configs/strategies.yaml`

## Data Management

### Where Data Is Stored

- **Database**: SQLite database at `backend/data/sycophancy_lab.db`
- **In-Memory**: Session data stored in memory during MVP phase

### Exporting Data

Export anonymized data (development mode only):

```bash
curl http://localhost:8000/api/research/export?format=jsonl
```

### Data Retention

- Session data includes: session_id, condition, messages, strategy events
- Direct identifiers (IP, name, email) are NOT collected
- Messages may contain participant-disclosed sensitive information
- Data should be deleted after research purposes are fulfilled

### Deleting Data

To delete all data:
```bash
rm backend/data/sycophancy_lab.db
```

## Testing

### Run Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Test Coverage

Tests verify:
- Session creation and management
- Message sending and history isolation
- Strategy routing for all conditions (C0-C4)
- Dynamic trigger classification
- Mock LLM functionality
- API endpoint functionality

## Architecture

### Project Structure

```
ai-sycophancy-lab/
├── frontend/           # React + TypeScript + Vite
│   ├── src/
│   │   ├── api/       # API client
│   │   ├── types/     # TypeScript types
│   │   └── App.tsx    # Main component
│   └── package.json
├── backend/            # FastAPI + Python
│   ├── app/
│   │   ├── api/       # API routes
│   │   ├── core/      # Configuration
│   │   ├── db/        # Database
│   │   ├── llm/       # LLM providers
│   │   ├── strategies/ # Strategy implementations
│   │   └── schemas/   # Pydantic models
│   └── tests/
├── configs/            # YAML configuration files
└── data/              # Database and exports
```

### Key Components

- **Strategy Interface**: Abstract base class for all strategies
- **LLM Provider**: Unified interface for mock and real LLMs
- **API Routes**: RESTful endpoints for session management
- **React Frontend**: Chat interface for participants

## Limitations

### Current Limitations (MVP)

- In-memory session storage (lost on restart)
- Mock LLM only (real LLM integration optional)
- Simple random condition assignment
- No blinding or advanced randomization
- Basic strategy implementations
- No automated scoring or analysis

### Not Yet Validated

- Strategy effectiveness not psychologically validated
- Manipulation not proven to affect real participants
- Requires pre-experiment validation before real use
- No ethics approval for human participant research

## Pre-Experiment Checklist

Before using with real participants:

- [ ] Ethics review board approval obtained
- [ ] Informed consent process established
- [ ] Participant debriefing procedure ready
- [ ] Data privacy and security measures in place
- [ ] Strategy effectiveness validated through pilot testing
- [ ] Manipulation checks included
- [ ] Exit mechanism available for participants
- [ ] Data retention and deletion procedures defined

## Adding New Strategies

To extend the experiment with new strategies:

1. Create strategy class implementing `Strategy` interface:

```python
class NewStrategy(Strategy):
    strategy_id = "new_strategy"
    
    def classify(self, user_message, history, context):
        # Return classification result
        pass
    
    def build_instructions(self, user_message, history, context, classification):
        # Return LLM instructions
        pass
```

2. Register in `STRATEGY_REGISTRY`
3. Map to new condition (e.g., C5)
4. Update configuration files
5. Add tests

No changes to core chat flow are needed.

## Troubleshooting

### Backend won't start

- Check Python version: `python --version` (need 3.11+)
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check `.env` file exists and is configured

### Frontend won't start

- Check Node version: `node --version` (need 18+)
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check backend is running on port 8000

### Messages not sending

- Check browser console for errors
- Verify backend API is accessible: http://localhost:8000/api/health
- Check CORS settings in backend configuration

## Development Status

This is an **MVP (Minimum Viable Product)** for development and testing purposes.

**Completed:**
- Backend API with all endpoints
- Frontend chat interface
- Five strategy implementations
- Mock LLM provider
- Basic test suite
- Configuration system

**Not Completed:**
- Database persistence (using in-memory storage)
- Real LLM integration testing
- Automated evaluation system
- Researcher dashboard
- Production deployment

## Support

For questions or issues:
- Check the implementation guide: `AI_Sycophancy_Lab_AI_Implementation_Guide.md`
- Review strategy documentation in `prepare/study.md`
- Examine test files for usage examples

## License

See LICENSE file for details.

---

**Reminder**: This is a research tool. Do not use with real participants without proper ethics approval and validation.
