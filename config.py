import os
from dotenv import load_dotenv

load_dotenv()

def get_llm_config():
    """
    Returns the LLM configuration based on environment variables.
    Supports both OpenAI and Azure OpenAI.
    """
    use_azure = os.environ.get("USE_AZURE_OPENAI", "false").lower() == "true"
    
    if use_azure:
        # Azure OpenAI configuration
        config_list = [
            {
                "model": os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4"),
                "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
                "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT"),
                "api_type": "azure",
                "api_version": os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            }
        ]
        
        print("Using Azure OpenAI Service")
        print(f"Endpoint: {os.environ.get('AZURE_OPENAI_ENDPOINT')}")
        print(f"Deployment: {os.environ.get('AZURE_OPENAI_DEPLOYMENT')}")
    else:
        # Standard OpenAI configuration
        config_list = [
            {
                "model": os.environ.get("OPENAI_MODEL", "gpt-4"),
                "api_key": os.environ.get("OPENAI_API_KEY"),
            }
        ]
        
        print("Using OpenAI API")
        print(f"Model: {os.environ.get('OPENAI_MODEL', 'gpt-4')}")
    
    llm_config = {
        "config_list": config_list,
        "temperature": float(os.environ.get("TEMPERATURE", "0.7")),
        "timeout": int(os.environ.get("TIMEOUT", "120")),
        "seed": int(os.environ.get("SEED", "42")),
    }
    
    return llm_config

def validate_config():
    """
    Validates that required environment variables are set.
    """
    use_azure = os.environ.get("USE_AZURE_OPENAI", "false").lower() == "true"
    
    if use_azure:
        required_vars = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_DEPLOYMENT"
        ]
        
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            print("Error: Missing required Azure OpenAI environment variables:")
            for var in missing_vars:
                print(f"  - {var}")
            print("\nPlease set these variables in your .env file")
            return False
    else:
        if not os.environ.get("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY is not set in environment variables")
            print("Please set it in your .env file")
            return False
    
    return True