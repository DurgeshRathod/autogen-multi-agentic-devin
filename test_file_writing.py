#!/usr/bin/env python3
"""
Test script to verify AutoGen agents can write files to workspace
"""

import os
import sys
from dotenv import load_dotenv
from autogen import GroupChat, GroupChatManager, UserProxyAgent
from agents import FrontendAgent
from config import get_llm_config, validate_config

load_dotenv()

def test_file_writing():
    """Test that agents can write files to workspace"""
    if not validate_config():
        print("Configuration validation failed")
        sys.exit(1)
    
    llm_config = get_llm_config()
    
    # Create workspace directory if it doesn't exist
    if not os.path.exists("workspace"):
        os.makedirs("workspace")
        print("Created workspace directory")
    
    # Create a simple test with just user proxy and frontend agent
    user_proxy = UserProxyAgent(
        name="user_proxy",
        system_message="You are the user interacting with the frontend developer. Execute any Python code that the frontend agent provides.",
        code_execution_config={
            "last_n_messages": 2,
            "work_dir": "workspace",
            "use_docker": False,
        },
        human_input_mode="NEVER",  # Automated test
        max_consecutive_auto_reply=10,  # Allow auto-reply to execute code
    )
    
    frontend_agent = FrontendAgent(llm_config).get_agent()
    
    # Create group chat with just these two agents
    group_chat = GroupChat(
        agents=[user_proxy, frontend_agent],
        messages=[],
        max_round=5,
        speaker_selection_method="auto",
    )
    
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config
    )
    
    # Test message that should trigger file creation
    test_message = """
    Create a simple HTML file called test.html in the workspace directory with the following:
    - A title "Test Page"
    - A heading "Hello World"
    - A paragraph saying "This is a test file created by AutoGen"
    
    IMPORTANT: Actually write this file to workspace/test.html using Python code.
    """
    
    print("\n" + "="*60)
    print("TESTING FILE WRITING CAPABILITY")
    print("="*60)
    
    user_proxy.initiate_chat(
        manager,
        message=test_message,
    )
    
    # Check if the file was created
    test_file_path = "workspace/test.html"
    if os.path.exists(test_file_path):
        print("\n" + "="*60)
        print("SUCCESS: File was created!")
        print("="*60)
        with open(test_file_path, 'r') as f:
            print("\nFile contents:")
            print(f.read())
        return True
    else:
        print("\n" + "="*60)
        print("FAILURE: File was not created")
        print("="*60)
        return False

if __name__ == "__main__":
    success = test_file_writing()
    sys.exit(0 if success else 1)