import json
import os
from pathlib import Path

from langchain_core.prompts import PromptTemplate
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage

from logger import log
from langchain_openai import ChatOpenAI
from model_client import get_model_client


def build_prompt_template(code_snippet: str, refactoring_rule: str, detection_rule: str, description:str):
    prompt_template = """
        ### ROLE
        You are a planning assistant for an automatic Java refactoring system.
        Your task is NOT to modify the code, but only to decide whether this occurrence is safe and suitable for automatic refactoring.
        
        ### PMD VIOLATION
        Description: {description}
        Detection Rule: {detection_rule}
        
        ### REFACTORING RECIPE (what the refactoring agent will try to do)
        {refactoring_rule}
        
        ### INPUT CODE
        ```java
        {code_snippet}
        
        ### OUTPUT FORMAT
        You MUST output a single JSON object, and nothing else:
        {{
            "should_refactor": true | false,
            "reason": "very short explanation: why refactor or why skip",
            "scope": "local_block" | "single_method" | "class_wide",
            "risk_level": "low" | "medium" | "high"
        }}
        """
    template = PromptTemplate(
        input_variables=["code_snippet", "refactoring_rule", "detection_rule", "description"],
        template=prompt_template
    )
    final_prompt = template.format(
        code_snippet=code_snippet,
        refactoring_rule=refactoring_rule,
        detection_rule=detection_rule,
        description=description
    )
    return final_prompt


class PlanningAgent:

    async def handle_task(self, code_snippet: str, refactoring_rule: str,
                          detection_rule:str, description: str):
        system_prompt = """
            You are a software‐engineering assistant.  
        """
        prompt = build_prompt_template(code_snippet, refactoring_rule, detection_rule, description)
        log.info(f"PlanningAgent User Prompt: {prompt}")

        result = await get_model_client().create([UserMessage(content=prompt, source="user")])
        log.info(f"PlanningAgent Response: {result.content}")
        return result.content
