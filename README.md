# InstaBotv2 Setup Instructions

## Prerequisites
- Python 3.x
- Virtual environment created

## Installation

1. **Install dependencies:**
```bash
source venv/bin/activate
pip install flask playwright python-dotenv
playwright install chromium
```

2. **Install localtunnel (for public URL):**
```bash
npm install -g localtunnel
```

3. **Configure .env file:**
```env
IG_USERNAME=your_instagram_username
IG_PASSWORD=your_instagram_password
```

## Quick Start (Recommended)

**The easiest way to start everything:**

```bash
source venv/bin/activate
python start.py
```

This will:
- ✅ Start Flask server on port 5001
- ✅ Create a public URL via localtunnel
- ✅ Automatically copy the URL to clipboard
- ✅ Retry if firewall blocks the connection

## Manual Usage

### 1. First Login
Before using the API, you need to login once to save the session:

```bash
# Activate virtual environment
source venv/bin/activate

# Run the Flask app (or use start.py for automatic public URL)
python app.py
```

In another terminal, login:
```bash
curl -X POST http://localhost:5001/login
```

This will open a browser window for you to complete the login (including 2FA if needed). Once logged in, the session will be saved.

### 2. Send Messages

After successful login, you can send messages via the API:

```bash
curl -X POST http://localhost:5001/send \
     -H "Content-Type: application/json" \
     -d '{"username": "target_username", "message": "Hello from API!"}'
```

### 3. Health Check

```bash
curl http://localhost:5001/health
```

## API Endpoints

- `POST /login` - Login to Instagram and save session
- `POST /send` - Send a DM (requires `username` and `message` in JSON body)
- `GET /health` - Health check endpoint

## Localtunnel Integration

The `start.py` script provides a public URL for your API:

```bash
python start.py
```

**Features:**
- 🌐 Creates public URL (e.g., `https://abc-xyz.loca.lt`)
- 📋 Automatically copies URL to clipboard
- 🔄 Retries up to 5 times if firewall blocks connection
- 🛑 Graceful shutdown with Ctrl+C

**Example output:**
```
✅ PUBLIC URL: https://friendly-rabbit-123.loca.lt
📋 URL copied to clipboard!

🎯 API Endpoints:
   • POST https://friendly-rabbit-123.loca.lt/login
   • POST https://friendly-rabbit-123.loca.lt/send
   • GET  https://friendly-rabbit-123.loca.lt/health
```

## Notes
- The browser will open in non-headless mode by default for debugging
- Session is saved in `instagram_state.json`
- Only one bot operation can run at a time (thread-locked)
- Use `start.py` for easy public URL access
