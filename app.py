import sys
from flask import Flask, request, jsonify
from bot import InstagramBot
import threading

# Ensure UTF-8 encoding for stdout/stderr to handle emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Global lock to prevent concurrent bot operations
bot_lock = threading.Lock()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


@app.route('/login', methods=['POST'])
def login():
    """Trigger Instagram login"""
    with bot_lock:
        try:
            bot = InstagramBot()
            success = bot.login()
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'Login successful'
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Login failed'
                }), 400
                
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500


@app.route('/send', methods=['POST'])
def send_dm():
    """Send a direct message"""
    with bot_lock:
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'status': 'error',
                    'message': 'No JSON data provided'
                }), 400
            
            username = data.get('username')
            message = data.get('message')
            
            if not username or not message:
                return jsonify({
                    'status': 'error',
                    'message': 'Missing username or message'
                }), 400
            
            bot = InstagramBot()
            success = bot.send_dm(username, message)
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': f'Message sent to {username}'
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to send message'
                }), 400
                
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500


if __name__ == '__main__':
    # Changed to port 5001 to avoid conflicts with AirPlay Receiver on macOS
    app.run(host='0.0.0.0', port=5001, debug=True)
