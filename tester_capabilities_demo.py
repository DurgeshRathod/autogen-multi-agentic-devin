#!/usr/bin/env python3
"""
Demonstration of tester agent capabilities for running and testing applications
"""

import os
import sys
from dotenv import load_dotenv
from autogen import UserProxyAgent
from agents import TesterAgent
from config import get_llm_config, validate_config

load_dotenv()

def demonstrate_tester_capabilities():
    """Show how the tester agent can run and test applications"""
    
    if not validate_config():
        print("Configuration validation failed")
        sys.exit(1)
    
    llm_config = get_llm_config()
    
    # Create workspace directory
    if not os.path.exists("workspace"):
        os.makedirs("workspace")
    
    # Create a simple test application for demonstration
    print("Setting up demo application...")
    
    # Create a simple HTML file
    os.makedirs("workspace/demo", exist_ok=True)
    
    with open("workspace/demo/index.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Demo Todo App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        #todoList { list-style-type: none; padding: 0; }
        .todo-item { padding: 10px; margin: 5px; background: #f0f0f0; }
    </style>
</head>
<body>
    <h1>Todo List Demo</h1>
    <input type="text" id="todoInput" placeholder="Enter a todo...">
    <button onclick="addTodo()">Add Todo</button>
    <ul id="todoList"></ul>
    
    <script>
        function addTodo() {
            const input = document.getElementById('todoInput');
            const list = document.getElementById('todoList');
            if (input.value) {
                const li = document.createElement('li');
                li.className = 'todo-item';
                li.textContent = input.value;
                list.appendChild(li);
                input.value = '';
            }
        }
    </script>
</body>
</html>""")
    
    # Create a simple Python backend
    with open("workspace/demo/api.py", "w") as f:
        f.write("""from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

todos = []

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    todo = request.json
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("Starting Flask API server on http://localhost:5000")
    app.run(debug=True, port=5000)
""")
    
    # Initialize agents
    user_proxy = UserProxyAgent(
        name="demo_user",
        system_message="Demonstrating tester capabilities",
        code_execution_config={
            "last_n_messages": 2,
            "work_dir": "workspace",
            "use_docker": False,
        },
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
    )
    
    tester_agent = TesterAgent(llm_config).get_agent()
    
    print("\n" + "="*60)
    print("TESTER AGENT CAPABILITIES DEMONSTRATION")
    print("="*60)
    
    # Test message demonstrating various capabilities
    test_message = """
    Please demonstrate your testing capabilities:
    
    1. First, install any necessary testing dependencies (like requests for API testing)
    
    2. Write a Python test script that:
       - Tests the Flask API health endpoint at http://localhost:5000/api/health
       - Tests adding todos via POST request
       - Tests retrieving todos via GET request
       - Save this as workspace/demo/test_api.py
    
    3. Write a simple browser automation test that:
       - Opens the index.html file in a browser
       - Simulates adding a todo item
       - Save this as workspace/demo/test_ui.py
    
    4. Create a test report summarizing:
       - What was tested
       - Test results
       - Any issues found
       - Save this as workspace/demo/test_report.md
    
    Note: Since we're in demo mode, you can write the test scripts even if the server isn't running.
    Focus on showing your ability to create comprehensive test code.
    """
    
    print("\nAsking tester agent to demonstrate capabilities...")
    print("-" * 40)
    
    try:
        user_proxy.initiate_chat(
            tester_agent,
            message=test_message,
        )
    except Exception as e:
        print(f"Error during demonstration: {e}")
    
    # Show created test files
    print("\n" + "="*60)
    print("TEST FILES CREATED")
    print("="*60)
    
    test_files = [
        "workspace/demo/test_api.py",
        "workspace/demo/test_ui.py", 
        "workspace/demo/test_report.md"
    ]
    
    for filepath in test_files:
        if os.path.exists(filepath):
            print(f"\n✓ Created: {filepath}")
            with open(filepath, 'r') as f:
                content = f.read()[:300]
                print(f"Preview:\n{content}...")
        else:
            print(f"\n✗ Not created: {filepath}")
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nThe tester agent can:")
    print("  ✓ Write and execute test scripts")
    print("  ✓ Start backend servers")
    print("  ✓ Open applications in browsers")
    print("  ✓ Perform API testing")
    print("  ✓ Perform UI automation testing")
    print("  ✓ Generate test reports")

if __name__ == "__main__":
    demonstrate_tester_capabilities()