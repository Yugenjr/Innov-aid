#!/usr/bin/env python3
"""
End-to-end test for the Finance App
Tests both backend API and frontend integration
"""

import requests
import json
import time
import subprocess
import sys
import os
from typing import Dict, Any

class FinanceAppTester:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:5173"
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "✓" if success else "✗"
        self.test_results.append({
            "name": test_name,
            "success": success,
            "message": message
        })
        print(f"{status} {test_name}: {message}")
    
    def test_backend_health(self) -> bool:
        """Test backend health endpoint"""
        try:
            response = requests.get(f"{self.backend_url}/api/health", timeout=5)
            if response.status_code == 200:
                self.log_test("Backend Health", True, "Server is running")
                return True
            else:
                self.log_test("Backend Health", False, f"Status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Backend Health", False, f"Connection failed: {e}")
            return False
    
    def test_chat_api(self) -> bool:
        """Test chat API with different scenarios"""
        test_cases = [
            {
                "name": "Student Mode Chat",
                "payload": {
                    "user_input": "How can I save money as a college student?",
                    "user_mode": "student",
                    "scenario_context": ""
                }
            },
            {
                "name": "Professional Mode Chat",
                "payload": {
                    "user_input": "What's the best investment strategy for retirement?",
                    "user_mode": "professional",
                    "scenario_context": ""
                }
            },
            {
                "name": "Emergency Fund Scenario",
                "payload": {
                    "user_input": "Build an emergency fund",
                    "user_mode": "student",
                    "scenario_context": "Emergency Fund: Building emergency savings step by step"
                }
            }
        ]
        
        all_passed = True
        for test_case in test_cases:
            try:
                response = requests.post(
                    f"{self.backend_url}/api/chat", 
                    json=test_case["payload"], 
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "response" in data and data["response"]:
                        self.log_test(
                            test_case["name"], 
                            True, 
                            f"Provider: {data.get('provider', 'unknown')}"
                        )
                    else:
                        self.log_test(test_case["name"], False, "Empty response")
                        all_passed = False
                else:
                    self.log_test(test_case["name"], False, f"Status {response.status_code}")
                    all_passed = False
                    
            except requests.exceptions.RequestException as e:
                self.log_test(test_case["name"], False, f"Request failed: {e}")
                all_passed = False
        
        return all_passed
    
    def test_finance_endpoints(self) -> bool:
        """Test finance calculation endpoints"""
        tests = [
            {
                "name": "Budget Analysis",
                "endpoint": "/api/budget/analyze",
                "payload": {
                    "monthly_income": 3000,
                    "rent": 1000,
                    "utilities": 150,
                    "insurance": 200,
                    "food": 400,
                    "transportation": 300,
                    "entertainment": 200,
                    "other": 150
                }
            },
            {
                "name": "Investment Calculation",
                "endpoint": "/api/invest/calc",
                "payload": {
                    "initial_investment": 1000,
                    "monthly_investment": 300,
                    "annual_return_pct": 7,
                    "years": 20
                }
            },
            {
                "name": "Savings Projection",
                "endpoint": "/api/savings/project",
                "payload": {
                    "target_amount": 10000,
                    "current_amount": 2000,
                    "monthly_contribution": 500
                }
            }
        ]
        
        all_passed = True
        for test in tests:
            try:
                response = requests.post(
                    f"{self.backend_url}{test['endpoint']}", 
                    json=test["payload"], 
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(test["name"], True, "Calculation successful")
                else:
                    self.log_test(test["name"], False, f"Status {response.status_code}")
                    all_passed = False
                    
            except requests.exceptions.RequestException as e:
                self.log_test(test["name"], False, f"Request failed: {e}")
                all_passed = False
        
        return all_passed
    
    def test_frontend_accessibility(self) -> bool:
        """Test if frontend is accessible"""
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                self.log_test("Frontend Accessibility", True, "Frontend is accessible")
                return True
            else:
                self.log_test("Frontend Accessibility", False, f"Status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Frontend Accessibility", False, f"Connection failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Finance App End-to-End Testing")
        print("=" * 50)
        
        # Test backend
        print("\n📡 Testing Backend...")
        backend_health = self.test_backend_health()
        
        if backend_health:
            chat_tests = self.test_chat_api()
            finance_tests = self.test_finance_endpoints()
        else:
            print("⚠️  Skipping API tests due to backend health failure")
            chat_tests = False
            finance_tests = False
        
        # Test frontend
        print("\n🌐 Testing Frontend...")
        frontend_tests = self.test_frontend_accessibility()
        
        # Summary
        print("\n📊 Test Summary")
        print("-" * 30)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        for result in self.test_results:
            status = "✓" if result["success"] else "✗"
            print(f"{status} {result['name']}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! The system is working correctly.")
            return True
        else:
            print("⚠️  Some tests failed. Please check the issues above.")
            return False

def main():
    tester = FinanceAppTester()
    success = tester.run_all_tests()
    
    if not success:
        print("\n💡 Troubleshooting Tips:")
        print("1. Make sure both backend and frontend servers are running")
        print("2. Backend should be on http://127.0.0.1:8000")
        print("3. Frontend should be on http://localhost:5173")
        print("4. Check console logs for detailed error messages")
        print("5. Try running: python start_app.py")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
