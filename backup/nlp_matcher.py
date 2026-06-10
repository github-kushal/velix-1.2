import spacy
import pickle
import numpy as np
import os

class NLPMatcher:
    def __init__(self, learning_enabled=True):
        self.learning_enabled = learning_enabled
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except OSError:
            raise Exception("spaCy model 'en_core_web_lg' not found. Please install it with: python -m spacy download en_core_web_lg")

        self.commands = {
            # Web & Search
            'open_google': ['open google', 'google search', 'launch google', 'go to google'],
            'open_youtube': ['open youtube', 'youtube', 'launch youtube', 'go to youtube'],
            'find_video': ['find video', 'search video', 'youtube search', 'search on youtube'],
            'search_web': ['search', 'google', 'search for', 'find information', 'look up'],
            'wikipedia': ['wikipedia', 'wiki', 'tell me about', 'information about'],
            
            # PDF & Files
            'read_pdf': ['read pdf', 'open pdf', 'show pdf', 'read document', 'pdf file'],
            'open_file': ['open file', 'open folder', 'launch file'],
            'take_note': ['take note', 'make note', 'write note', 'save note', 'note down'],
            
            # Media
            'play_music': ['play music', 'start music', 'music please', 'put on music'],
            
            # Information
            'weather': ['weather', 'temperature', 'forecast', 'how hot', 'how cold'],
            'time': ['time', 'current time', 'what time'],
            'location': ['location', 'where am i', 'current location'],
            'distance': ['distance', 'how far', 'miles to', 'kilometers to'],
            'crypto_price': ['crypto price', 'cryptocurrency', 'bitcoin price', 'crypto value'],
            
            # AI & Chat
            'activate_ai': ['activate ai', 'ai mode', 'chat mode', 'ai assistant'],
            'joke': ['joke', 'tell joke', 'funny', 'make me laugh'],
            'quote': ['quote', 'inspiration', 'motivational quote'],
            'random_fact': ['fact', 'random fact', 'tell me fact', 'interesting fact'],
            
            # System Control
            'shutdown': ['shutdown', 'turn off', 'power off', 'shut down'],
            'restart': ['restart', 'reboot', 'restart computer'],
            'sleep': ['sleep', 'hibernate', 'standby'],
            'volume': ['volume', 'set volume', 'change volume'],
            'screenshot': ['screenshot', 'capture screen', 'take screenshot'],
            'change_tab': ['change tab', 'switch tab', 'next tab', 'previous tab', 'change the tab', 'change this tab'],
            'close_window': ['close window', 'close program', 'exit window', 'close app', 'close tab'],
            
            # Tasks & Reminders
            'set_alarm': ['set alarm', 'alarm', 'wake me up', 'create alarm'],
            'reminder': ['reminder', 'remind me', 'set reminder'],
            'todo': ['todo', 'to do', 'task list', 'todo list'],
            'timer': ['timer', 'set timer', 'countdown'],
            
            # Authentication & System
            'change_password': ['change password', 'new password', 'update password'],
            'enroll_face': ['enroll face', 'add face', 'register face', 'face recognition'],
            'malfunction': ['malfunction', 'restart program', 'reload', 'reset'],
            
            # Utilities
            'calculate': ['calculate', 'math', 'compute', 'calculator'],
            'translate': ['translate', 'translation', 'convert language'],
            'how_to': ['how to', 'instructions for', 'guide for', 'steps to'],
            
            # Exit
            'exit': ['bye', 'goodbye', 'exit', 'quit', 'good bye'],
            'thank_you': ['thank you', 'thanks', 'appreciate it']
        }

        # Load or create command embeddings
        self.command_embeddings = self.load_or_create_embeddings()

    def load_or_create_embeddings(self):
        """Load embeddings from file or create new ones"""
        if os.path.exists('command_embeddings.pkl'):
            try:
                with open('command_embeddings.pkl', 'rb') as f:
                    return pickle.load(f)
            except (pickle.PickleError, EOFError):
                print("Warning: Could not load embeddings file. Creating new embeddings...")
        
        # Create new embeddings
        command_embeddings = {}
        for cmd, phrases in self.commands.items():
            embeddings = {}
            for phrase in phrases:
                embeddings[phrase] = self.nlp(phrase).vector
            command_embeddings[cmd] = embeddings
        
        # Save embeddings
        with open('command_embeddings.pkl', 'wb') as f:
            pickle.dump(command_embeddings, f)
        
        return command_embeddings

    def user_input_to_command(self, user_input):
        """Convert user input to the best matching command"""
        if not user_input or user_input.strip() == "":
            return None, 0.0
        
        # Convert user input to vector
        user_doc = self.nlp(user_input)
        user_vector = user_doc.vector
        
        best_match = None
        best_score = -1.0
        matched_phrase = ""

        # Search through all command embeddings
        for cmd_name, emb_dict in self.command_embeddings.items():
            for phrase, embedding in emb_dict.items():
                similarity = self.calculate_similarity(user_vector, embedding)
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = cmd_name
                    matched_phrase = phrase
        
        # Return both the command name and the score
        if best_match:
            return {
                'command': best_match,
                'confidence': best_score,
                'matched_phrase': matched_phrase,
                'user_input': user_input
            }
        else:
            return None

    def calculate_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        # Avoid division by zero
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)
    


    def get_confidence_level(self, score):
        """Convert similarity score to confidence level"""
        if score >= 0.8:
            return "HIGH"
        elif score >= 0.6:
            return "MEDIUM"
        elif score >= 0.4:
            return "LOW"
        else:
            return "VERY_LOW"

    def add_custom_command(self, command_name, phrases):
        """Add a new custom command to the matcher"""
        if command_name in self.commands:
            print(f"Warning: Command '{command_name}' already exists. Overwriting.")
        
        self.commands[command_name] = phrases
        
        # Update embeddings for this command
        embeddings = {}
        for phrase in phrases:
            embeddings[phrase] = self.nlp(phrase).vector
        self.command_embeddings[command_name] = embeddings
        
        # Save updated embeddings
        with open('command_embeddings.pkl', 'wb') as f:
            pickle.dump(self.command_embeddings, f)
        
        print(f"Added custom command: {command_name}")

    def get_available_commands(self):
        """Get list of all available commands"""
        return list(self.commands.keys())

    def test_matching(self, test_phrases=None):
        """Test the matcher with example phrases"""
        if test_phrases is None:
            test_phrases = [
                "what's the temperature outside",
                "play some songs",
                "thanks for your help",
                "I want to watch videos",
                "set an alarm for morning",
                "how far is london",
                "tell me a joke"
            ]
        
        print("Testing NLP Matcher:")
        print("-" * 50)
        
        for phrase in test_phrases:
            result = self.user_input_to_command(phrase)
            if result:
                confidence_level = self.get_confidence_level(result['confidence'])
                print(f"'{phrase}'")
                print(f"  → Command: {result['command']}")
                print(f"  → Confidence: {result['confidence']:.3f} ({confidence_level})")
                print(f"  → Matched phrase: '{result['matched_phrase']}'")
            else:
                print(f"'{phrase}' → No match found")
            print()


# Example usage
if __name__ == "__main__":
    # Create matcher instance
    matcher = NLPMatcher()
    
    # Test the matcher
    matcher.test_matching()
    
    # Example of adding a custom command
    # matcher.add_custom_command("custom_greeting", ["hello there", "hey assistant", "greetings"])