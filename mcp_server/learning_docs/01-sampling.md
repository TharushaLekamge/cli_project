# How Sampling Works

The flow is straightforward:

1. Server completes its work (e.g., fetching Wikipedia articles)
2. Server creates a prompt asking for text generation
3. Server sends a sampling request to the client
4. Client calls Claude with the provided prompt
5. Client returns the generated text to the server
6. Server uses the generated text in its response

## Benefits of Sampling

- Reduces server complexity: The server doesn't need to integrate with language models directly
- Shifts cost burden: The client pays for token usage, not the server
- No API keys needed: The server doesn't need credentials for Claude
- Perfect for public servers: You don't want a public server racking up AI costs for every user
