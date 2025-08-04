This directory contains LangExtract components that have been adapted for vllm compatability. Download these components for reuse or use the following snippet to generate your own!

Required:

- schema.py  
- prompting.py  
- inference.py  
- data.py  
- "__init__.py" 

To generate, use:

```python
# =============================================================================
# STEP 4: Create Required LangExtract Components
# =============================================================================

# Since we're adapting LangExtract, create the minimal required components

# langextract/data.py
langextract_data_content = '''
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
'''

with open('langextract/data.py', 'w') as f:
    f.write(langextract_data_content)

# langextract/inference.py
langextract_inference_content = '''
import abc
from collections.abc import Iterator, Sequence
import dataclasses
from typing import Any

@dataclasses.dataclass(frozen=True)
class ScoredOutput:
    score: float | None = None
    output: str | None = None

class InferenceOutputError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class BaseLanguageModel(abc.ABC):
    def __init__(self, constraint=None):
        self._constraint = constraint

    @abc.abstractmethod
    def infer(self, batch_prompts: Sequence[str], **kwargs) -> Iterator[Sequence[ScoredOutput]]:
        pass
'''

with open('langextract/inference.py', 'w') as f:
    f.write(langextract_inference_content)

# langextract/prompting.py
langextract_prompting_content = '''
import dataclasses
import json
import yaml
from typing import List
from langextract.data import ExampleData, FormatType

@dataclasses.dataclass
class PromptTemplateStructured:
    description: str
    examples: List[ExampleData] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class QAPromptGenerator:
    template: PromptTemplateStructured
    format_type: FormatType = FormatType.YAML
    attribute_suffix: str = "_attributes"
    examples_heading: str = "Examples"
    question_prefix: str = "Q: "
    answer_prefix: str = "A: "
    fence_output: bool = True

    def format_example_as_text(self, example: ExampleData) -> str:
        question = example.text
        data_dict = {"extractions": []}
        
        for extraction in example.extractions:
            data_entry = {
                f"{extraction.extraction_class}": extraction.extraction_text,
                f"{extraction.extraction_class}{self.attribute_suffix}": extraction.attributes or {}
            }
            data_dict["extractions"].append(data_entry)

        if self.format_type == FormatType.YAML:
            formatted_content = yaml.dump(data_dict, default_flow_style=False, sort_keys=False)
            answer = f"```yaml\\n{formatted_content.strip()}\\n```" if self.fence_output else formatted_content.strip()
        else:
            formatted_content = json.dumps(data_dict, indent=2)
            answer = f"```json\\n{formatted_content.strip()}\\n```" if self.fence_output else formatted_content.strip()

        return "\\n".join([
            f"{self.question_prefix}{question}",
            f"{self.answer_prefix}{answer}\\n"
        ])

    def render(self, question: str, additional_context: str = None) -> str:
        prompt_lines = [f"{self.template.description}\\n"]
        
        if additional_context:
            prompt_lines.append(f"{additional_context}\\n")

        if self.template.examples:
            prompt_lines.append(self.examples_heading)
            for ex in self.template.examples:
                prompt_lines.append(self.format_example_as_text(ex))

        prompt_lines.append(f"{self.question_prefix}{question}")
        prompt_lines.append(self.answer_prefix)
        return "\\n".join(prompt_lines)
'''

with open('langextract/prompting.py', 'w') as f:
    f.write(langextract_prompting_content)

# langextract/schema.py
langextract_schema_content = '''
import abc
import dataclasses
import enum
from collections.abc import Sequence
from typing import Any
from langextract.data import ExampleData

class ConstraintType(enum.Enum):
    NONE = "none"

@dataclasses.dataclass
class Constraint:
    constraint_type: ConstraintType = ConstraintType.NONE

EXTRACTIONS_KEY = "extractions"

class BaseSchema(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_examples(cls, examples_data: Sequence[ExampleData], attribute_suffix: str = "_attributes"):
        pass

@dataclasses.dataclass
class GeminiSchema(BaseSchema):
    _schema_dict: dict

    @property
    def schema_dict(self) -> dict:
        return self._schema_dict

    @classmethod
    def from_examples(cls, examples_data: Sequence[ExampleData], attribute_suffix: str = "_attributes"):
        # Simplified schema generation
        schema_dict = {
            "type": "object",
            "properties": {
                EXTRACTIONS_KEY: {"type": "array", "items": {"type": "object"}}
            },
            "required": [EXTRACTIONS_KEY]
        }
        return cls(_schema_dict=schema_dict)
'''

with open('langextract/schema.py', 'w') as f:
    f.write(langextract_schema_content)

print("✅ LangExtract components created")
```
