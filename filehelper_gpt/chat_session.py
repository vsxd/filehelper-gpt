import os
import logging
from typing import Optional

from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import SQLChatMessageHistory


class ChatSession:
    """Manage a chat conversation using LangChain and store history in SQLite."""

    def __init__(
        self, db_path: str = "chat_history.sqlite", session_id: str = "default"
    ):
        connection = f"sqlite:///{db_path}"
        self.history = SQLChatMessageHistory(
            session_id=session_id, connection_string=connection
        )
        self.memory = ConversationBufferMemory(
            chat_memory=self.history, return_messages=True
        )
        self.chain = ConversationChain(llm=OpenAI(temperature=0.9), memory=self.memory)

    def ask_question(self, question: str) -> str:
        """Return answer from LLM and store conversation in database."""
        return self.chain.run(question)

    def clear(self) -> None:
        """Clear conversation history from SQLite."""
        self.history.clear()

    def __enter__(self) -> "ChatSession":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass
