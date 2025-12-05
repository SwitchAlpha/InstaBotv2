from flask import Flask, request, jsonify
from bot import InstagramBot
import threading

app = Flask(__name__)

# Global lock to prevent concurrent bot operations
bot_lock = threading.Lock()


@app.route('/send', methods=['POST'])
def send_message():
    """
    Send a direct message to an Instagram user.
    
    Request body:
    {
        "username": "target_username",
        "message": "Your message here"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        username = data.get('username')
        message = data.get('message')
        
        if not username or not message:
            return jsonify({'error': 'Both username and message are required'}), 400
        
        # Use lock to ensure only one bot operation at a time
        with bot_lock:
            bot = InstagramBot()
            success = bot.send_dm(username, message)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Message sent to {username}'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to send message. Check logs for details.'
            }), 500
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/login', methods=['POST'])
def login():
    """
    Login to Instagram and save session cookies.
    This endpoint should be called once initially to establish a session.
    """
    try:
        with bot_lock:
            bot = InstagramBot()
            success = bot.login()
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Login successful. Session saved.'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Login failed. Check credentials in .env file.'
            }), 500
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

