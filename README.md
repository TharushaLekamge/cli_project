Now update the readme # MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models. The application supports both cloud-based (Claude via Anthropic API) and local (Ollama) LLM providers, along with document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.9+
- **For Claude**: Anthropic API Key
- **For Ollama**: [Ollama](https://ollama.ai) installed locally

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and set your preferred LLM provider:

**For Ollama (Local LLM - Recommended for privacy):**
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2  # or mistral, codellama, etc.
USE_UV=1
```

**For Claude (Cloud-based):**
```env
LLM_PROVIDER=claude
CLAUDE_MODEL=claude-sonnet-4-5
ANTHROPIC_API_KEY=your_api_key_here
USE_UV=1
```

### Step 2: Install Ollama (if using Ollama provider)

1. Download and install Ollama from [https://ollama.ai](https://ollama.ai)

2. Pull your preferred model:

```bash
ollama pull llama3.2
# or
ollama pull mistral
ollama pull codellama
```

3. Verify Ollama is running:

```bash
ollama list
```

### Step 3: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0" ollama
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

### Switching Between LLM Providers

To switch between Claude and Ollama, simply update the `LLM_PROVIDER` variable in your `.env` file:

**Switch to Ollama:**
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

**Switch to Claude:**
```env
LLM_PROVIDER=claude
CLAUDE_MODEL=claude-sonnet-4-5
ANTHROPIC_API_KEY=your_api_key_here
```

No code changes are required - the application will automatically use the selected provider on next run.

### Available Ollama Models

Popular models you can use with Ollama:
- `llama3.2` - Meta's Llama 3.2 (recommended)
- `mistral` - Mistral AI's model
- `codellama` - Code-specialized Llama
- `phi3` - Microsoft's Phi-3
- `gemma2` - Google's Gemma 2

Pull any model with: `ollama pull <model-name>`

## Development

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Implementing MCP Features

To fully implement the MCP features:

1. Complete the TODOs in `mcp_server.py`
2. Implement the missing functionality in `mcp_client.py`

### Linting and Typing Check

There are no lint or type checks implemented.
