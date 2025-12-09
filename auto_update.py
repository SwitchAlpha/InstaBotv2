"""
Auto-update module for Instagram Bot API
Checks GitHub for new versions and updates automatically
"""

import os
import sys
import requests
import subprocess
import shutil
from pathlib import Path

GITHUB_REPO = "SwitchAlpha/InstaBotv2"  # User should update this
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
VERSION_FILE = Path(__file__).parent / "VERSION"
CURRENT_VERSION = "1.0.0"  # Will be read from VERSION file


def get_current_version():
    """Get current installed version"""
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return CURRENT_VERSION


def get_latest_version():
    """Get latest version from GitHub"""
    try:
        response = requests.get(GITHUB_API_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('tag_name', '').lstrip('v')
        return None
    except Exception as e:
        print(f"Failed to check for updates: {e}")
        return None


def compare_versions(v1, v2):
    """Compare two version strings (e.g., '1.0.0' vs '1.0.1')"""
    try:
        v1_parts = [int(x) for x in v1.split('.')]
        v2_parts = [int(x) for x in v2.split('.')]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            part1 = v1_parts[i] if i < len(v1_parts) else 0
            part2 = v2_parts[i] if i < len(v2_parts) else 0
            
            if part1 < part2:
                return -1  # v1 is older
            elif part1 > part2:
                return 1   # v1 is newer
        
        return 0  # Equal
    except:
        return 0


def download_and_update():
    """Download latest version and update"""
    try:
        print("\nDownloading update...")
        
        # Get download URL for the update script
        response = requests.get(GITHUB_API_URL, timeout=10)
        if response.status_code != 200:
            return False
        
        data = response.json()
        
        # For source code updates via git
        if os.path.exists('.git'):
            print("Updating via git pull...")
            result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
            if result.returncode == 0:
                print("Update successful!")
                return True
            else:
                print(f"Git pull failed: {result.stderr}")
                return False
        else:
            # Download update zip and extract
            # This is more complex - user would need to implement
            print("Please update manually by running: git pull")
            print(f"Or download from: https://github.com/{GITHUB_REPO}/releases/latest")
            return False
            
    except Exception as e:
        print(f"Update failed: {e}")
        return False


def check_and_update():
    """Check for updates and install if available"""
    print("\n" + "="*60)
    print("Checking for updates...")
    print("="*60)
    
    current = get_current_version()
    latest = get_latest_version()
    
    if not latest:
        print("Could not check for updates (no internet or repo not found)")
        return False
    
    print(f"Current version: {current}")
    print(f"Latest version:  {latest}")
    
    if compare_versions(current, latest) < 0:
        print(f"\nNew version available: {latest}")
        
        # Auto-update
        user_input = input("Would you like to update now? (y/n): ").strip().lower()
        if user_input == 'y':
            if download_and_update():
                # Update VERSION file
                VERSION_FILE.write_text(latest)
                print("\nUpdate complete! Please restart the application.")
                return True
            else:
                print("\nUpdate failed. Continuing with current version.")
        else:
            print("Update skipped.")
    else:
        print("You are running the latest version!")
    
    print("="*60 + "\n")
    return False


if __name__ == "__main__":
    check_and_update()
