import json
import re
import sys
from dataclasses import asdict, dataclass


@dataclass
class Tool:
    name: str
    url: str
    description: str
    language: str


README_FILE = sys.argv[1]
METADATA_FILE = sys.argv[2]

template_pattern = r"- \[(.*?)\]\((.*?)\) - (.*?)\. \`([^\`]+)\`"
matches = re.findall(template_pattern, open(README_FILE).read())
tools = [asdict(Tool(*match)) for match in matches]
metadata_content = {"total": len(tools), "tools": tools}

with open(METADATA_FILE, "w+") as file:
    json.dump(metadata_content, file, indent=2)
