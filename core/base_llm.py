from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class BaseLLM(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def add_user_message(self, messages: list, message) -> None:
        """
        Add a user message to the message list.

        Args:
            messages: List of messages
            message: Message to add (can be string, dict, or Message object)
        """
        pass

    @abstractmethod
    def add_assistant_message(self, messages: list, message) -> None:
        """
        Add an assistant message to the message list.

        Args:
            messages: List of messages
            message: Message to add (can be string, dict, or Message object)
        """
        pass

    @abstractmethod
    def text_from_message(self, message) -> str:
        """
        Extract text content from a message.

        Args:
            message: Message object

        Returns:
            Extracted text as string
        """
        pass

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, Any]],
        system: Optional[str] = None,
        temperature: float = 1.0,
        stop_sequences: Optional[List[str]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        thinking: bool = False,
        thinking_budget: int = 1024,
    ):
        """
        Send a chat request to the LLM.

        Args:
            messages: List of message dictionaries
            system: System prompt
            temperature: Sampling temperature
            stop_sequences: List of stop sequences
            tools: List of available tools
            thinking: Enable thinking mode (if supported)
            thinking_budget: Token budget for thinking

        Returns:
            Message response from the LLM
        """
        pass

