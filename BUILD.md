# Building Executables

## Automated Builds (GitHub Actions)

When you push a version tag to GitHub, executables are automatically built for both macOS and Windows.

### Steps:

1. **Create a GitHub repository** (if you haven't already):
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/InstaBotv2.git
git push -u origin main
```

2. **Create and push a version tag**:
```bash
git tag v1.0.0
git push origin v1.0.0
```

3. **Wait for build** (takes ~5-10 minutes)
   - Go to your repository on GitHub
   - Click "Actions" tab
   - Watch the build progress

4. **Download executables**:
   - Go to "Releases" tab
   - Download `InstaBotAPI-macOS` or `InstaBotAPI-Windows.exe`

### Manual Build Trigger

You can also trigger builds manually:
1. Go to "Actions" tab on GitHub
2. Select "Build Executables" workflow
3. Click "Run workflow"

## Local Build (Current Platform Only)

You can also build locally for your current platform:

### macOS:
```bash
source venv/bin/activate
pip install -r requirements.txt
pyinstaller instabot.spec
```

Output: `dist/InstaBotAPI` (macOS executable)

### Windows:
```cmd
venv\Scripts\activate
pip install -r requirements.txt
pyinstaller instabot.spec
```

Output: `dist\InstaBotAPI.exe` (Windows executable)

## Using the Executables

### Setup:
1. Download the executable for your platform
2. Create a `.env` file in the same directory:
```env
IG_USERNAME=your_username
IG_PASSWORD=your_password
```

3. Install Node.js and localtunnel:
```bash
npm install -g localtunnel
```

### Run:
**macOS:**
```bash
chmod +x InstaBotAPI-macOS
./InstaBotAPI-macOS
```

**Windows:**
```cmd
InstaBotAPI-Windows.exe
```

The public URL will be displayed and copied to your clipboard automatically!

## Troubleshooting

### "Cannot verify app" (macOS)
```bash
xattr -d com.apple.quarantine InstaBotAPI-macOS
```

### Missing Playwright browsers
The executable will prompt you to install browsers on first run.

### Port already in use
Check if Flask is already running on port 5001:
```bash
lsof -ti:5001 | xargs kill -9  # macOS/Linux
```
