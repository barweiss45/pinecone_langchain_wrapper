#! /usr/bin/env python3

import json
from typing import Any, Dict, List, Union


def to_json(data: Union[Dict, List]) -> str:
    """
    to_json Convert data to json string
    """
    if isinstance(data, (Dict, List)):
        return json.dumps(data)
    return None


def to_dict(data: str) -> Dict[str, Any]:
    """
    to_dict Convert json string to dictionary
    """
    if isinstance(data, str):
        return json.loads(data)
    return None
