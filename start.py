#!/usr/bin/env python3
"""
Startup script for Instagram Bot API with Cloudflare Tunnel.
Automatically creates a public URL and copies it to clipboard.
Uses cloudflared - reliable, no signup required!
"""

import subprocess
import time
import os
import signal
import sys
import re
import platform
import urllib.request
import stat
import requests
from threading import Thread
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import auto-update module
try:
    from auto_update import check_and_update
    AUTO_UPDATE_AVAILABLE = True
except ImportError:
    AUTO_UPDATE_AVAILABLE = False

# Track processes for cleanup
flask_process = None
tunnel_process = None

def get_cloudflared_path():
    """Get or download cloudflared binary"""
    # Check if cloudflared is already in PATH
    try:
        result = subprocess.run(['which', 'cloudflared'], capture_output=True, text=True)
        if result.returncode == 0:
            return 'cloudflared'
    except:
        pass
    
    # Download cloudflared if not found
    cloudflared_dir = Path.home() / '.instabot'
    cloudflared_dir.mkdir(exist_ok=True)
    
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Determine download URL based on OS/arch
    if system == 'darwin':
        if 'arm' in machine or 'aarch64' in machine:
            url = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64.tgz'
        else:
            url = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz'
        cloudflared_path = cloudflared_dir / 'cloudflared'
    elif system == 'linux':
        if 'arm' in machine or 'aarch64' in machine:
            url = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64'
        else:
            url = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64'
        cloudflared_path = cloudflared_dir / 'cloudflared'
    elif system == 'windows':
        url = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe'
        cloudflared_path = cloudflared_dir / 'cloudflared.exe'
    else:
        raise Exception(f"Unsupported platform: {system}")
    
    # Check if already downloaded
    if cloudflared_path.exists():
        return str(cloudflared_path)
    
    # Download cloudflared
    print(f"📥 Downloading cloudflared (~50MB)...")
    print(f"   This only happens once...")
    
    try:
        if url.endswith('.tgz'):
            # Download and extract tar.gz (macOS)
            tgz_path = cloudflared_dir / 'cloudflared.tgz'
            print(f"   Downloading from: {url}")
            urllib.request.urlretrieve(url, str(tgz_path))
            
            # Extract - macOS cloudflared.tgz contains a single binary named 'cloudflared'
            import tarfile
            with tarfile.open(str(tgz_path), 'r:gz') as tar:
                # Extract to temp location
                tar.extractall(str(cloudflared_dir))
            
            # The extracted file should be 'cloudflared' in the directory
            # Rename it to our target if needed
            extracted_binary = cloudflared_dir / 'cloudflared'
            if extracted_binary.exists() and extracted_binary != cloudflared_path:
                if cloudflared_path.exists():
                    cloudflared_path.unlink()
                extracted_binary.rename(cloudflared_path)
            
            # Clean up tgz file
            if tgz_path.exists():
                tgz_path.unlink()
        else:
            # Direct download (Linux/Windows)
            urllib.request.urlretrieve(url, str(cloudflared_path))
        
        # Verify the file exists and has content
        if not cloudflared_path.exists():
            raise Exception("Cloudflared binary not found after download")
        
        if cloudflared_path.stat().st_size < 1000:
            raise Exception("Cloudflared binary seems corrupted (too small)")
        
        # Make executable - use os.chmod for better compatibility
        current_permissions = os.stat(str(cloudflared_path)).st_mode
        os.chmod(str(cloudflared_path), current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        
        print(f"✅ Cloudflared downloaded successfully!")
        print(f"   Binary size: {cloudflared_path.stat().st_size / 1024 / 1024:.1f}MB")
        return str(cloudflared_path)
    
    except Exception as e:
        print(f"❌ Failed to download cloudflared: {e}")
        # Clean up on failure
        try:
            if tgz_path.exists():
                tgz_path.unlink()
            if cloudflared_path.exists():
                cloudflared_path.unlink()
        except:
            pass
        raise

def copy_to_clipboard(text):
    """Copy text to clipboard (macOS/Linux/Windows)"""
    try:
        if platform.system() == 'Darwin':  # macOS
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            process.communicate(text.encode('utf-8'))
            return True
        elif platform.system() == 'Windows':  # Windows
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            process.communicate(text.encode('utf-8'))
            return True
        else:  # Linux
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            process.communicate(text.encode('utf-8'))
            return True
    except:
        return False

def run_flask():
    """Run Flask server"""
    global flask_process
    print("🚀 Starting Flask server...")
    flask_process = subprocess.Popen(
        ['python', 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Print Flask output
    for line in flask_process.stdout:
        print(f"[Flask] {line.strip()}")

def start_tunnel():
    """Start Cloudflare tunnel"""
    global tunnel_process
    
    try:
        print(f"\n{'='*60}")
        print("🌐 Starting Cloudflare Tunnel...")
        print("   (Reliable & Free - No signup required!)")
        print(f"{'='*60}\n")
        
        # Get cloudflared binary
        cloudflared = get_cloudflared_path()
        
        # Start cloudflared tunnel
        tunnel_process = subprocess.Popen(
            [cloudflared, 'tunnel', '--url', 'http://localhost:5001'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        url_found = False
        
        # Parse output to find the public URL
        for line in tunnel_process.stdout:
            line = line.strip()
            
            # Cloudflare prints the URL in format: "https://xxx.trycloudflare.com"
            if not url_found and ('trycloudflare.com' in line or 'cloudflare' in line.lower()):
                # Extract URL
                url_match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line)
                if url_match:
                    url = url_match.group(0)
                    url_found = True
                    
                    print(f"\n{'='*60}")
                    print(f"✅ PUBLIC URL: {url}")
                    print(f"{'='*60}\n")
                    
                    # Copy to clipboard
                    if copy_to_clipboard(url):
                        print(f"📋 URL copied to clipboard!")
                    else:
                        print(f"📋 Copy this URL manually: {url}")
                    
                    # Register with n8n webhook
                    try:
                        region = os.getenv('REGION', 'unknown')
                        webhook_url = 'https://n8n.liveapp-dev.com/webhook/register-region'
                        
                        payload = {
                            'url': url,
                            'region': region
                        }
                        
                        print(f"\n📡 Registering with webhook...")
                        print(f"   Region: {region}")
                        
                        response = requests.post(webhook_url, json=payload, timeout=10)
                        
                        if response.status_code == 200:
                            print(f"✅ Successfully registered with n8n!")
                        else:
                            print(f"⚠️  Webhook registration failed (status {response.status_code})")
                    except Exception as webhook_error:
                        print(f"⚠️  Webhook registration failed: {webhook_error}")
                    
                    print(f"\n🎯 API Endpoints:")
                    print(f"   • POST {url}/login")
                    print(f"   • POST {url}/send")
                    print(f"   • GET  {url}/health")
                    print(f"\n{'='*60}\n")
                    print(f"🔗 Tunnel is active. Press Ctrl+C to stop.\n")
            
            # Show relevant messages
            if 'error' in line.lower() or 'fail' in line.lower():
                print(f"[Tunnel] {line}")
        
        # If loop ends, process has terminated
        tunnel_process.wait()
        
    except Exception as e:
        print(f"\n❌ Error starting Cloudflare tunnel: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   1. Check internet connection")
        print(f"   2. Try running: python app.py (to test Flask alone)")
        print(f"\n   You can still access the API locally at: http://localhost:5001\n")

def cleanup(signum=None, frame=None):
    """Cleanup processes on exit"""
    print(f"\n\n{'='*60}")
    print("🛑 Shutting down...")
    print(f"{'='*60}\n")
    
    if tunnel_process:
        print("Closing tunnel...")
        tunnel_process.terminate()
        try:
            tunnel_process.wait(timeout=2)
        except:
            tunnel_process.kill()
    
    if flask_process:
        print("Stopping Flask server...")
        flask_process.terminate()
        try:
            flask_process.wait(timeout=2)
        except:
            flask_process.kill()
    
    print("✅ Cleanup complete")
    sys.exit(0)

def main():
    """Main entry point"""
    # Check for updates first
    if AUTO_UPDATE_AVAILABLE:
        try:
            if check_and_update():
                # If update was successful, user needs to restart
                print("Please restart the application to use the new version.")
                sys.exit(0)
        except Exception as e:
            print(f"Auto-update check failed: {e}")
            print("Continuing with current version...\n")
    
    # Register cleanup handlers
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    print(f"\n{'='*60}")
    print("🤖 Instagram Bot API - Starting Up")
    print(f"{'='*60}\n")
    
    # Start Flask in background thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Wait for Flask to start
    print("⏳ Waiting for Flask to initialize...")
    time.sleep(3)
    
    # Start tunnel (blocking)
    try:
        start_tunnel()
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
