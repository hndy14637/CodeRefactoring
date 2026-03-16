import asyncio
import os
from dataclasses import dataclass
from typing import List, Optional

from autogen_core import AgentId, MessageContext, RoutedAgent, SingleThreadedAgentRuntime, message_handler
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

def get_model_client(model_name: Optional[str] = None):
    # default value
    if not model_name:
        model_name = "deepseek-v3"

    model_client = OpenAIChatCompletionClient(
        model=model_name,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model_info={
            "vision": True,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
        },
    )
    return model_client
