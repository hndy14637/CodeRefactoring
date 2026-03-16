import os
import time
import json
import subprocess
import pathlib
from dataclasses import dataclass

import requests
from typing import List, Optional
import subprocess
import json

from config_loader import get


def run_pmd(project_path, ruleset_path, pmd_home):
    cmd = [
        f"{pmd_home}/bin/pmd",
        "check",
        "-d", project_path,
        "-R", ruleset_path,
        "-f", "json"
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.stderr.strip():
        print("PMD stderr:", result.stderr)

    return result.stdout  # JSON string


def best_practice_detection():
    target_repo_dir = get('settings', 'target_repo_dir')
    print("target_repo_dir:", target_repo_dir)
    json_output = run_pmd(
        project_path=target_repo_dir,
        ruleset_path="category/java/bestpractices.xml",
        pmd_home="detection/pmd-bin-7.19.0"
    )

    return json_output


@dataclass
class RefactoringItem:
    filename: str
    start_line: int
    end_line: int
    rule: str
    description: str

    refactoring_rule: str
    code_snippet: str


def get_rule_content(key, rules_dir='refactoring_rules'):
    filename = f"{key}.rule"

    if not os.path.exists(rules_dir):
        return None

    for file in os.listdir(rules_dir):
        if file == filename:
            filepath = os.path.join(rules_dir, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            except IOError:
                return None

    return None


def fetch_code_snippet(filename: str, start_line: int, end_line: int) -> str:
    if start_line < 1 or end_line < start_line:
        raise ValueError(f"Invalid range: start_line={start_line}, end_line={end_line}")

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)

    safe_start = max(1, start_line)
    safe_end = min(end_line, total_lines)

    snippet_lines = lines[safe_start - 1: safe_end]

    snippet = "".join(snippet_lines)

    return snippet


def detection_result_parsing():
    json_output = best_practice_detection()
    detection_result = json.loads(json_output)
    with open('experimental/json-main/detection_result.json', 'w') as f:
        json.dump(detection_result, f, ensure_ascii=False, indent=2)
    files = detection_result['files']
    refactoring_list = []
    for f in files:
        filename = f['filename']
        for violation in f['violations']:
            rule_content = get_rule_content(violation['rule'])
            if not rule_content:
                continue
            code_snippet = fetch_code_snippet(filename, violation['beginline'], violation['endline'])
            refactoring_item = RefactoringItem(
                filename=filename,
                start_line=violation['beginline'],
                end_line=violation['endline'],
                rule=violation['rule'],
                description=violation['description'],
                refactoring_rule=rule_content,
                code_snippet=code_snippet
            )
            refactoring_list.append(refactoring_item)
    return refactoring_list

if __name__ == '__main__':
    detection_result_parsing()
