# Ollama Adapter - Quick Start Guide

## Overview

The Ollama adapter allows you to use local open-source LLMs instead of cloud-based Claude API. This provides:
- **Privacy**: All data stays on your machine
- **No API costs**: Free to use
- **Offline capability**: Works without internet
- **Speed**: Fast responses with good hardware

## Installation

### 1. Install Ollama

Download from: https://ollama.ai

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download installer from https://ollama.ai

### 2. Start Ollama Service

Ollama typically starts automatically. To verify:
```bash
ollama --version
ollama list
```

### 3. Pull a Model

```bash
# Recommended starter model (2GB)
ollama pull llama3.2

# Other options:
ollama pull mistral      # 4GB
ollama pull codellama    # 7GB - great for coding
ollama pull phi3         # 2GB - Microsoft's efficient model
```

### 4. Configure Your Project

Edit `.env`:
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
USE_UV=1
```

### 5. Install Python Dependencies

```bash
uv pip install -e .
# or
pip install ollama
```

### 6. Run Your Chat

```bash
uv run main.py
# or
python main.py
```

You should see: `🦙 Using Ollama with model: llama3.2`

## Choosing the Right Model

| Model | Size | Best For | Speed |
|-------|------|----------|-------|
| llama3.2 | 2GB | General chat, Q&A | Fast |
| mistral | 4GB | Balanced performance | Medium |
| codellama | 7GB | Code generation | Medium |
| phi3 | 2GB | Quick responses | Very Fast |
| gemma2 | 9GB | High quality output | Slower |

## Troubleshooting

### "Model not found"
```bash
ollama pull <model-name>
```

### Ollama not running
```bash
# macOS/Linux
ollama serve

# Or restart the Ollama app
```

### Slow responses
- Use a smaller model (phi3, llama3.2)
- Check your RAM usage
- Consider upgrading hardware

### Connection errors
```bash
# Check if Ollama is accessible
curl http://localhost:11434/api/tags
```

## Limitations vs Claude

The Ollama adapter currently has these limitations:
- ⚠️ **No tool/function calling support** (tools parameter ignored)
- ⚠️ **No thinking mode** (thinking parameter ignored)
- ✅ Basic chat works perfectly
- ✅ Document retrieval works
- ✅ Multi-turn conversations work

## Performance Tips

1. **Use GPU**: Ollama automatically uses GPU if available
2. **Adjust context size**: Larger contexts = slower but more memory
3. **Temperature**: Lower (0.3-0.7) = more focused, Higher (0.8-1.0) = more creative
4. **Keep Ollama updated**: `brew upgrade ollama` or download latest version

## Advanced Configuration

You can customize Ollama behavior by modifying `core/ollama.py`:

```python
options = {
    "temperature": temperature,
    "num_predict": 8000,    # Max tokens to generate
    "top_k": 40,            # Top-k sampling
    "top_p": 0.9,           # Nucleus sampling
    "repeat_penalty": 1.1,  # Penalize repetition
}
```

## Switching Back to Claude

Edit `.env`:
```env
LLM_PROVIDER=claude
CLAUDE_MODEL=claude-sonnet-4-5
ANTHROPIC_API_KEY=your_key_here
```

Restart the application. No code changes needed!

## Resources

- Ollama Documentation: https://github.com/ollama/ollama
- Model Library: https://ollama.ai/library
- Python Client: https://github.com/ollama/ollama-python

