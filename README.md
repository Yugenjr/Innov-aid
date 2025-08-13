# Personal Finance Chatbot

An intelligent conversational AI system that provides personalized financial guidance using IBM's Granite AI model.

## Features

### 🤖 AI-Powered Financial Advisor
- Powered by IBM Granite 3.1-1b model
- Personalized financial advice
- Context-aware responses
- Demographic-specific guidance (students vs professionals)

### 💬 Interactive Chatbot
- Natural language conversations
- Pre-built financial scenarios
- Chat history tracking
- Quick-start scenario buttons

### 📊 Budget Tracker
- Monthly income and expense tracking
- Visual expense breakdown
- 50/30/20 rule comparison
- Budget analysis and recommendations

### 💰 Savings Goals
- Goal setting and tracking
- Progress visualization
- Savings projections
- Automated savings tips

### 📈 Investment Guide
- Investment basics education
- Risk assessment tools
- Portfolio recommendations
- Investment calculator

## Financial Scenarios Covered

1. **Student Loan Repayment** - Guidance for managing and paying off student loans
2. **Budget Summary** - Help with creating and maintaining budgets
3. **Emergency Fund** - Building emergency savings step by step
4. **Spending Analysis** - Identifying and reducing unnecessary expenses
5. **Savings Recommendations** - Practical savings strategies
6. **Financial Stress** - Supportive guidance for financial anxiety

## Quick Start

### Option 1: Using the batch file (Windows)
1. Double-click `run_app.bat`
2. Wait for installation to complete
3. The app will open in your browser automatically

### Option 2: Manual installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run app.py
   ```

3. Open your browser to `http://localhost:8501`

## Usage

1. **Home Page**: Overview of features and quick navigation
2. **Finance Chatbot**: 
   - Click "Load AI Model" to initialize the IBM Granite model
   - Use scenario buttons for quick starts
   - Type custom questions in the chat interface
3. **Budget Tracker**: Input your income and expenses for analysis
4. **Savings Goals**: Set and track your financial goals
5. **Investment Guide**: Learn about investing and portfolio allocation

## Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **IBM Granite 3.1-1b**: AI model for text generation
- **Transformers**: Hugging Face library for model integration
- **Plotly**: Interactive charts and visualizations
- **PyTorch**: Deep learning framework

## Model Information

This application uses IBM's Granite 3.1-1b-a400m-instruct model:
- Lightweight and efficient
- Optimized for instruction following
- Suitable for financial advice generation
- Runs locally for privacy

## Notes

- First run may take longer due to model download (~2-3GB)
- Model loading requires adequate RAM (4GB+ recommended)
- Fallback responses available if model fails to load
- All data stays local - no external API calls for chat

## Disclaimer

This application provides educational financial information only and should not be considered as professional financial advice. Always consult with qualified financial advisors for important financial decisions.
