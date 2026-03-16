import json
import re
from typing import Dict, Any, Optional

from encode_util import detect_encoding
from logger import log


def load_from_json(test_card_filepath):
    with open(test_card_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def parse_json_file(file_path):
    try:
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f:
            raw_content = f.read()

        # 清理内容
        json_data = parse_json_str(raw_content)

        # 解析JSON
        return json_data

    except json.JSONDecodeError as e:
        log.error(f"parse_json_file JSON解析错误: {e}")
        return None
    except Exception as e:
        log.error(f"parse_json_file 处理文件时出错: {e}")
        return None


def extract_first_json_block(text):
    if is_json(text):
        return text

    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
    if match:
        candidate = match.group(1).strip()
        if is_json(candidate):
            return candidate

    json_like_patterns = [
        r'(\{[\s\S]*?\})',
        r'(\[[\s\S]*?\])'
    ]
    for pattern in json_like_patterns:
        for match in re.finditer(pattern, text):
            candidate = match.group(1).strip()
            if is_json(candidate):
                return candidate

    return None


def is_json(s):
    try:
        json.loads(s)
        return True
    except Exception as e:
        print(e)
        return False


def parse_json_str(json_str):
    try:
        cleaned_content = extract_first_json_block(json_str)
        if cleaned_content is None:
            log.error("")
            return None
        return json.loads(cleaned_content)
    except json.JSONDecodeError as e:
        log.error(f"parse_json_str: {e}")
        return None
    except Exception as e:
        log.error(f"parse_json_str : {e}")
        return None
