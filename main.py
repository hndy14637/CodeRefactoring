import asyncio
import json
from typing import List

from json_util import parse_json_str
from logger import log
from planning_agent import PlanningAgent
from refactoring_agent import RefactoringAgent
from smell_detection_agent import detection_result_parsing, RefactoringItem
from verification_agent import VerificationAgent

async def coordinate_agents():
    refactoring_agent = RefactoringAgent()
    planning_agent = PlanningAgent()
    verification_agent = VerificationAgent()

    # Detection
    refactoring_list: List[RefactoringItem] = detection_result_parsing()

    refactoring_index = 1
    for refactoring_item in refactoring_list:
        filename = refactoring_item.filename

        # Planning
        planning_resp = await planning_agent.handle_task(
            refactoring_item.code_snippet,
            refactoring_item.refactoring_rule,
            refactoring_item.rule,
            refactoring_item.description
        )
        planning_result = parse_json_str(planning_resp)
        should_refactor = str(planning_result['should_refactor']).lower()
        if not should_refactor or should_refactor.__contains__("false"):
            log.info("refactoring rejection")
            with open(f"refactoring_rejection_#{str(refactoring_index)}.json", 'w') as f:
                json.dump(planning_result, f, ensure_ascii=False, indent=2)
            continue

        # Refactoring
        refactoring_resp = await refactoring_agent.handle_task(
            refactoring_item.code_snippet,
            refactoring_item.refactoring_rule,
            refactoring_item.rule,
            refactoring_item.description
        )
        refactoring_result = parse_json_str(refactoring_resp)
        with open(f"refactoring_result_#{str(refactoring_index)}.json", 'w') as f:
            json.dump(refactoring_result, f, ensure_ascii=False, indent=2)

        # Verification
        verification_resp = await verification_agent.handle_task(
            refactoring_item.code_snippet,
            refactoring_item.refactoring_rule,
            refactoring_item.rule,
            refactoring_item.description,
            refactoring_resp
        )
        verification_result = parse_json_str(verification_resp)
        with open(f"refactoring_verification_#{str(refactoring_index)}.json", 'w') as f:
            json.dump(verification_result, f, ensure_ascii=False, indent=2)

        refactoring_index = refactoring_index + 1

if __name__ == '__main__':
    asyncio.run(coordinate_agents())
