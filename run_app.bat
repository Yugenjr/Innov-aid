@echo off
echo Installing required packages...
pip install -r requirements.txt

echo Starting the Personal Finance Chatbot...
streamlit run app.py

pause
