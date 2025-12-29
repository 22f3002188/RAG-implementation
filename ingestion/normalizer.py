from typing import Dict, List


def normalize_ocr_layout(ocr_data: Dict) -> str:
    """
    Normalize OCR output using layout information (line order).
    No hardcoding, no UI assumptions, no rules added.
    """

    lines: Dict[int, List[str]] = {}

    for i in range(len(ocr_data["text"])):
        text = ocr_data["text"][i].strip()
        if not text:
            continue

        line_num = ocr_data["line_num"][i]
        lines.setdefault(line_num, []).append(text)

    ordered_lines = [
        " ".join(words)
        for _, words in sorted(lines.items(), key=lambda x: x[0])
    ]

    normalized_text = (
        "The following text was extracted from a user interface screenshot "
        "in top-to-bottom visual order. No interaction logic is implied.\n"
        "- " + "\n- ".join(ordered_lines)
    )

    return normalized_text
