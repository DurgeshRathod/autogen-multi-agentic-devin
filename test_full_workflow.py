#!/usr/bin/env python3
"""
Full workflow test demonstrating agents building and testing an application
"""

import os
import sys
from dotenv import load_dotenv
from autogen import GroupChat, GroupChatManager, UserProxyAgent
from agents import (
    FrontendAgent,
    PythonAgent,
    ProductRequirementsAgent,
    ScrumMasterAgent,
    TesterAgent
)
from config import get_llm_config, validate_config

load_dotenv()

def run_full_development_cycle():
    """Run a complete development cycle with building and testing"""
    
    if not validate_config():
        print("Configuration validation failed")
        sys.exit(1)
    
    llm_config = get_llm_config()
    
    # Create workspace directory
    if not os.path.exists("workspace"):
        os.makedirs("workspace")
        print("Created workspace directory")
    
    # Initialize all agents
    user_proxy = UserProxyAgent(
        name="user_proxy",
        system_message="You are the product owner with a vision for the application.",
        code_execution_config={
            "last_n_messages": 2,
            "work_dir": "workspace",
            "use_docker": False,
        },
        human_input_mode="ALWAYS",
    )
    
    product_agent = ProductRequirementsAgent(llm_config).get_agent()
    scrum_master = ScrumMasterAgent(llm_config).get_agent()
    frontend_agent = FrontendAgent(llm_config).get_agent()
    python_agent = PythonAgent(llm_config).get_agent()
    tester_agent = TesterAgent(llm_config).get_agent()
    
    agents = [
        user_proxy,
        product_agent,
        scrum_master,
        frontend_agent,
        python_agent,
        tester_agent,
    ]
    
    # Create group chat with extended rounds for full cycle
    group_chat = GroupChat(
        agents=agents,
        messages=[],
        max_round=100,  # More rounds for complete development cycle
        speaker_selection_method="auto",
    )
    
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config
    )
    
    print("\n" + "="*60)
    print("FULL DEVELOPMENT CYCLE WITH AUTOMATED TESTING")
    print("="*60)
    print("\nAgents participating:")
    for agent in agents[1:]:
        print(f"  ✓ {agent.name}")
    print("="*60 + "\n")
    
    # Full development cycle message
    development_message = """
    Let's build a complete Todo List application with the following workflow:
    
    1. Product Requirements Agent: Define detailed requirements for a todo list app including:
       - User stories and acceptance criteria
       - Feature prioritization
       - Non-functional requirements (performance, security, usability)
    
    2. Scrum Master: Create a sprint plan breaking down the work into tasks
    
    3. Frontend Agent: 
       - Design and implement the UI
       - Create all necessary HTML, CSS, and JavaScript files
       - Ensure the frontend can connect to the backend API
       - Make it responsive and user-friendly
    
    4. Python Agent:
       - Design and implement a REST API backend
       - Create endpoints for CRUD operations on todos
       - Set up proper data persistence (file-based or SQLite)
       - Include proper error handling and validation
       - Create a requirements.txt for dependencies
    
    5. Tester Agent:
       - Start the backend server
       - Open the frontend in a browser
       - Write and execute automated tests for both frontend and backend
       - Test the API endpoints
       - Perform UI testing
       - Create a test report with findings
       - Report any bugs found
    
    Each agent should create actual working code and save it to files.
    The tester should actually run and test the application.
    
    Let's begin!
    """
    
    try:
        user_proxy.initiate_chat(
            manager,
            message=development_message,
        )
    except Exception as e:
        print(f"Error during development cycle: {e}")
    
    # Display final project structure
    print("\n" + "="*60)
    print("FINAL PROJECT STRUCTURE")
    print("="*60)
    
    for root, dirs, files in os.walk("workspace"):
        level = root.replace("workspace", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
    
    print("\n" + "="*60)
    print("DEVELOPMENT CYCLE COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_full_development_cycle()