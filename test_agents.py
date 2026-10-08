#!/usr/bin/env python3
"""
Test script to verify that agents can generate and write code to files
"""

import os
import sys
from dotenv import load_dotenv
from autogen import GroupChat, GroupChatManager
from agents import FrontendAgent, PythonAgent
from config import get_llm_config, validate_config

load_dotenv()

def test_code_generation():
    """Test if agents can generate and write code to files"""
    
    if not validate_config():
        print("Configuration validation failed")
        sys.exit(1)
    
    llm_config = get_llm_config()
    
    # Create workspace directory
    if not os.path.exists("workspace"):
        os.makedirs("workspace")
    
    # Let agents create their own directory structure
    
    # Initialize agents
    frontend_agent = FrontendAgent(llm_config).get_agent()
    python_agent = PythonAgent(llm_config).get_agent()
    
    # Create a simple user proxy for testing
    from autogen import UserProxyAgent
    user_proxy = UserProxyAgent(
        name="test_user",
        system_message="Testing agent code generation",
        code_execution_config={
            "last_n_messages": 2,
            "work_dir": "workspace",
            "use_docker": False,
        },
        human_input_mode="NEVER",  # Automated testing
        max_consecutive_auto_reply=0,
    )
    
    agents = [user_proxy, frontend_agent, python_agent]
    
    # Create group chat
    group_chat = GroupChat(
        agents=agents,
        messages=[],
        max_round=10,
        speaker_selection_method="round_robin",
    )
    
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config
    )
    
    print("\n" + "="*60)
    print("TESTING AGENT CODE GENERATION CAPABILITIES")
    print("="*60)
    
    # Test message - let agents decide structure
    test_message = """
    I need you to build a simple Todo List application.
    
    Frontend Agent: Create a user interface for the todo list with the ability to add, 
    mark as complete, and delete todos. Choose the appropriate technology stack and 
    structure the project as you see fit.
    
    Python Agent: Create a backend API to support the todo list operations (CRUD). 
    Choose your preferred framework and design the architecture as you deem appropriate.
    
    Both agents should implement actual working code and organize it properly.
    """
    
    print("\nSending test request to agents...")
    print("-" * 40)
    
    try:
        user_proxy.initiate_chat(
            manager,
            message=test_message,
        )
    except Exception as e:
        print(f"Error during chat: {e}")
    
    # Check what files were created
    print("\n" + "="*60)
    print("CHECKING GENERATED PROJECT STRUCTURE")
    print("="*60)
    
    print("\nFiles created in workspace directory:")
    for root, dirs, files in os.walk("workspace"):
        level = root.replace("workspace", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
    
    # Show a sample of generated files
    print("\n" + "-"*40)
    print("Sample of generated files:")
    print("-"*40)
    
    for root, dirs, files in os.walk("workspace"):
        for file in files[:3]:  # Show first 3 files as sample
            filepath = os.path.join(root, file)
            print(f"\n📄 {filepath}")
            try:
                with open(filepath, 'r') as f:
                    content = f.read()[:200]
                    print(f"Preview: {content}...")
            except:
                print("(Binary or unreadable file)")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_code_generation()