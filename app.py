from flask import Flask, request, jsonify, render_template
import json
import re
from datetime import datetime
import os
import requests

app = Flask(__name__)

class MicrofinanceBot:
    def __init__(self):
        self.user_sessions = {}
        
    def process_message(self, message, user_id):
        """Process user message and return appropriate response"""
        message = message.lower().strip()
        
        # Initialize user session if not exists
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'step': 'welcome',
                'loan_amount': None,
                'business_type': None,
                'documents_ready': None
            }
        
        session = self.user_sessions[user_id]
        
        # Intent recognition
        intent = self.recognize_intent(message)
        
        # Generate response based on intent and session
        return self.generate_response(intent, message, session)
    
    def recognize_intent(self, message):
        """Simple intent recognition"""
        if any(word in message for word in ['apply', 'loan', 'borrow', 'money', 'need']):
            return 'apply_loan'
        elif any(word in message for word in ['program', 'type', 'offer', 'available']):
            return 'loan_programs'
        elif any(word in message for word in ['document', 'need', 'require', 'paper']):
            return 'documents_needed'
        elif any(word in message for word in ['repayment', 'pay', 'payment', 'term']):
            return 'repayment_questions'
        elif any(word in message for word in ['rate', 'interest', 'cost', 'charge']):
            return 'interest_rates'
        elif any(word in message for word in ['connect', 'speak', 'talk', 'officer']):
            return 'connect_officer'
        elif any(word in message for word in ['yes', 'have', 'ready', 'got']):
            return 'documents_ready'
        elif any(word in message for word in ['no', 'missing', 'help', 'assistance']):
            return 'help_documents'
        else:
            return 'general'
    
    def generate_response(self, intent, message, session):
        """Generate bot response based on intent and session state"""
        
        if intent == 'apply_loan':
            session['step'] = 'business_info'
            return {
                'text': "Great! I'd be happy to help you apply for a loan. To get started, could you tell me a bit about your business or income source?",
                'quick_replies': [
                    "I have a small business",
                    "I work for someone", 
                    "I need emergency funds"
                ]
            }
        
        elif intent == 'loan_programs':
            return {
                'text': "We offer several loan programs designed specifically for women entrepreneurs:\n\n• Small Business Loans: $500 - $5,000\n• Emergency Loans: $200 - $1,000\n• Education Loans: $1,000 - $3,000\n\nAll loans have flexible repayment terms and low interest rates. Would you like to apply?",
                'quick_replies': [
                    "Yes, I want to apply",
                    "Tell me more about requirements",
                    "What are the interest rates?"
                ]
            }
        
        elif intent == 'documents_needed':
            return {
                'text': "For loan applications, you'll need:\n\n• Valid ID (passport, driver's license)\n• Proof of income (pay stubs, business records)\n• Bank statements (last 3 months)\n• Two references\n• Business plan (for business loans)\n\nDo you have these documents ready?",
                'quick_replies': [
                    "Yes, I have them",
                    "I need help getting some documents",
                    "Let me apply anyway"
                ]
            }
        
        elif intent == 'repayment_questions':
            return {
                'text': "Our repayment terms are very flexible:\n\n• Weekly, bi-weekly, or monthly payments\n• Grace period of 2 weeks for emergencies\n• No penalties for early repayment\n• We work with you if you face difficulties\n\nWould you like to speak with someone about your specific situation?",
                'quick_replies': [
                    "Yes, connect me with someone",
                    "Tell me more about loan programs"
                ]
            }
        
        elif intent == 'interest_rates':
            return {
                'text': "Our interest rates are very competitive:\n\n• Small Business Loans: 8-12% annually\n• Emergency Loans: 10-15% annually\n• Education Loans: 6-10% annually\n\nThese rates are much lower than traditional lenders and designed to be affordable for women entrepreneurs. Would you like to apply?",
                'quick_replies': [
                    "Yes, I want to apply",
                    "Tell me about requirements"
                ]
            }
        
        elif intent == 'documents_ready':
            session['step'] = 'business_info'
            return {
                'text': "Excellent! Since you have your documents ready, let's get started with your loan application. Could you tell me a bit about your business or income source?",
                'quick_replies': [
                    "I have a small business",
                    "I work for someone",
                    "I need emergency funds"
                ]
            }
        
        elif intent == 'help_documents':
            return {
                'text': "No worries! We understand that getting documents can be challenging. Here's how we can help:\n\n• **ID Documents**: We accept expired IDs up to 6 months past expiry\n• **Income Proof**: We can work with verbal income verification for small amounts\n• **Bank Statements**: We accept mobile money statements or cash deposit records\n• **References**: Family members or community leaders can serve as references\n• **Business Plan**: We can help you create a simple business plan\n\nWould you like to speak with a loan officer who can guide you through getting these documents?",
                'quick_replies': [
                    "Yes, connect me with someone",
                    "Let me apply anyway"
                ]
            }
        
        elif intent == 'connect_officer':
            session['step'] = 'completed'
            return {
                'text': "I'm connecting you with one of our loan officers now. They will call you within the next 24 hours to discuss your application and answer any questions. Thank you for choosing Women's Empowerment Microfinance! 🌟",
                'quick_replies': []
            }
        
        else:
            # Handle conversation flow based on session state
            if session['step'] == 'business_info':
                # Extract business type from message
                if any(word in message for word in ['business', 'shop', 'store', 'sell']):
                    session['business_type'] = 'business'
                elif any(word in message for word in ['work', 'job', 'employee', 'salary']):
                    session['business_type'] = 'employment'
                elif any(word in message for word in ['emergency', 'urgent', 'need']):
                    session['business_type'] = 'emergency'
                
                session['step'] = 'loan_amount'
                return {
                    'text': "Thank you for sharing that information. Now, could you tell me approximately how much you're looking to borrow? This will help me guide you to the right loan program.",
                    'quick_replies': []
                }
            
            elif session['step'] == 'loan_amount':
                # Extract amount from message
                amount_match = re.search(r'\d+', message)
                if amount_match:
                    amount = int(amount_match.group())
                    session['loan_amount'] = amount
                    
                    # Determine loan type based on amount
                    if 500 <= amount <= 5000:
                        loan_type = "Small Business Loan"
                    elif 200 <= amount < 500:
                        loan_type = "Emergency Loan"
                    elif 1000 <= amount <= 3000:
                        loan_type = "Education Loan"
                    else:
                        loan_type = "Custom Loan"
                    
                    session['step'] = 'completed'
                    return {
                        'text': f"Perfect! Based on the amount you mentioned (${amount}), I'd recommend our {loan_type} program. I have all the information I need to help you get started. Let me connect you with one of our experienced loan officers who will guide you through the application process and answer any specific questions you may have.",
                        'quick_replies': []
                    }
                else:
                    return {
                        'text': "Could you please specify the amount you'd like to borrow? For example, you can say '$1000' or 'one thousand dollars'.",
                        'quick_replies': []
                    }
            
            else:
                return {
                    'text': "I understand you're interested in our services. Let me connect you with one of our loan officers who can provide personalized assistance.",
                    'quick_replies': [
                        "Connect me with someone",
                        "Tell me about loan programs"
                    ]
                }

