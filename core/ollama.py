import ollama
from anthropic.types import Message
from typing import List, Dict, Any
from core.base_llm import BaseLLM


class OllamaMessage:
    """Mock Message class to mimic Anthropic's Message structure."""

    def __init__(self, content: List[Dict[str, str]], role: str = "assistant", model: str = ""):
        self.content = [type('obj', (object,), {'type': 'text', 'text': item['text']})() for item in content]
        self.role = role
        self.model = model
        self.stop_reason = "end_turn"


class Ollama(BaseLLM):
    def __init__(self, model: str = "llama3.2"):
        super().__init__(model)
        self.client = ollama.Client()

        try:
            self.client.show(model)
        except Exception as e:
            print(f"Warning: Model '{model}' not found. You may need to run: ollama pull {model}")
            print(f"Error: {e}")

    def add_user_message(self, messages: list, message):
        user_message = {
            "role": "user",
            "content": message.content
            if isinstance(message, (Message, OllamaMessage))
            else message,
        }
        messages.append(user_message)

    def add_assistant_message(self, messages: list, message):
        assistant_message = {
            "role": "assistant",
            "content": message.content
            if isinstance(message, (Message, OllamaMessage))
            else message,
        }
        messages.append(assistant_message)

    def text_from_message(self, message: OllamaMessage):
        return "\n".join(
            [block.text for block in message.content if hasattr(block, 'text')]
        )

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=None,
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ) -> OllamaMessage:
        """
        Chat with Ollama, mimicking Claude's interface.

        Note: Ollama doesn't support all features like thinking or tools in the same way.
        This adapter focuses on basic chat functionality.
        """
        if stop_sequences is None:
            stop_sequences = []

        ollama_messages = self._convert_messages(messages)

        if system:
            ollama_messages.insert(0, {
                "role": "system",
                "content": system
            })

        options = {
            "temperature": temperature,
            "num_predict": 8000,  # Match Claude's max_tokens
        }

        # Note: stop sequences would need different handling in Ollama
        # Omitting for now as it causes type issues

        # Note: Ollama doesn't have native tool support like Claude
        # Tools would need to be handled separately if needed
        if tools:
            print("Warning: Ollama adapter doesn't fully support tools yet")

        try:
            response = self.client.chat(
                model=self.model,
                messages=ollama_messages,
                tools=tools,
                options=options,
            )

            # Format response to match Claude's structure
            message = response["message"]

            # TOOL CALL PATH
            if "tool_calls" in message and message["tool_calls"]:
                print("tool calling")
                # Convert Ollama tool calls to Claude-compatible format
                content_blocks = []

                # Add any text content first
                if message.get("content"):
                    content_blocks.append({
                        "type": "text",
                        "text": message["content"]
                    })

                # Add tool call blocks
                for tool_call in message["tool_calls"]:
                    # Create a tool_use block that matches Claude's structure
                    tool_block = type('obj', (object,), {
                        'type': 'tool_use',
                        'id': tool_call["function"].get("name", "tool_call"),  # Use name as id
                        'name': tool_call["function"]["name"],
                        'input': tool_call["function"].get("arguments", {})
                    })()
                    content_blocks.append(tool_block)

                ollama_msg = OllamaMessage(
                    content=[{"type": "text", "text": ""}],  # Placeholder
                    role="assistant",
                    model=self.model,
                )
                # Override content with the tool blocks
                ollama_msg.content = content_blocks
                ollama_msg.stop_reason = "tool_use"
                return ollama_msg

            # TEXT PATH
            content_text = message.get("content", "")
            return OllamaMessage(
                content=[{"type": "text", "text": content_text}],
                role="assistant",
                model=self.model,
            )

        except Exception as e:
            print(f"Error calling Ollama: {e}")
            # Return empty message on error
            return OllamaMessage(
                content=[{"type": "text", "text": f"Error: {str(e)}"}],
                role="assistant",
                model=self.model,
            )

    def _convert_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Convert MessageParam format to Ollama message format."""
        ollama_messages = []

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            # Handle different content formats
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                # Extract text from content blocks
                text_parts = []
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                        elif block.get("type") == "tool_result":
                            # Handle tool results
                            text_parts.append(str(block.get("content", "")))
                    elif hasattr(block, 'text'):
                        text_parts.append(block.text)
                    else:
                        text_parts.append(str(block))
                text = " ".join(text_parts)
            else:
                text = str(content)

            ollama_messages.append({
                "role": role,
                "content": text
            })

        return ollama_messages

