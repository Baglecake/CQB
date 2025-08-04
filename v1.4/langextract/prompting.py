
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
            answer = f"```yaml\n{formatted_content.strip()}\n```" if self.fence_output else formatted_content.strip()
        else:
            formatted_content = json.dumps(data_dict, indent=2)
            answer = f"```json\n{formatted_content.strip()}\n```" if self.fence_output else formatted_content.strip()

        return "\n".join([
            f"{self.question_prefix}{question}",
            f"{self.answer_prefix}{answer}\n"
        ])

    def render(self, question: str, additional_context: str = None) -> str:
        prompt_lines = [f"{self.template.description}\n"]
        
        if additional_context:
            prompt_lines.append(f"{additional_context}\n")

        if self.template.examples:
            prompt_lines.append(self.examples_heading)
            for ex in self.template.examples:
                prompt_lines.append(self.format_example_as_text(ex))

        prompt_lines.append(f"{self.question_prefix}{question}")
        prompt_lines.append(self.answer_prefix)
        return "\n".join(prompt_lines)
