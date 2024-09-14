from typing import Dict
import json


def load_json(filename: str) -> Dict:
    """Load a json file."""
    with open(filename) as f:
        return json.load(f)


def get_config() -> Dict:
    """Load the config.json file."""
    return load_json("config.json")


def sort_func(name: Dict) -> str:
    """The function to sort by when sorting the free lessons."""
    return name["name"].split(" - ")[1]


def save_to_file(filename: str, data: str) -> None:
    """save data to a file."""
    with open(filename, "w") as f:
        f.write(json.dumps(data))
