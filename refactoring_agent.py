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
        You are an automatic Java refactoring assistant. 
        Your goal is to fix the following PMD best-practice violation while preserving behavior.
        
        ### REFACTORING RECIPE
        You MUST follow this refactoring recipe step by step:
        {refactoring_rule}
        
        Detection Rule:
        {detection_rule}
        
        Description:
        {description}
        
        ### INPUT CODE
        {code_snippet}
        
        ### CONSTRAINTS
        - Preserve the original behavior as much as possible.
        - Keep the code compilable and consistent with standard Java style.
        - Prefer minimal, local changes that are just enough to fix this violation.
        - Do not change public APIs (public method signatures, public fields) unless the recipe explicitly allows it.

        ### OUTPUT FORMAT
        You MUST output a single JSON object, and nothing else:
        {{
            "status": "refactored" | "skip",
            "reason": "short explanation of what you did or why you skipped",
            "patched_code": "the full updated Java code that should replace the INPUT CODE block"
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


class RefactoringAgent:

    async def handle_task(self, code_snippet: str, refactoring_rule: str,
                          detection_rule:str, description: str):
        system_prompt = """
            You are a software‐engineering assistant.  
        """
        prompt = build_prompt_template(code_snippet, refactoring_rule, detection_rule, description)
        log.info(f"RefactoringAgent User Prompt: {prompt}")

        result = await get_model_client().create([UserMessage(content=prompt, source="user")])
        log.info(f"RefactoringAgent Response: {result.content}")
        return result.content
