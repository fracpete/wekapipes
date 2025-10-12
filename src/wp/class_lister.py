from typing import List, Dict


def list_classes() -> Dict[str, List[str]]:
    return {
        "seppl.io.Reader": [
            "wp.reader",
        ],
        "seppl.io.Filter": [
            "wp.filter",
        ],
        "seppl.io.Writer": [
            "wp.writer",
        ],
    }
