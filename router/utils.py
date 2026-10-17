def clean_markdown_fences(text: str) -> str:
    """
    Removes common markdown code fences so downstream JSON parsers don't break.
    Keeps behavior compatible with your current _clean_response().
    """
    if not text:
        return text
    t = text.strip()
    if t.startswith("```json"):
        t = t.replace("```json", "", 1)
        if t.endswith("```"):
            t = t[:-3]
    elif t.startswith("```"):
        t = t.replace("```", "", 1)
        if t.endswith("```"):
            t = t[:-3]
    return t.strip()
