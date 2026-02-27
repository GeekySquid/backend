# VS Code Setup Guide 🚀

## Quick Start (3 Steps)

### 1️⃣ Open Project in VS Code

```bash
cd ~/Desktop/stock-ai-backend
code .
```

Or: File → Open Folder → Select `stock-ai-backend`

---

### 2️⃣ Run the API Server

**Method A: Using Run & Debug (Easiest)** ⭐

1. Click the **Run & Debug** icon in the left sidebar (▶️ with bug)
2. Select **"Start API Server"** from the dropdown
3. Click the green **Play** button ▶️
4. Server starts in the integrated terminal!

**Method B: Using Terminal**

1. Open terminal in VS Code: `View → Terminal` or `` Ctrl+` ``
2. Run:
```bash
uvicorn app.main:app --reload
```

**Method C: Using Tasks**

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
2. Type: `Tasks: Run Task`
3. Select: `Start API Server`

---

### 3️⃣ Test the API

**Method A: Run Tests**

1. Go to **Run & Debug**
2. Select **"Run Tests"**
3. Click ▶️

**Method B: Open API Docs**

1. Press `Cmd+Shift+P`
2. Type: `Tasks: Run Task`
3. Select: `Open API Docs`
4. Browser opens at http://localhost:8000/docs

**Method C: Manual Test**

Open new terminal and run:
```bash
curl "http://localhost:8000/api/v1/predict?symbol=AAPL"
```

---

## VS Code Features Configured ✨

### 🎯 Run & Debug Configurations

Three pre-configured launch options:

1. **Start API Server** - Runs the FastAPI server with auto-reload
2. **Run Tests** - Executes the test suite
3. **Train Models** - Trains ML models with mock data

### ⚡ Tasks (Quick Actions)

Press `Cmd+Shift+P` → `Tasks: Run Task`:

- **Start API Server** - Launch the API
- **Run Tests** - Test all endpoints
- **Train Models** - Train ML models
- **Install Dependencies** - Install requirements
- **Open API Docs** - Open Swagger UI

### 🔧 Editor Settings

Auto-configured:
- ✅ Format on save
- ✅ Auto-import organization
- ✅ Type checking
- ✅ Linting (flake8)
- ✅ Hide `__pycache__` folders

---

## Keyboard Shortcuts ⌨️

| Action | Mac | Windows/Linux |
|--------|-----|---------------|
| Run/Debug | `F5` | `F5` |
| Open Terminal | `` Cmd+` `` | `` Ctrl+` `` |
| Command Palette | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| Quick Open | `Cmd+P` | `Ctrl+P` |
| Run Task | `Cmd+Shift+B` | `Ctrl+Shift+B` |

---

## Step-by-Step Visual Guide 📸

### Starting the Server

```
1. Click Run & Debug icon (left sidebar)
   ┌─────────────┐
   │  ▶️ 🐛      │  ← Click here
   └─────────────┘

2. Select "Start API Server"
   ┌──────────────────────────┐
   │ Start API Server      ▼  │  ← Click dropdown
   └──────────────────────────┘

3. Click green Play button
   ┌──────────────────────────┐
   │ ▶️ Start API Server      │  ← Click play
   └──────────────────────────┘

4. Terminal shows:
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ✅ Server is running!
```

### Testing the API

```
1. Open new terminal
   Terminal → New Terminal

2. Run test command:
   python3 test_api.py

3. See results:
   ✓ Root endpoint working
   ✓ Health check working
   ✓ Single prediction working
   ✅ ALL TESTS PASSED!
```

---

## Troubleshooting 🔧

### "Module not found" Error

**Solution**: Install dependencies
```bash
pip3 install -r requirements.txt
```

Or use Task: `Cmd+Shift+P` → `Tasks: Run Task` → `Install Dependencies`

### "Port 8000 already in use"

**Solution**: Kill existing process
```bash
lsof -ti:8000 | xargs kill -9
```

Or change port in `.vscode/launch.json`:
```json
"args": [
    "app.main:app",
    "--reload",
    "--port",
    "8001"  // Change to 8001
]
```

### "Python interpreter not found"

**Solution**: Select Python interpreter
1. Press `Cmd+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose Python 3.9 or higher

