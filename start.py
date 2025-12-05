#!/usr/bin/env python3
"""
Startup script for Instagram Bot API with localtunnel integration.
Automatically creates a public URL and copies it to clipboard.
Retries if firewall blocks the connection.
"""

import subprocess
import time
import re
import os
import signal
import sys
from threading import Thread

# Track processes for cleanup
flask_process = None
tunnel_process = None

def copy_to_clipboard(text):
    """Copy text to clipboard (macOS)"""
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        return True
    except Exception as e:
        print(f"⚠️  Could not copy to clipboard: {e}")
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

def start_localtunnel(max_retries=5):
    """Start localtunnel and parse URL"""
    global tunnel_process
    
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            print(f"\n{'='*60}")
            print(f"🌐 Starting localtunnel (attempt {retry_count + 1}/{max_retries})...")
            print(f"{'='*60}\n")
            
            # Start localtunnel
            tunnel_process = subprocess.Popen(
                ['lt', '--port', '5001'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            url_found = False
            
            # Parse output to find URL
            for line in tunnel_process.stdout:
                line = line.strip()
                print(f"[Tunnel] {line}")
                
                # Look for URL pattern
                url_match = re.search(r'https://[a-z0-9-]+\.loca\.lt', line)
                if url_match and not url_found:
                    url = url_match.group(0)
                    url_found = True
                    
                    print(f"\n{'='*60}")
                    print(f"✅ PUBLIC URL: {url}")
                    print(f"{'='*60}\n")
                    
                    # Copy to clipboard
                    if copy_to_clipboard(url):
                        print(f"📋 URL copied to clipboard!")
                    
                    print(f"\n🎯 API Endpoints:")
                    print(f"   • POST {url}/login")
                    print(f"   • POST {url}/send")
                    print(f"   • GET  {url}/health")
                    print(f"\n{'='*60}\n")
                
                # Check for firewall error
                if 'connection refused' in line.lower() or 'firewall' in line.lower() or 'econnrefused' in line.lower():
                    print(f"\n⚠️  Firewall/connection issue detected!")
                    tunnel_process.terminate()
                    retry_count += 1
                    time.sleep(2)
                    break
            else:
                # If loop completed without break, tunnel is running
                tunnel_process.wait()
                break
                
        except Exception as e:
            print(f"❌ Error starting tunnel: {e}")
            retry_count += 1
            time.sleep(2)
    
    if retry_count >= max_retries:
        print(f"\n❌ Failed to establish tunnel after {max_retries} attempts")
        print(f"💡 You can still access API locally at: http://localhost:5001")

def cleanup(signum=None, frame=None):
    """Cleanup processes on exit"""
    print(f"\n\n{'='*60}")
    print("🛑 Shutting down...")
    print(f"{'='*60}\n")
    
    if tunnel_process:
        print("Stopping localtunnel...")
        tunnel_process.terminate()
        tunnel_process.wait()
    
    if flask_process:
        print("Stopping Flask server...")
        flask_process.terminate()
        flask_process.wait()
    
    print("✅ Cleanup complete")
    sys.exit(0)

def main():
    """Main entry point"""
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
    
    # Start localtunnel (blocking)
    try:
        start_localtunnel()
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
