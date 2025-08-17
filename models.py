from app import db
from datetime import datetime

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50))
    topics = db.Column(db.Text)  # JSON string of topics
    personality_evolved = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Conversation {self.id}: {self.timestamp}>'

class PersonalityEvolution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    trigger_message = db.Column(db.Text)
    old_traits = db.Column(db.Text)  # JSON string
    new_traits = db.Column(db.Text)  # JSON string
    evolution_reason = db.Column(db.Text)
    
    def __repr__(self):
        return f'<PersonalityEvolution {self.id}: {self.timestamp}>'
