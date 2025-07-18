# Women's Empowerment Microfinance Chatbot

A Python Flask-based chatbot designed to help women entrepreneurs with loan applications and microfinance services.

## Features

- **Intelligent Conversation Flow**: Handles loan applications step-by-step
- **Multiple Loan Programs**: Small Business, Emergency, and Education loans
- **Document Guidance**: Helps users understand required documents
- **Quick Reply Buttons**: Easy-to-use interface with suggested responses
- **Facebook Messenger Integration**: Ready for Facebook Messenger deployment
- **Session Management**: Remembers user progress through applications

## Loan Programs

- **Small Business Loans**: $500 - $5,000 (8-12% annual interest)
- **Emergency Loans**: $200 - $1,000 (10-15% annual interest)
- **Education Loans**: $1,000 - $3,000 (6-10% annual interest)

## Quick Start

### Local Development

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Access the chatbot**:
   - Web Interface: http://localhost:5000
   - Health Check: http://localhost:5000/health
   - Test Endpoint: http://localhost:5000/test

### Deployment on Railway

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/python-microfinance-bot.git
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Connect your GitHub repository to Railway
   - Railway will automatically detect Python and deploy
   - Your bot will be available at your Railway URL

## API Endpoints

- `GET /` - Web interface
- `POST /webhook` - Chatbot message processing
- `GET /health` - Health check
- `GET /test` - Test endpoint
- `GET /facebook/webhook` - Facebook webhook verification
- `POST /facebook/webhook` - Facebook message handling

## Facebook Messenger Integration

To connect with Facebook Messenger:

1. Create a Facebook App
2. Add Messenger product
3. Set webhook URL to: `https://your-railway-url/facebook/webhook`
4. Set verify token to: `shakti_webhook_2024`
5. Subscribe to messaging events

## Conversation Flow

1. **Welcome** → User greeted with loan options
2. **Intent Recognition** → Bot understands user's request
3. **Business Info** → Collects business/income information
4. **Loan Amount** → Determines appropriate loan program
5. **Document Check** → Verifies document readiness
6. **Connection** → Links user with loan officer

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Railway
- **Messaging**: Facebook Messenger API

## Contributing

Feel free to contribute to improve the chatbot's functionality and user experience.

## License

MIT License 