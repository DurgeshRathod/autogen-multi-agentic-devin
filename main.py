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

class MultiAgentSystem:
    def __init__(self):
        if not validate_config():
            sys.exit(1)
        
        self.llm_config = get_llm_config()
        
        # Create workspace directory if it doesn't exist
        if not os.path.exists("workspace"):
            os.makedirs("workspace")
            print("Created workspace directory for code generation")
        
        self.user_proxy = UserProxyAgent(
            name="user_proxy",
            system_message="You are the user interacting with the development team.",
            code_execution_config={
                "last_n_messages": 2,
                "work_dir": "workspace",
                "use_docker": False,
            },
            human_input_mode="ALWAYS",
        )
        
        self.frontend_agent = FrontendAgent(self.llm_config).get_agent()
        self.python_agent = PythonAgent(self.llm_config).get_agent()
        self.product_agent = ProductRequirementsAgent(self.llm_config).get_agent()
        self.scrum_master = ScrumMasterAgent(self.llm_config).get_agent()
        self.tester_agent = TesterAgent(self.llm_config).get_agent()
        
        self.agents = [
            self.user_proxy,
            self.product_agent,
            self.scrum_master,
            self.frontend_agent,
            self.python_agent,
            self.tester_agent,
        ]
    
    def create_group_chat(self, max_round=50):
        group_chat = GroupChat(
            agents=self.agents,
            messages=[],
            max_round=max_round,
            speaker_selection_method="auto",
        )
        
        manager = GroupChatManager(
            groupchat=group_chat,
            llm_config=self.llm_config
        )
        
        return group_chat, manager
    
    def start_project(self, initial_message):
        """Start a new project with the given requirements"""
        group_chat, manager = self.create_group_chat()
        
        print("\n" + "="*60)
        print("STARTING MULTI-AGENT DEVELOPMENT TEAM")
        print("="*60)
        print("\nAgents available:")
        for agent in self.agents[1:]:
            print(f"- {agent.name}")
        print("\n" + "="*60 + "\n")
        
        self.user_proxy.initiate_chat(
            manager,
            message=initial_message,
        )
    
    def collaborative_workflow(self):
        """Demonstrate a collaborative workflow between agents"""
        group_chat, manager = self.create_group_chat(max_round=20)
        
        workflow_message = """
        Let's work together to build a simple todo list application.
        
        Product Requirements Agent: Please define the requirements for a basic todo list app.
        Scrum Master: Once requirements are ready, create a sprint plan.
        Frontend Agent: Design the UI components needed.
        Python Agent: Design the backend API.
        Tester Agent: Create a test plan for the application.
        
        Let's collaborate step by step.
        """
        
        self.user_proxy.initiate_chat(
            manager,
            message=workflow_message,
        )

def main():
    system = MultiAgentSystem()
    
    print("\nMulti-Agent Development System")
    print("================================")
    print("\nOptions:")
    print("1. Start a new project")
    print("2. Run collaborative workflow demo")
    print("3. Custom task")
    
    choice = input("\nSelect an option (1-3): ")
    
    if choice == "1":
        project_desc = input("\nDescribe your project requirements: ")
        system.start_project(project_desc)
    elif choice == "2":
        system.collaborative_workflow()
    elif choice == "3":
        custom_task = input("\nEnter your custom task: ")
        system.start_project(custom_task)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()