# Life Dashboard

A fully offline, mobile-responsive personal dashboard that runs in a Proxmox LXC container. The dashboard displays live personal metrics and provides AI insights using local Ollama models.

## Features

- **Offline Operation**: Runs completely offline after initial setup
- **Mobile Responsive**: Works on both phone and laptop
- **Local Data Storage**: Uses SQLite and JSON for local metrics
- **AI Integration**: Leverages Ollama for local LLM insights
- **Semantic Memory**: Simple vector store for context retention
- **Persistent Storage**: Survives full Proxmox reboots
- **Containerized**: Deployable in LXC with proper resource limits

## Requirements

- Python 3.8+
- Ollama (local LLM service)
- Docker (for containerization)
- Proxmox LXC container environment

## Setup

1. **Install Ollama**:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Pull required models**:
   ```bash
   ollama pull gemma:2b
   ollama pull all-minilm:22m
   ```

3. **Create virtual environment and install dependencies**:
   ```bash
   python3 -m venv lifedashboard-env
   source lifedashboard-env/bin/activate
   pip install -r requirements.txt
   ```

4. **Initialize database**:
   ```bash
   python init_db.py
   ```

5. **Run the application**:
   ```bash
   ./run.sh
   ```

The dashboard will be accessible at `http://localhost:8001`

## Ollama Configuration

The dashboard uses optimized Ollama settings for mobile performance. Configuration is handled automatically through `ollama.env`:

```bash
OLLAMA_HOST="http://localhost:11434"
OLLAMA_KEEP_ALIVE="2m"
OLLAMA_CONTEXT_LENGTH="2048"
OLLAMA_NUM_PARALLEL="1"
OLLAMA_MAX_LOADED_MODELS="2"
OLLAMA_KV_CACHE_TYPE="f16"
```

These settings ensure:
- Fast response times with model caching
- Efficient resource usage on mobile devices
- Optimal context handling for AI insights
- Prevents memory overload during concurrent operations

## AI Models Used

The dashboard uses lightweight models optimized for local deployment:

1. **gemma:2b** - 2 billion parameter model for general AI insights
   - Size: ~1.7 GB
   - Fast inference
   - Good balance of performance and size

2. **all-minilm:22m** - 22 million parameter embedding model
   - Size: ~45 MB
   - Efficient for semantic memory and context processing
   - Perfect for smartphone deployment

## Deployment

### Docker Container
```bash
docker build -t life-dashboard .
docker run -p 8000:8000 life-dashboard
```

### Proxmox LXC
1. Create a new LXC container
2. Set appropriate resource limits (CPU, Memory)
3. Mount persistent volumes for data storage
4. Deploy the Docker container or run directly with Python

### Systemd Service
```bash
sudo cp systemd/life-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable life-dashboard.service
sudo systemctl start life-dashboard.service
```

## API Endpoints

- `GET /` - Main dashboard page
- `GET /health` - Health check endpoint
- `GET /api/metrics` - Get all dashboard metrics
- `GET /api/tasks` - Get tasks
- `GET /api/calendar` - Get calendar events
- `GET /api/health-logs` - Get health logs
- `GET /api/github` - Get GitHub activity
- `POST /api/ai/insight` - Get AI insights
- `POST /api/ai/summarize` - Summarize week
- `POST /api/ai/plan` - Generate plan
- `GET /api/memory` - Get semantic memory
- `POST /api/memory/add` - Add to memory

## Memory Entry Examples

**Add Text Memory:**
```bash
curl -X POST http://localhost:8001/api/memory/add \
  -H "Content-Type: application/json" \
  -d '{"text": "User\'s personal memory entry"}'
```

**Add Structured Memory:**
```bash
curl -X POST http://localhost:8001/api/memory/add \
  -H "Content-Type: application/json" \
  -d '{"memory": {"event": "Meeting", "duration": "1 hour", "participants": ["Alice", "Bob"]}}'
```
- `POST /api/memory` - Add memory entry (alternative format)

## Data Storage

The dashboard uses:
- **SQLite database** for structured metrics (tasks, calendar, health logs, GitHub activity)
- **JSON files** for semantic memory and configuration
- **Persistent volumes** for data storage that survive container restarts

## AI Integration

The dashboard integrates with Ollama for:
- Summarizing weeks
- Generating daily plans
- Providing personalized insights
- Dynamic model loading/unloading

## Security

- All data is stored locally
- No external API calls after initial setup
- Zero internet connectivity required after configuration
- Secure data handling with local storage only

## Performance

The dashboard is optimized for:
- **Low resource usage**: Uses lightweight models that run efficiently on smartphones
- **Fast response times**: Models are designed for quick inference
- **Offline-first**: All functionality works without internet connection
- **Mobile-friendly**: Responsive design works on all devices

## License

MIT