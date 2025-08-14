# Finance App Testing Guide

This guide helps you test the Finance App to ensure everything is working correctly.

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
python start_app.py
```
This script will:
- Check prerequisites (Python, Node.js)
- Install dependencies
- Start both backend and frontend servers
- Provide helpful URLs

### Option 2: Manual Setup
1. **Start Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start Frontend (in new terminal):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Testing the Application

### 1. Automated Testing
Run the comprehensive test suite:
```bash
python test_full_system.py
```

This will test:
- ✅ Backend API health
- ✅ Chat functionality (student/professional modes)
- ✅ Finance calculations (budget, savings, investment)
- ✅ Frontend accessibility

### 2. Manual Testing

#### Backend API Testing
```bash
python test_backend_api.py
```

#### Frontend Testing
1. Open http://localhost:5173
2. Test sign-in form validation:
   - Try invalid email formats
   - Try short passwords
   - Check error messages
   - Test loading states

3. Test chat functionality:
   - Switch between student/professional modes
   - Try the quick scenario buttons
   - Send custom messages
   - Check response formatting
   - Verify error handling

## What to Look For

### ✅ Sign-in Form Should:
- Validate email format in real-time
- Require password minimum length
- Show loading state during submission
- Display clear error messages
- Have password visibility toggle

### ✅ Chat Interface Should:
- Display messages with proper formatting
- Show loading indicators while processing
- Handle API errors gracefully
- Format AI responses with bullet points and numbering
- Show provider information (Granite AI, Gemini AI, etc.)
- Scroll automatically to new messages

### ✅ Model Responses Should:
- Be relevant to the user's question
- Differ between student and professional modes
- Include structured advice (numbered lists, bullet points)
- Handle financial scenarios appropriately
- Provide fallback responses if AI models fail

## Troubleshooting

### Backend Issues
- **Port 8000 already in use**: Kill existing processes or use different port
- **Module not found**: Run `pip install -r backend/requirements.txt`
- **CORS errors**: Check ALLOW_ORIGINS in backend/.env

### Frontend Issues
- **Port 5173 already in use**: Frontend will automatically try next available port
- **API connection failed**: Ensure backend is running on port 8000
- **Build errors**: Run `npm install` in frontend directory

### Common Problems
1. **Chat not working**: Check browser console for API errors
2. **Responses not formatted**: Verify the formatResponse function is working
3. **Sign-in validation not working**: Check browser console for JavaScript errors

## Expected Test Results

When everything is working correctly, you should see:
- ✅ All automated tests passing
- ✅ Sign-in form with proper validation
- ✅ Chat responses formatted with structure
- ✅ Error handling for network issues
- ✅ Loading states throughout the app

## API Endpoints

The backend provides these endpoints:
- `GET /api/health` - Health check
- `POST /api/chat` - Chat with AI
- `POST /api/budget/analyze` - Budget analysis
- `POST /api/savings/project` - Savings projection
- `POST /api/invest/calc` - Investment calculation
- `POST /api/speech/transcribe` - Speech to text
- `POST /api/speech/tts` - Text to speech

## Environment Configuration

Backend configuration (backend/.env):
```
GRANITE_MODEL_ID=ibm-granite/granite-3.1-1b-a400m-instruct
GEMINI_API_KEY=your_key_here
ALLOW_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Frontend automatically connects to backend on localhost:8000.

## Success Criteria

The application is working correctly when:
1. All tests in `test_full_system.py` pass
2. Sign-in form validates properly
3. Chat responses are well-formatted and relevant
4. Error states are handled gracefully
5. Loading states provide good user feedback
