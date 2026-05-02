"""
Tool: PDF Extractor
Responsibility: Read a PDF and return structured page-by-page text.
This separation (tool vs agent) is the key to industry-standard agent design.
"""

import fitz  # PyMuPDF
from typing import Dict
from utils.logger import get_logger

logger = get_logger("tool.pdf_extractor")


def extract_pages(pdf_bytes: bytes) -> Dict[int, str]:
    """
    Extract text from each page of a PDF.
    Returns: { page_number: page_text }
    Page numbers are 1-indexed (human-readable).
    """
    logger.info("Starting PDF extraction")
    pages: Dict[int, str] = {}

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = len(doc)
        logger.info(f"PDF loaded — {total_pages} pages found")

        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text("text").strip()
            if text:
                pages[page_num + 1] = text  # 1-indexed
                logger.debug(f"Page {page_num + 1}: extracted {len(text)} chars")
            else:
                logger.warning(f"Page {page_num + 1}: no text found (image-only?)")

        doc.close()
        logger.info(f"Extraction complete — {len(pages)} pages with text")
        return pages

    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        raise


def format_for_context(pages: Dict[int, str]) -> str:
    """
    Format the page dict into a clean string for the LLM context.
    Each page is clearly delimited so the model can cite page numbers.
    """
    sections = []
    for page_num, text in pages.items():
        sections.append(f"[PAGE {page_num}]\n{text}")
    return "\n\n---\n\n".join(sections)
