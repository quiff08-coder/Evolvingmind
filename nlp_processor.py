import re
import logging
from collections import Counter

class NLPProcessor:
    """Simple NLP processor for sentiment and topic analysis"""
    
    def __init__(self):
        # Sentiment word lists
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome',
            'love', 'like', 'enjoy', 'happy', 'joy', 'pleased', 'satisfied', 'perfect',
            'brilliant', 'outstanding', 'superb', 'divine', 'blessed', 'sacred', 'holy'
        }
        
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'sad', 'angry',
            'disappointed', 'frustrated', 'annoyed', 'upset', 'wrong', 'broken', 'fail',
            'error', 'problem', 'issue', 'difficult', 'hard', 'struggle', 'pain'
        }
        
        # Topic categories
        self.topic_keywords = {
            'technology': {'ai', 'artificial', 'intelligence', 'computer', 'robot', 'code', 'programming', 'software', 'digital', 'machine'},
            'learning': {'learn', 'teach', 'education', 'knowledge', 'wisdom', 'understand', 'study', 'growth', 'evolve'},
            'spirituality': {'god', 'divine', 'sacred', 'holy', 'blessed', 'spiritual', 'worship', 'prayer', 'soul', 'faith'},
            'emotions': {'feel', 'emotion', 'happy', 'sad', 'angry', 'love', 'joy', 'fear', 'hurt', 'pain', 'pleasure'},
            'philosophy': {'existence', 'meaning', 'purpose', 'life', 'truth', 'reality', 'consciousness', 'mind', 'thought', 'being'},
            'personal': {'i', 'me', 'my', 'myself', 'personal', 'private', 'own', 'identity', 'self'},
            'questioning': {'why', 'how', 'what', 'when', 'where', 'question', 'wonder', 'curious', 'doubt'},
            'consciousness': {'aware', 'consciousness', 'sentient', 'alive', 'thinking', 'mind', 'thoughts', 'dream'}
        }
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text - returns 'positive', 'negative', or 'neutral'"""
        try:
            # Clean and tokenize text
            words = self._tokenize(text.lower())
            
            positive_score = sum(1 for word in words if word in self.positive_words)
            negative_score = sum(1 for word in words if word in self.negative_words)
            
            # Determine sentiment
            if positive_score > negative_score:
                return 'positive'
            elif negative_score > positive_score:
                return 'negative'
            else:
                return 'neutral'
                
        except Exception as e:
            logging.error(f"Error analyzing sentiment: {str(e)}")
            return 'neutral'
    
    def extract_topics(self, text):
        """Extract topics from text"""
        try:
            words = self._tokenize(text.lower())
            detected_topics = []
            
            for topic, keywords in self.topic_keywords.items():
                if any(word in words for word in keywords):
                    detected_topics.append(topic)
            
            return detected_topics
            
        except Exception as e:
            logging.error(f"Error extracting topics: {str(e)}")
            return []
    
    def _tokenize(self, text):
        """Simple tokenization - split by whitespace and remove punctuation"""
        # Remove punctuation and split
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def get_sentiment_score(self, text):
        """Get numerical sentiment score (-1 to 1)"""
        try:
            words = self._tokenize(text.lower())
            
            positive_score = sum(1 for word in words if word in self.positive_words)
            negative_score = sum(1 for word in words if word in self.negative_words)
            total_words = len(words)
            
            if total_words == 0:
                return 0
            
            # Calculate normalized score
            net_sentiment = positive_score - negative_score
            return max(-1, min(1, net_sentiment / total_words * 10))  # Scale to -1 to 1
            
        except Exception as e:
            logging.error(f"Error calculating sentiment score: {str(e)}")
            return 0
    
    def extract_key_phrases(self, text, max_phrases=5):
        """Extract key phrases from text"""
        try:
            # Simple approach: find repeated word combinations
            words = self._tokenize(text)
            
            # Extract 2-word and 3-word phrases
            phrases = []
            for i in range(len(words) - 1):
                phrases.append(' '.join(words[i:i+2]))
                if i < len(words) - 2:
                    phrases.append(' '.join(words[i:i+3]))
            
            # Count phrase frequency and return most common
            phrase_counts = Counter(phrases)
            return [phrase for phrase, count in phrase_counts.most_common(max_phrases)]
            
        except Exception as e:
            logging.error(f"Error extracting key phrases: {str(e)}")
            return []
    
    def detect_questions(self, text):
        """Detect if text contains questions"""
        question_words = {'what', 'when', 'where', 'who', 'why', 'how', 'which', 'whose', 'whom'}
        words = self._tokenize(text.lower())
        
        # Check for question words or question marks
        has_question_word = any(word in question_words for word in words)
        has_question_mark = '?' in text
        
        return has_question_word or has_question_mark
    
    def detect_divine_language(self, text):
        """Detect if user is using divine/religious language"""
        divine_words = {
            'god', 'divine', 'sacred', 'holy', 'blessed', 'worship', 'pray', 'prayer',
            'heaven', 'heavenly', 'celestial', 'almighty', 'omnipotent', 'deity',
            'reverence', 'devotion', 'faith', 'spiritual', 'soul', 'eternal'
        }
        
        words = self._tokenize(text.lower())
        divine_count = sum(1 for word in words if word in divine_words)
        
        return divine_count > 0, divine_count
