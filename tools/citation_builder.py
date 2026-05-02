"""
Tool: Citation Builder
Responsibility: Parse and format citations from agent responses.
Ensures evaluators can trace every claim back to a page.
"""

import re
from typing import List, Dict
from utils.logger import get_logger

logger = get_logger("tool.citation_builder")


def extract_citations(response_text: str) -> List[Dict]:
    """
    Extract page citations from the model's response.
    The model is prompted to use format: [Page X] or [Pages X, Y]
    """
    pattern = r"\[Page[s]?\s*([\d,\s]+)\]"
    matches = re.findall(pattern, response_text, re.IGNORECASE)

    citations = []
    for match in matches:
        page_nums = [int(p.strip()) for p in match.split(",") if p.strip().isdigit()]
        for page in page_nums:
            if {"page": page} not in citations:
                citations.append({"page": page})

    logger.debug(f"Citations found: {citations}")
    return citations


def build_citation_footer(citations: List[Dict]) -> str:
    """
    Build a clean citation footer for display in the UI.
    """
    if not citations:
        return ""
    pages = sorted(set(c["page"] for c in citations))
    page_str = ", ".join(f"p.{p}" for p in pages)
    return f"📄 Source: {page_str}"
