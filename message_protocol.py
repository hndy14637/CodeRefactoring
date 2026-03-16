import json
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class DefectPatternMatchingTask:
    repo_owner: str
    repo_name: str
    defect_title: str
    patch_source_code: str
    patch_fixed: str
    tpl_source_code: str

@dataclass
class DefectTask:
    prompt: str
    repo_owner: str
    repo_name: str
    title: str
    number: int
    url: str
    body: str
    related_issues: str

    # self-adaptive mechanism
    # agent update
    comment_info: str
    is_comment_context_complete: bool
    is_comment_context_sufficient: bool
    comment_history_context: str
    comment_adaptive_message: str

    code_change_info: str
    is_code_change_context_complete: bool
    is_code_change_context_sufficient: bool
    code_change_history_context: str
    code_change_adaptive_message: str

    def get_context_sufficiency(self, model_response: str, type: str) -> bool:
        try:
            key = ''
            if type == 'comment':
                key = 'is_comment_context_sufficient'
            elif type == 'code_change':
                key = 'is_code_change_context_sufficient'
            is_context_sufficient = None
            if not is_context_sufficient:
                return False
            if isinstance(is_context_sufficient, bool):
                return is_context_sufficient
            if isinstance(is_context_sufficient, str):
                return is_context_sufficient.lower() in ('true', 'yes')
            return False
        except (json.JSONDecodeError, AttributeError):
            return False




@dataclass
class TaskResult:
    result: str


@dataclass
class FinalResult:
    result: Any
