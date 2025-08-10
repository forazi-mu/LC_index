#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from main import app
    print("App imported successfully")
    
    with app.test_client() as client:
        response = client.get('/health')
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.get_json()}")
        
        response = client.get('/')
        print(f"Index page status: {response.status_code}")
        print(f"Index page content length: {len(response.data)}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

