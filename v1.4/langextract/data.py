
import dataclasses
import enum
from typing import Dict, List, Any, Optional

class FormatType(enum.Enum):
    YAML = "yaml"
    JSON = "json"

@dataclasses.dataclass
class CharInterval:
    start_pos: int | None = None
    end_pos: int | None = None

@dataclasses.dataclass
class Extraction:
    extraction_class: str
    extraction_text: str
    char_interval: CharInterval | None = None
    description: str | None = None
    attributes: Dict[str, str | List[str]] | None = None

@dataclasses.dataclass
class ExampleData:
    text: str
    extractions: List[Extraction] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class Document:
    text: str
    additional_context: str | None = None

@dataclasses.dataclass
class AnnotatedDocument:
    extractions: List[Extraction] | None = None
    text: str | None = None