# Initialize bot
bot = MicrofinanceBot()

def send_facebook_message(recipient_id, message_text, quick_replies=None):
    """Send message to Facebook Messenger"""
    page_access_token = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN')
    
    if not page_access_token:
        print("ERROR: FACEBOOK_PAGE_ACCESS_TOKEN not set")
        return False
    
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={page_access_token}"
    
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    
    # Add quick replies if provided
    if quick_replies:
        payload["message"]["quick_replies"] = [
            {"content_type": "text", "title": reply, "payload": reply}
            for reply in quick_replies
        ]
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Message sent successfully to {recipient_id}")
            return True
        else:
            print(f"Failed to send message: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return False

@app.route('/')
def home():
    """Serve the chatbot interface"""
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming messages from the chatbot interface"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        sender = data.get('sender', 'web-user')
        
        # Process message through bot
        response = bot.process_message(message, sender)
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint for deployment platforms"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Microfinance Chatbot'
    })

@app.route('/test')
def test():
    """Test endpoint"""
    return jsonify({
        'message': 'Python Microfinance Bot is running!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/debug/facebook')
def debug_facebook():
    """Debug endpoint to check Facebook configuration"""
    token = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN')
    return jsonify({
        'has_token': bool(token),
        'token_length': len(token) if token else 0,
        'token_preview': token[:10] + '...' if token else None,
        'timestamp': datetime.now().isoformat()
    })

# Facebook Messenger webhook endpoints
@app.route('/facebook/webhook', methods=['GET'])
def facebook_webhook_verify():
    """Facebook webhook verification"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    verify_token = 'shakti_webhook_2024'
    
    if mode == 'subscribe' and token == verify_token:
        return challenge
    else:
        return 'Forbidden', 403

@app.route('/facebook/webhook', methods=['POST'])
def facebook_webhook():
    """Handle Facebook Messenger messages"""
    try:
        data = request.get_json()
        
        if data.get('object') == 'page':
            for entry in data.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    sender_id = messaging_event['sender']['id']
                    
                    if messaging_event.get('message'):
                        message_text = messaging_event['message']['text']
                        
                        # Process message through bot
                        response = bot.process_message(message_text, sender_id)
                        
                        # Send response back to Facebook
                        send_facebook_message(sender_id, response['text'], response.get('quick_replies'))
                        
            return 'OK', 200
        else:
            return 'Not Found', 404
            
    except Exception as e:
        return 'Internal Server Error', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 