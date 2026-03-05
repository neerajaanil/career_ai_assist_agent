# Career AI Assist Agent

An intelligent AI agentic system that assists in answering questions about career background, skills, and experience using OpenAI GPT models. This project demonstrates expertise in building production-ready AI agentic systems with tool calling, context management, and interactive conversational interfaces.

🌐 **Live Demo**: [Try it on Hugging Face Spaces](https://huggingface.co/spaces/neerajaanil/career_conversations)

## About This Project

This project showcases advanced AI agentic system development, featuring:

- **Intelligent Agent Architecture**: Built with a modular, extensible agent framework that leverages OpenAI's function calling capabilities
- **Context-Aware Conversations**: Seamlessly integrates multiple data sources (LinkedIn profiles, career summaries) to provide accurate, personalized responses
- **Tool Integration**: Implements custom tools for user interaction tracking, notifications, and data recording
- **Production-Ready Design**: Includes proper error handling, logging, configuration management, and scalable architecture patterns
- **Interactive UI**: Modern Gradio-based interface for seamless user interactions

This system demonstrates practical expertise in building AI agentic systems that can autonomously handle complex conversational tasks, make decisions about tool usage, and maintain context across interactions—essential skills for developing next-generation AI applications.

## Technical Architecture & AI Agentic Capabilities

### Core Agentic Features

- **Autonomous Tool Selection**: The agent intelligently decides when and which tools to use based on conversation context, demonstrating true agentic behavior
- **Multi-Turn Reasoning**: Implements iterative tool calling with up to 10 iterations, allowing the agent to chain multiple operations and reason through complex queries
- **Dynamic Context Management**: Maintains conversation history and context across multiple interactions, enabling coherent multi-turn dialogues
- **Error Handling & Resilience**: Robust error handling for API failures, tool execution errors, and edge cases, ensuring reliable production operation

### System Architecture

- **Modular Design**: Clean separation of concerns with dedicated modules for agent logic, data loading, tool definitions, and configuration
- **Extensible Tool Framework**: Easy-to-extend tool system that allows adding new capabilities without modifying core agent logic
- **Type-Safe Configuration**: Strongly-typed configuration management with validation and environment variable support
- **Production Patterns**: Implements logging, structured error handling, and configuration validation following industry best practices

### AI/ML Engineering

- **LLM Integration**: Deep understanding of OpenAI's Chat Completions API, function calling, and message formatting
- **Prompt Engineering**: Sophisticated system prompts that guide agent behavior and ensure consistent, professional responses
- **RAG Implementation**: Retrieval-Augmented Generation pattern using structured data sources (PDF parsing, text summarization)
- **Conversational AI**: Advanced chat interface with history management and context preservation

## Setup & Local Testing

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Internet connection

### Step-by-Step Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd career_ai_assist_agent
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - The `.env` file template is already in the repository
   - Edit `.env` and add your OpenAI API key:
   ```bash
   # Required
   OPENAI_API_KEY=sk-your-actual-api-key-here
   AGENT_NAME=Your Name
   
   # Optional
   OPENAI_MODEL=gpt-4o-mini
   PUSHOVER_TOKEN=
   PUSHOVER_USER=
   SERVER_HOST=0.0.0.0
   SERVER_PORT=7860
   SHARE=false
   ```

5. **Prepare data files:**
   - Ensure you have the following files in the `data/` directory:
     - `linkedin.pdf`: Your LinkedIn profile exported as PDF
     - `summary.txt`: A text summary of your career background
   - If these files don't exist, create placeholder files or the app will show an error

6. **Run the application:**
   ```bash
   python run.py
   ```
   
   Or alternatively:
   ```bash
   python -m career_ai_assist_agent.app
   ```

7. **Access the application:**
   - The application will start and display a URL in the terminal
   - Typically: `http://localhost:7860`
   - Open this URL in your browser to start chatting with the agent

### Testing the Application

Once the app is running:

1. **Open the browser** to the displayed URL (usually `http://localhost:7860`)
2. **Try example questions** like:
   - "What is your background?"
   - "Tell me about your experience"
   - "What skills do you have?"
   - "What projects have you worked on?"
3. **Verify the agent responds** with information from your LinkedIn profile and summary
4. **Check the terminal** for any error messages or logs

### Troubleshooting

- **"OPENAI_API_KEY environment variable is required"**: Make sure your `.env` file has a valid API key
- **"LinkedIn PDF not found"**: Ensure `data/linkedin.pdf` exists
- **"Summary file not found"**: Ensure `data/summary.txt` exists
- **Port already in use**: Change `SERVER_PORT` in `.env` to a different port (e.g., 7861)
- **Module not found errors**: Make sure you've activated your virtual environment and installed dependencies

## Usage

### Online Demo

Try the live deployment on Hugging Face Spaces: [https://huggingface.co/spaces/neerajaanil/career_conversations](https://huggingface.co/spaces/neerajaanil/career_conversations)

### Local Deployment

After following the setup instructions above, the application will be available at `http://localhost:7860` (or the port specified in your `.env` file). Open your browser to the displayed URL and start chatting with the agent about career background, skills, and experience.

## Key Technologies & Skills

- **AI/ML**: OpenAI GPT-4, Function Calling, Agentic AI Systems
- **Python**: Object-Oriented Design, Type Hints, Async Patterns
- **LLM Engineering**: Prompt Engineering, RAG, Context Management
- **Software Architecture**: Modular Design, Extensibility, Production Patterns
- **Tools**: Gradio, PyPDF, Python-dotenv, OpenAI SDK

## Requirements

- Python 3.8+
- OpenAI API key
