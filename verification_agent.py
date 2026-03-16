import json
import os
from pathlib import Path

from langchain_core.prompts import PromptTemplate
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage

from logger import log
from langchain_openai import ChatOpenAI
from model_client import get_model_client


def build_prompt_template(code_snippet: str, refactoring_rule: str,
                          detection_rule: str, description:str, patched_code:str):
    prompt_template = """
        ### ROLE
        You are a verification assistant for an automatic Java refactoring system.
        Your task is to **check** the patch produced by the refactoring agent, not to generate new code.
        
        ### PMD VIOLATION
        - Description: {description}
        - Detection rule: {detection_rule}
        
        ### REFACTORING RECIPE
        {refactoring_rule}
        
        ### ORIGINAL CODE
        {code_snippet}
        
        ### PATCHED CODE
        {patched_code}
        
        ### DECISION RULES
        - If the patch clearly removes the violation AND does not introduce suspicious behavior/API changes, return "accept".
        - If the patch seems incorrect, incomplete, or changes behavior/API in a suspicious way, return "reject".
        - If you are unsure (e.g., the change is too complex to reason about), return "uncertain".
        
        ### OUTPUT FORMAT
        You MUST output a single JSON object, and nothing else:
        {{
            "verdict": "accept" | "reject" | "uncertain",
            "still_violates_rule": true | false,
            "description": 1-3 sentences
        }}
        """
    template = PromptTemplate(
        input_variables=["code_snippet", "refactoring_rule", "detection_rule", "description", "patched_code"],
        template=prompt_template
    )
    final_prompt = template.format(
        code_snippet=code_snippet,
        refactoring_rule=refactoring_rule,
        detection_rule=detection_rule,
        description=description,
        patched_code=patched_code
    )
    return final_prompt


class VerificationAgent:
    async def handle_task(self, code_snippet: str, refactoring_rule: str,
                          detection_rule:str, description: str, patched_code:str):
        system_prompt = """
            You are a software‐engineering assistant.  
        """
        prompt = build_prompt_template(code_snippet, refactoring_rule, detection_rule,
                                       description, patched_code)
        log.info(f"VerificationAgent User Prompt: {prompt}")

        result = await get_model_client().create([UserMessage(content=prompt, source="user")])
        log.info(f"VerificationAgent Response: {result.content}")
        return result.content
