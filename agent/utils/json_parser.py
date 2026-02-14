import json
import re

def extract_json(text: str) -> dict:
    """
    Robust JSON extractor for LLM outputs with multiline strings.
    """

    # 1. Extract JSON object

    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in LLM output")

    json_str = match.group()

    # 2. First attempt: normal JSON

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass  

    # 3. Repair multiline string values ONLY
    
    def fix_multiline_strings(match):
        content = match.group(1)
        content = content.replace("\n", "\\n")
        return f"\"{content}\""

    repaired = re.sub(
        r"\"([\s\S]*?)\"",
        fix_multiline_strings,
        json_str
    )

    return json.loads(repaired)
