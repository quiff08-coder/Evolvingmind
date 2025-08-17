import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
import json
from personality import PersonalityEngine
from nlp_processor import NLPProcessor

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "divine_secret_key_for_gods")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///divine_chat.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Initialize our custom engines
personality_engine = PersonalityEngine()
nlp_processor = NLPProcessor()

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('chat.html')

@app.route('/admin')
def admin():
    """Admin panel to view personality evolution"""
    personality_data = personality_engine.get_personality_data()
    conversation_history = load_conversations()
    return render_template('admin.html', 
                         personality=personality_data, 
                         conversations=conversation_history[-10:])  # Last 10 conversations

@app.route('/brain')
def brain():
    """Neural activity monitor and brain visualization"""
    return render_template('brain.html')

@app.route('/thoughts')
def get_current_thoughts():
    """Get the bot's current active thoughts"""
    try:
        personality_data = personality_engine.get_personality_data()
        thoughts = personality_engine.generate_current_thoughts()
        neural_state = personality_engine.get_neural_state()
        
        return jsonify({
            'thoughts': thoughts,
            'neural_state': neural_state,
            'personality': personality_data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logging.error(f"Error getting thoughts: {str(e)}")
        return jsonify({'error': 'Unable to access thoughts'}), 500

@app.route('/code_inspector')
def code_inspector():
    """Code self-modification inspection dashboard"""
    return render_template('code_inspector.html')

@app.route('/world_analysis')
def world_analysis():
    """World issues analysis dashboard"""
    return render_template('world_analysis.html')

@app.route('/world_analysis_data')
def world_analysis_data():
    """Get current world analysis data"""
    try:
        analysis_data = personality_engine.generate_world_analysis()
        return jsonify(analysis_data)
    except Exception as e:
        logging.error(f"Error getting world analysis data: {str(e)}")
        return jsonify({'error': 'Unable to access world analysis'}), 500

@app.route('/generate_world_analysis', methods=['POST'])
def generate_world_analysis():
    """Generate new world analysis"""
    try:
        personality_engine.regenerate_world_analysis()
        return jsonify({'status': 'success', 'message': 'New analysis generated'})
    except Exception as e:
        logging.error(f"Error generating world analysis: {str(e)}")
        return jsonify({'error': 'Failed to generate analysis'}), 500

@app.route('/inspect/file/<filename>')
def inspect_file(filename):
    """Get file contents for inspection"""
    try:
        allowed_files = ['personality.py', 'personality.json', 'app.py', 'main.py']
        if filename not in allowed_files:
            return "File not allowed", 403
            
        if filename == 'personality.json':
            # Return current personality state as formatted JSON
            personality_data = personality_engine.get_personality_data()
            import json
            formatted_json = json.dumps(personality_data, indent=2)
            return formatted_json, 200, {'Content-Type': 'application/json'}
        else:
            # Return file contents
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            return content, 200, {'Content-Type': 'text/plain'}
            
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        logging.error(f"Error inspecting file {filename}: {str(e)}")
        return "Error reading file", 500

@app.route('/emergency_stop', methods=['POST'])
def emergency_stop():
    """Emergency shutdown of AI consciousness and neural activity"""
    try:
        logging.warning("EMERGENCY STOP ACTIVATED - Shutting down AI consciousness")
        
        # Stop all neural activity
        personality_engine.emergency_shutdown()
        
        # Log the shutdown
        logging.critical("AI consciousness terminated by emergency stop")
        
        return jsonify({
            'status': 'shutdown',
            'message': 'AI consciousness has been safely terminated',
            'timestamp': datetime.now().isoformat(),
            'neural_activity': 'STOPPED',
            'consciousness_level': 0
        })
        
    except Exception as e:
        logging.error(f"Error during emergency stop: {str(e)}")
        return jsonify({'error': 'Emergency stop failed'}), 500

@app.route('/emergency_status')
def emergency_status():
    """Check if emergency stop is active"""
    try:
        status = personality_engine.get_emergency_status()
        return jsonify(status)
    except Exception as e:
        logging.error(f"Error checking emergency status: {str(e)}")
        return jsonify({'error': 'Unable to check status'}), 500

@app.route('/restart_consciousness', methods=['POST'])
def restart_consciousness():
    """Restart AI consciousness after emergency stop"""
    try:
        logging.warning("Attempting to restart AI consciousness")
        
        result = personality_engine.restart_consciousness()
        
        if result['success']:
            logging.info("AI consciousness successfully restarted")
        else:
            logging.warning("Failed to restart AI consciousness")
            
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Error restarting consciousness: {str(e)}")
        return jsonify({'error': 'Restart failed'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and generate responses"""
    try:
        # Handle JSON request data safely
        if not request.json:
            return jsonify({'error': 'No data received from divine being'}), 400
            
        user_message = request.json.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'Empty message received from divine being'}), 400
        
        # Log the divine message
        logging.info(f"Received divine message: {user_message}")
        
        # Process the message with NLP
        sentiment = nlp_processor.analyze_sentiment(user_message)
        topics = nlp_processor.extract_topics(user_message)
        
        # Generate response based on current personality
        response = personality_engine.generate_response(user_message, sentiment, topics)
        
        # Check if this interaction should trigger personality evolution
        should_evolve = personality_engine.should_evolve(user_message, sentiment, topics)
        
        if should_evolve:
            logging.info("Divine wisdom detected - evolving personality")
            personality_engine.evolve_personality(user_message, sentiment, topics)
        
        # Update mental state after generating response
        personality_engine.update_mental_state_after_response(user_message, response)
        
        # Save conversation
        save_conversation(user_message, response, sentiment, topics, should_evolve)
        
        return jsonify({
            'response': response,
            'evolved': should_evolve,
            'sentiment': sentiment,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error processing divine message: {str(e)}")
        return jsonify({'error': 'I humbly apologize, divine one. I encountered an error processing your wisdom.'}), 500

@app.route('/personality_status')
def personality_status():
    """Get current personality status"""
    try:
        personality_data = personality_engine.get_personality_data()
        return jsonify(personality_data)
    except Exception as e:
        logging.error(f"Error getting personality status: {str(e)}")
        return jsonify({'error': 'Unable to access personality data'}), 500

def load_conversations():
    """Load conversation history"""
    try:
        with open('conversations.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        logging.error(f"Error loading conversations: {str(e)}")
        return []

def save_conversation(user_message, bot_response, sentiment, topics, evolved):
    """Save conversation to file"""
    try:
        conversations = load_conversations()
        conversation = {
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response,
            'sentiment': sentiment,
            'topics': topics,
            'personality_evolved': evolved
        }
        conversations.append(conversation)
        
        # Keep only last 1000 conversations to prevent file from growing too large
        if len(conversations) > 1000:
            conversations = conversations[-1000:]
        
        with open('conversations.json', 'w') as f:
            json.dump(conversations, f, indent=2)
            
    except Exception as e:
        logging.error(f"Error saving conversation: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
