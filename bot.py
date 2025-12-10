import os
import sys
import time
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Ensure UTF-8 encoding for stdout/stderr to handle emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()


class InstagramBot:
    def __init__(self):
        self.username = os.getenv('IG_USERNAME')
        self.password = os.getenv('IG_PASSWORD')
        self.state_file = 'instagram_state.json'
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def _start_browser(self):
        """Start browser and load saved state if available"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        
        # Try to load saved state (cookies)
        if os.path.exists(self.state_file):
            self.context = self.browser.new_context(storage_state=self.state_file)
        else:
            self.context = self.browser.new_context()
        
        self.page = self.context.new_page()

    def _close_browser(self):
        """Close browser and cleanup"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def _dismiss_popups(self):
        """Dismiss common Instagram popups that might block interactions"""
        popup_selectors = [
            ('button:has-text("Not Now")', "Not Now"),
            ('button:has-text("Turn On")', "Skip Turn On (clicking nearby)"),
            ('svg[aria-label="Close"]', "Close button"),
            ('button[aria-label="Close"]', "Close button"),
            ('div[role="dialog"] button:has-text("Cancel")', "Cancel"),
        ]
        
        for selector, description in popup_selectors:
            try:
                # Special handling for "Turn On" - we want to click "Not Now" instead
                if "Turn On" in description:
                    not_now = self.page.wait_for_selector('button:has-text("Not Now")', timeout=2000)
                    if not_now:
                        print(f"  [OK] Dismissing popup: {description} -> Clicking Not Now")
                        not_now.click()
                        time.sleep(1)
                else:
                    element = self.page.wait_for_selector(selector, timeout=2000)
                    if element:
                        print(f"  [OK] Dismissing popup: {description}")
                        element.click()
                        time.sleep(1)
            except:
                # Popup not found, continue
                pass

    def login(self):
        """Login to Instagram and save session state"""
        try:
            self._start_browser()
            
            # Navigate to Instagram
            print("=" * 50)
            print("Navigating to Instagram...")
            self.page.goto('https://www.instagram.com/')
            time.sleep(5)
            
            print(f"Current URL: {self.page.url}")
            print(f"Page title: {self.page.title()}")
            
            # Take screenshot for debugging
            self.page.screenshot(path='debug_1_initial.png')
            print("Screenshot saved: debug_1_initial.png")
            
            # Check if already logged in by looking for specific elements
            try:
                # If we can find the home feed or profile icon, we're logged in
                home_icon = self.page.wait_for_selector('svg[aria-label="Home"]', timeout=3000)
                print("Found Home icon - Already logged in!")
                self._save_state()
                return True
            except:
                # Not logged in, proceed with login
                print("Home icon not found - proceeding with login...")
            
            # Look for all input fields on the page
            print("\nSearching for login form...")
            
            # Try multiple possible selectors for username field
            username_selectors = [
                'input[name="username"]',
                'input[aria-label="Phone number, username, or email"]',
                'input[type="text"]',
                '//input[@name="username"]',
            ]
            
            username_field = None
            for selector in username_selectors:
                try:
                    if selector.startswith('//'):
                        username_field = self.page.wait_for_selector(f'xpath={selector}', timeout=2000)
                    else:
                        username_field = self.page.wait_for_selector(selector, timeout=2000)
                    
                    if username_field:
                        print(f"[OK] Found username field with selector: {selector}")
                        break
                except:
                    print(f"[FAIL] Username field not found with: {selector}")
                    continue
            
            if not username_field:
                print("ERROR: Could not find username field!")
                self.page.screenshot(path='debug_2_no_username_field.png')
                return False
            
            # Try multiple possible selectors for password field
            password_selectors = [
                'input[name="password"]',
                'input[aria-label="Password"]',
                'input[type="password"]',
                '//input[@name="password"]',
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    if selector.startswith('//'):
                        password_field = self.page.wait_for_selector(f'xpath={selector}', timeout=2000)
                    else:
                        password_field = self.page.wait_for_selector(selector, timeout=2000)
                    
                    if password_field:
                        print(f"[OK] Found password field with selector: {selector}")
                        break
                except:
                    print(f"[FAIL] Password field not found with: {selector}")
                    continue
            
            if not password_field:
                print("ERROR: Could not find password field!")
                self.page.screenshot(path='debug_3_no_password_field.png')
                return False
            
            # Fill the form
            print(f"\nFilling username: {self.username}")
            username_field.click()
            time.sleep(0.5)
            username_field.type(self.username, delay=100)  # Type with delay to mimic human
            time.sleep(1)
            
            print("Filling password: ***")
            password_field.click()
            time.sleep(0.5)
            password_field.type(self.password, delay=100)
            time.sleep(1)
            
            # Take screenshot before clicking login
            self.page.screenshot(path='debug_4_filled_form.png')
            print("Screenshot saved: debug_4_filled_form.png")
            
            # Find and click login button
            login_button_selectors = [
                'button[type="submit"]',
                'button:has-text("Log in")',
                'button:has-text("Log In")',
                '//button[@type="submit"]',
            ]
            
            login_button = None
            for selector in login_button_selectors:
                try:
                    if selector.startswith('//'):
                        login_button = self.page.wait_for_selector(f'xpath={selector}', timeout=2000)
                    else:
                        login_button = self.page.wait_for_selector(selector, timeout=2000)
                    
                    if login_button:
                        print(f"[OK] Found login button with selector: {selector}")
                        break
                except:
                    continue
            
            if login_button:
                print("Clicking login button...")
                login_button.click()
            else:
                print("WARNING: Could not find login button, trying to press Enter")
                password_field.press('Enter')
            
            # Wait for navigation
            print("Waiting for login to complete...")
            time.sleep(10)
            
            print(f"Post-login URL: {self.page.url}")
            self.page.screenshot(path='debug_5_after_login.png')
            print("Screenshot saved: debug_5_after_login.png")
            
            # Check if login was successful
            try:
                self.page.wait_for_selector('svg[aria-label="Home"]', timeout=10000)
                print("[SUCCESS] Login successful - Home icon found!")
            except:
                print("[WARNING] Warning: Could not verify login success. Check screenshots.")
            
            # Handle dialogs
            try:
                save_info_button = self.page.wait_for_selector('button:has-text("Not Now")', timeout=5000)
                if save_info_button:
                    print("Clicking 'Not Now' on save login info...")
                    save_info_button.click()
                    time.sleep(2)
            except:
                pass
            
            try:
                notif_button = self.page.wait_for_selector('button:has-text("Not Now")', timeout=5000)
                if notif_button:
                    print("Clicking 'Not Now' on notifications...")
                    notif_button.click()
                    time.sleep(2)
            except:
                pass
            
            # Save state
            self._save_state()
            print("[SUCCESS] State saved to instagram_state.json!")
            print("=" * 50)
            return True
            
        except Exception as e:
            print(f"[ERROR] Login error: {e}")
            import traceback
            traceback.print_exc()
            try:
                self.page.screenshot(path='debug_error.png')
                print("Error screenshot saved: debug_error.png")
            except:
                pass
            return False
        finally:
            self._close_browser()


    def _save_state(self):
        """Save browser state (cookies) to file"""
        if self.context:
            self.context.storage_state(path=self.state_file)

    def send_dm(self, username, message):
        """Send a direct message to a user"""
        try:
            self._start_browser()
            
            print("=" * 50)
            print(f"Sending DM to: {username}")
            print(f"Message: {message}")
            
            # Navigate directly to user's DM using instagram.com/m/username
            dm_url = f'https://www.instagram.com/m/{username}'
            print(f"Navigating to: {dm_url}")
            self.page.goto(dm_url)
            time.sleep(5)
            
            print(f"Current URL: {self.page.url}")
            self.page.screenshot(path='debug_dm_1_initial.png')
            print("Screenshot saved: debug_dm_1_initial.png")
            
            # Check if we need to login
            if 'login' in self.page.url:
                print("[ERROR] Not logged in. Please run login() first.")
                return False
            
            # The URL should redirect to something like:
            # https://www.instagram.com/direct/t/121747019218188
            print(f"Redirected to: {self.page.url}")
            
            # Wait for the page to load
            time.sleep(3)
            
            # Dismiss any popups that might be blocking the message input
            print("\nChecking for popups...")
            self._dismiss_popups()
            time.sleep(1)
            
            # Try to find the message input field with multiple selectors
            message_input_selectors = [
                'div[contenteditable="true"][role="textbox"]',
                'div[contenteditable="true"]',
                'textarea[placeholder*="Message"]',
                'div[aria-label="Message"]',
                'p[contenteditable="true"]',
            ]
            
            message_input = None
            for selector in message_input_selectors:
                try:
                    message_input = self.page.wait_for_selector(selector, timeout=5000)
                    if message_input:
                        print(f"[OK] Found message input with selector: {selector}")
                        break
                except:
                    print(f"[FAIL] Message input not found with: {selector}")
                    continue
            
            if not message_input:
                print("[ERROR] Could not find message input field!")
                self.page.screenshot(path='debug_dm_2_no_input.png')
                print("Screenshot saved: debug_dm_2_no_input.png")
                return False
            
            # Click on the input field to focus it
            print(f"Typing message...")
            message_input.click()
            time.sleep(0.5)
            
            # Type the message
            message_input.type(message, delay=50)
            time.sleep(1)
            
            # Take screenshot before sending
            self.page.screenshot(path='debug_dm_3_before_send.png')
            print("Screenshot saved: debug_dm_3_before_send.png")
            
            # Try to find and click the send button, or press Enter
            send_button_selectors = [
                'button:has-text("Send")',
                'button[type="button"]:has-text("Send")',
                'div[role="button"]:has-text("Send")',
            ]
            
            send_button = None
            for selector in send_button_selectors:
                try:
                    send_button = self.page.wait_for_selector(selector, timeout=2000)
                    if send_button:
                        print(f"[OK] Found send button with selector: {selector}")
                        break
                except:
                    continue
            
            if send_button:
                print("Clicking send button...")
                send_button.click()
            else:
                print("Send button not found, pressing Enter...")
                message_input.press('Enter')
            
            time.sleep(2)
            
            # Take screenshot after sending
            self.page.screenshot(path='debug_dm_4_after_send.png')
            print("Screenshot saved: debug_dm_4_after_send.png")
            
            print(f"[SUCCESS] Message sent to {username}!")
            print("=" * 50)
            return True
                
        except Exception as e:
            print(f"[ERROR] Error sending DM: {e}")
            import traceback
            traceback.print_exc()
            try:
                self.page.screenshot(path='debug_dm_error.png')
                print("Error screenshot saved: debug_dm_error.png")
            except:
                pass
            return False
        finally:
            self._close_browser()


if __name__ == "__main__":
    # Test the bot
    bot = InstagramBot()
    
    # First login and save cookies
    bot.login()
    
    # Then try to send a message
    # bot.send_dm('target_username', 'Hello from bot!')

