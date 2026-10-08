# Multi-Agent Development Team with AutoGen

A sophisticated multi-agent system built with Microsoft AutoGen that simulates a complete software development team. Each agent specializes in different aspects of the development lifecycle.

## Agents

### 1. **Frontend Agent**
- Specializes in React, Vue, Angular, and modern web frameworks
- Handles UI/UX design, responsive layouts, and frontend optimization
- Implements accessibility standards and cross-browser compatibility

### 2. **Python Agent**
- Expert in backend development with Python
- Designs APIs, database schemas, and microservices
- Handles authentication, security, and performance optimization

### 3. **Product Requirements Agent**
- Analyzes business requirements and user needs
- Creates user stories with acceptance criteria
- Prioritizes features and defines success metrics

### 4. **Scrum Master Agent**
- Facilitates agile ceremonies and sprint planning
- Tracks team velocity and removes blockers
- Ensures adherence to Scrum methodology

### 5. **Tester Agent**
- Develops comprehensive test strategies
- Creates test cases for all testing levels
- Performs automated and manual testing
- Ensures quality standards are met

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API credentials:
```bash
cp .env.example .env
```

### Using OpenAI API
Edit `.env` and add:
```
OPENAI_API_KEY=your_openai_api_key_here
USE_AZURE_OPENAI=false
```

### Using Azure OpenAI
Edit `.env` and add:
```
USE_AZURE_OPENAI=true
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

## Usage

### Interactive Mode
Run the main script to interact with the multi-agent system:

```bash
python main.py
```

Options:
1. **Start a new project** - Describe your requirements and watch agents collaborate
2. **Run collaborative workflow demo** - See agents work together on a todo app
3. **Custom task** - Provide any development task for the team

### Example Workflows
Run predefined examples to see the system in action:

```bash
python example_workflow.py
```

## How It Works

1. **User provides requirements** - You describe what you want to build
2. **Product Requirements Agent** - Analyzes and structures the requirements
3. **Scrum Master** - Creates sprint plans and coordinates the team
4. **Development Agents** - Frontend and Python agents design the solution
5. **Tester Agent** - Creates test plans and quality assurance strategies
6. **Collaborative iteration** - Agents work together, providing feedback and refining the solution

## Project Structure

```
multi-agentic-exploration/
├── agents/
│   ├── __init__.py
│   ├── frontend_agent.py
│   ├── python_agent.py
│   ├── product_requirements_agent.py
│   ├── scrum_master_agent.py
│   └── tester_agent.py
├── workspace/              # Code execution workspace
├── main.py                # Main orchestrator
├── example_workflow.py    # Example demonstrations
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md
```

## Features

- **Automated collaboration** - Agents communicate and coordinate automatically
- **Role-based expertise** - Each agent has specialized knowledge
- **Flexible workflows** - Supports various development methodologies
- **Code execution** - Agents can write and test actual code
- **Interactive or automated** - Run interactively or use predefined workflows

## Requirements

- Python 3.8+
- API key for either:
  - OpenAI API (GPT-4 recommended)
  - Azure OpenAI Service
- AutoGen library

## Example Use Cases

- Building web applications
- API development
- Creating authentication systems
- Developing dashboards
- Implementing chat applications
- Any software development project requiring team collaboration

## Notes

- The system uses GPT-4 by default for optimal performance
- Agents can execute code in the workspace directory
- Human input mode can be adjusted for different levels of automation
- The group chat manager coordinates agent interactions automatically