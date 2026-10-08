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

def run_example_workflow():
    """
    Demonstrates how the multi-agent system works together on a project
    """
    
    if not validate_config():
        sys.exit(1)
    
    llm_config = get_llm_config()
    
    user_proxy = UserProxyAgent(
        name="user_proxy",
        system_message="You are the product owner with a project idea.",
        code_execution_config={
            "last_n_messages": 2,
            "work_dir": "workspace",
            "use_docker": False,
        },
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
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
    
    group_chat = GroupChat(
        agents=agents,
        messages=[],
        max_round=15,
        speaker_selection_method="round_robin",
    )
    
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config
    )
    
    print("\n" + "="*80)
    print("EXAMPLE: Building an E-commerce Product Page")
    print("="*80)
    
    example_project = """
    Project: E-commerce Product Display Page
    
    I need to build a product display page for an e-commerce website with the following requirements:
    1. Show product images, title, price, and description
    2. Add to cart functionality
    3. Customer reviews section
    4. Related products recommendation
    5. Responsive design for mobile and desktop
    
    Product Requirements Agent: Please analyze and create detailed requirements.
    Scrum Master: Break this down into sprint tasks.
    Frontend Agent: Suggest the frontend implementation approach.
    Python Agent: Design the backend API structure.
    Tester Agent: Create a testing strategy.
    """
    
    user_proxy.initiate_chat(
        manager,
        message=example_project,
    )

def run_automated_examples():
    """
    Run several pre-defined example scenarios
    """
    
    examples = [
        {
            "name": "User Authentication System",
            "description": """
            Build a secure user authentication system with:
            - User registration with email verification
            - Login/logout functionality
            - Password reset feature
            - Session management
            - Role-based access control
            """
        },
        {
            "name": "Real-time Chat Application",
            "description": """
            Create a real-time chat application with:
            - One-on-one messaging
            - Group chat rooms
            - Message history
            - Online status indicators
            - File sharing capability
            """
        },
        {
            "name": "Task Management Dashboard",
            "description": """
            Develop a task management dashboard with:
            - Create, read, update, delete tasks
            - Task categorization and tagging
            - Due date tracking
            - Progress visualization
            - Team collaboration features
            """
        }
    ]
    
    print("\n" + "="*80)
    print("AUTOMATED EXAMPLE SCENARIOS")
    print("="*80)
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   {example['description'][:100]}...")
    
    print("\nThese examples demonstrate how different agents collaborate on various project types.")

if __name__ == "__main__":
    print("\nMulti-Agent System Examples")
    print("============================")
    print("\n1. Run interactive example workflow")
    print("2. View automated example scenarios")
    
    choice = input("\nSelect option (1-2): ")
    
    if choice == "1":
        run_example_workflow()
    elif choice == "2":
        run_automated_examples()
    else:
        print("Invalid choice.")