### Server won't start

**Solution**: Check models are trained
```bash
python3 train_models_mock.py
```

---

## Recommended Extensions 🔌

Install these VS Code extensions for better experience:

1. **Python** (Microsoft) - Essential
2. **Pylance** (Microsoft) - IntelliSense
3. **REST Client** - Test API in VS Code
4. **Thunder Client** - API testing
5. **Better Comments** - Colorful comments

Install: `Cmd+Shift+X` → Search → Install

---

## Using REST Client Extension 🌐

Create `test.http` file:

```http
### Health Check
GET http://localhost:8000/health

### Single Prediction
GET http://localhost:8000/api/v1/predict?symbol=AAPL

### Batch Prediction
POST http://localhost:8000/api/v1/predict/batch
Content-Type: application/json

{
  "symbols": ["AAPL", "GOOGL", "MSFT"]
}

### Metrics
GET http://localhost:8000/metrics
```

Click "Send Request" above each request!

---

## Debugging 🐛

### Set Breakpoints

1. Click left of line number (red dot appears)
2. Press `F5` to start debugging
3. Code pauses at breakpoint
4. Inspect variables in left panel

### Debug Console

While debugging:
- View variables
- Execute Python code
- Inspect objects

---

## Terminal Tips 💡

### Multiple Terminals

1. **Terminal 1**: Run server
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Terminal 2**: Run tests
   ```bash
   python3 test_api.py
   ```

3. **Terminal 3**: Make API calls
   ```bash
   curl "http://localhost:8000/health"
   ```

### Split Terminal

Click the split icon in terminal panel to run multiple commands side-by-side!

---

## Workspace Layout 📐

### Recommended Layout

```
┌─────────────────────────────────────────┐
│  Explorer  │  Editor                    │
│            │                            │
│  app/      │  app/main.py              │
│  ├─core/   │                            │
│  ├─models/ │  [Your code here]         │
│  ├─routes/ │                            │
│  └─services│                            │
│            │                            │
│  README.md │                            │
│            │                            │
├─────────────────────────────────────────┤
│  Terminal                               │
│  $ uvicorn app.main:app --reload       │
│  INFO: Uvicorn running on ...          │
└─────────────────────────────────────────┘
```

---

## Quick Commands Cheat Sheet 📋

```bash
# Start server
uvicorn app.main:app --reload

# Run tests
python3 test_api.py

# Train models
python3 train_models_mock.py

# Install dependencies
pip3 install -r requirements.txt

# Check health
curl http://localhost:8000/health

# Make prediction
curl "http://localhost:8000/api/v1/predict?symbol=AAPL"

# View logs
# (automatically shown in terminal)

# Stop server
# Press Ctrl+C in terminal
```

---

## Pro Tips 🌟

### 1. Auto-reload is enabled
Change any file → Server automatically restarts!

### 2. View logs in real-time
All requests are logged in the terminal with timestamps

### 3. Use Command Palette
`Cmd+Shift+P` is your friend - access everything!

### 4. Quick file navigation
`Cmd+P` → Type filename → Enter

### 5. Multi-cursor editing
`Cmd+D` to select next occurrence
`Cmd+Shift+L` to select all occurrences

---

## Summary 📝

### To Start Working:

1. **Open project**: `code .`
2. **Start server**: Press `F5` → Select "Start API Server"
3. **Test API**: Run `python3 test_api.py`
4. **View docs**: http://localhost:8000/docs

### Common Tasks:

- **Run server**: `F5` or `Cmd+Shift+B`
- **Run tests**: Run & Debug → "Run Tests"
- **Open terminal**: `` Cmd+` ``
- **Command palette**: `Cmd+Shift+P`

---

## Need Help? 🆘

### Check these files:
- `README.md` - Main documentation
- `QUICKSTART.md` - Quick start guide
- `IMPLEMENTATION_COMPLETE.md` - Features list

### VS Code Help:
- Help → Welcome
- Help → Interactive Playground
- Help → Keyboard Shortcuts Reference

---

**You're all set! Press `F5` to start! 🚀**
