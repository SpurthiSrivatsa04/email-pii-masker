import re

# Define regex patterns for PII entities
PII_ENTITIES = {
    "credit_debit_no": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "aadhar_num": r"\b\d{4}([- ]?)\d{4}\1\d{4}\b",
    "dob": (
        r"\b\d{1,2}[-/](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|"
        r"Nov|Dec)[a-z]*[-/]\d{2,4}\b|\b\d{2}[-/]\d{2}[-/]\d{2,4}\b"
    ),
    "expiry_no": r"\b(0[1-9]|1[0-2])[-/](\d{2}|\d{4})\b",
    "email": (
        r"[a-zA-Z0-9_.+-]+(?:[a-zA-Z0-9áéíóúñüÁÉÍÓÚÑÜ]+)?@"
        r"[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+(?=\s|$|[^a-zA-Z0-9])"
    ),
    "full_name": (
        r"\b(?!(?:My|Aadhar|Aadhaar|Credit|Account|Technical|Card|"
        r"Support|Assistance|Needed|State|City|number|ID|Contact|Phone|for)\b)"
        r"([A-ZÀ-ÿ][a-zÀ-ÿ'-]{2,})(?:\s+[A-ZÀ-ÿ][a-zÀ-ÿ'-]+){1,2}"
        r"(?!\s*(?:is|number|no|is:|in|at|from|to|-|:|\.)\b)"
        r"(?<!\b\d)"
    ),
    "phone_number": (
        r"(?:\+?\d{1,3}[-\s]?)?(?:\(\d{1,4}\)|\d{1,4})[-\s]?"
        r"\d{1,4}[-\s]?\d{1,4}(?:[-\s]?\d{1,4}){1,}|\d{10,}"
    ),
    "cvv_no": r"(?<=\D)\d{3}(?=\D)",
}


def mask_pii(text: str) -> tuple[str, list[dict]]:
    """
    Mask PII in text using regex and return masked text with details.

    Args:
        text (str): Input text containing potential PII.

    Returns:
        tuple[str, list[dict]]: Masked text and list of PII entities with
            positions, classifications, and original values.

    Example:
            >>> mask_pii("Contact: John Doe, 1234-5678-9012-3456")
            ('Contact: [full_name], [credit_debit_no]', [
                {'position': [9, 17], 'classification': 'full_name',
                'entity': 'John Doe'},
                {'position': [19, 37], 'classification': 'credit_debit_no',
                'entity': '1234-5678-9012-3456'}
            ])
    """
    # Find all PII matches in the text
    matches = []
    for label, pattern in PII_ENTITIES.items():
        for match in re.finditer(pattern, text):
            start, end = match.span()
            matches.append((start, end, label, match.group()))

    # Sort matches by start position and filter out overlaps
    matches.sort(key=lambda x: x[0])
    non_overlapping = []
    last_end = -1
    for match in matches:
        start, end = match[0], match[1]
        if start >= last_end:
            non_overlapping.append(match)
            last_end = end

    # Build masked text and collect entity details
    masked_text = ""
    last_index = 0
    entities = []
    for start, end, label, entity in non_overlapping:
        masked_text += text[last_index:start] + f"[{label}]"
        entities.append({
            "position": [start, end],
            "classification": label,
            "entity": entity
        })
        last_index = end

    masked_text += text[last_index:]
    return masked_text, entities
