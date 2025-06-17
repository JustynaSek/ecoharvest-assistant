---
title: EcoHarvest Assistant
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.19.2
app_file: app.py
pinned: false
---

# EcoHarvest Assistant

An AI-powered assistant that provides comprehensive information about EcoHarvest products and support services. The assistant uses specialized agents to handle different types of queries, ensuring accurate and relevant responses.

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/JustynaSek86/ecoharvest_assistant)

## Technical Description
AI-powered assistant for EcoHarvest products, featuring RAG-based product information, technical support, and automated query routing. Built with Gradio, it provides instant access to product specs, troubleshooting guides, and maintenance procedures.

## Features

- Intelligent query routing to specialized agents
- Product information database with detailed specifications
- Support knowledge base for troubleshooting
- Real-time chat interface
- Modern, responsive UI
- Automatic context management
- Comprehensive error handling
- Support information database integration

## Example Prompts

Here are some example prompts that demonstrate the RAG (Retrieval-Augmented Generation) capabilities of our agents:

### Product Information Queries
```
1. "What is the warranty period for the EcoHarvest GrowPod?"
2. "Can I grow multiple types of plants in one GrowPod?"
```

### Technical Support Queries
```
1. "How do I troubleshoot if my GrowPod's pump is making unusual noise?"
2. "What maintenance procedures are required for the GrowPod?"
```

### General Inquiries
```
1. "How do I connect my GrowPod to the mobile app?"
2. "My name is XYZ, send me a welcome notification."
```

Each query is processed through our RAG system, which:
1. Analyzes the query to determine the appropriate agent
2. Searches the relevant knowledge base (product or support)
3. Retrieves the most relevant information
4. Generates a contextual response based on the retrieved information

The system ensures that responses are:
- Based on factual information from our knowledge bases
- Contextually relevant to the specific query
- Free from confidential or sensitive information
- Helpful and actionable

## Capabilities

### Product Information
- Detailed product specifications
- Pricing and availability
- Warranty information
- Compatibility details
- Product features and benefits

### Technical Support
- Troubleshooting guides
- Maintenance procedures
- Technical assistance
- Common issues and solutions
- System diagnostics
- Support knowledge base queries
- Technical documentation access
- Error resolution guidance

### General Assistance
- Account notifications
- System status updates
- General inquiries
- Service information

## Local Development Setup

### Prerequisites

- Python 3.8 or higher
- Package manager (pip or uv)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://huggingface.co/spaces/JustynaSek86/ecoharvest_assistant
cd ecoharvest_assistant
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

Using pip (recommended for Hugging Face Spaces):
```bash
pip install -r requirements.txt
```

Using uv (faster alternative):
```bash
# Install uv first
pip install uv

# Then install dependencies
uv pip install -r requirements.txt
```

Note: While `uv` is faster and more modern, we recommend using `pip` for Hugging Face Spaces deployment as it's the standard package manager supported by the platform.

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
OPENAI_API_KEY=your_api_key_here
PUSHOVER_TOKEN=your_pushover_token_here
PUSHOVER_USER=your_pushover_user_here
```

### Running the Application

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:7860
```

## Project Structure

```
ecoharvest_assistant/
├── app.py                    # Main application entry point
├── gradio_interface.py       # Gradio interface configuration
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
└── src/                     # Source code directory
    ├── my_agents/           # AI agents implementation
    │   ├── product_info_agent/    # Product information agent
    │   ├── support_info_agent/    # Support information agent
    │   │   ├── support_info_agent.py      # Main support agent implementation
    │   │   ├── support_info_agent_tools.py # Support agent tools and RAG components
    │   │   └── support_info_guardrail.py   # Support query safety checks
    │   ├── triage_agent/          # Request routing agent
    │   ├── notification_agent/    # Notification handling agent
    ├── data/                # Data files and knowledge bases
    ├── tools/               # Utility tools and helpers
    └── gradio_interface.py  # Additional Gradio components
```

## How It Works

The EcoHarvest Assistant uses a multi-agent system to handle different types of queries:

1. **Triage Agent**: Analyzes incoming queries and routes them to the appropriate specialized agent
2. **Product Information Agent**: Handles all product-related queries
3. **Support Information Agent**: 
   - Manages technical support and troubleshooting queries
   - Accesses the support knowledge base for accurate information
   - Provides step-by-step troubleshooting guidance
   - Handles maintenance and technical assistance queries
   - Implements safety checks for sensitive support information
4. **Notification Agent**: Handles system notifications and alerts

The system automatically determines the most appropriate agent for each query, ensuring that users receive accurate and relevant information without needing to specify which type of agent they want to use.

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 