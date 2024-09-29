import re
import string
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class EnvVarDefinition:
    type: str
    required: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class EnvSchema:
    vars: Dict[str, EnvVarDefinition] = field(default_factory=dict)
    secrets: Dict[str, EnvVarDefinition] = field(default_factory=dict)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class EnvTemplate:
    name: str
    template: str
    env_schema: EnvSchema = field(default_factory=EnvSchema)
    parse_err: Optional[Exception] = None

    def __post_init__(self):
        resolved = " ".join(self.template.split())
        try:
            self.tree = string.Template(resolved)
        except Exception as e:
            self.parse_err = e
            return

        # Simulate parsing the template and extracting variables
        for match in re.finditer(r"\{\{(\w+)\.(\w+)\}\}", self.template):
            section, name = match.groups()
            if section in ["Vars", "Env"]:
                self.env_schema.vars[name] = EnvVarDefinition(type="", required=True)
            elif section == "Secrets":
                self.env_schema.secrets[name] = EnvVarDefinition(type="", required=True)

    def parse_error(self) -> Optional[Exception]:
        return self.parse_err

    def resolve(self, data: "Data", include_secrets: bool) -> str:
        if data is None:
            data = Data()

        env_var_data = {
            "Vars": {k: v for k, v in data.vars.items()},
            "Env": {k: v for k, v in data.vars.items()},
            "Secrets": (
                {k: v for k, v in data.secrets.items()} if include_secrets else {}
            ),
        }

        try:
            result = self.tree.safe_substitute(env_var_data)
            return result.replace("<no value>", "")
        except KeyError as e:
            raise ValueError(f"Missing key in template: {e}")


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Data:
    vars: Dict[str, "Val"] = field(default_factory=dict)
    secrets: Dict[str, "Val"] = field(default_factory=dict)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ProblemSource:
    kind: str
    name: str
    observed_generation: int
    path: str
    value: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Problem:
    type: str
    message: str
    causes: List[ProblemSource]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Val:
    type: str
    value: str

    def env_var_type(self) -> str:
        return self.type

    def array_string(self) -> List[str]:
        return self.value.split(",")


@dataclass
class EnvVar:
    val: Val

    def __str__(self) -> str:
        if self.val.type in ["ArrayNumber", "ArrayString"]:
            return (
                "{"
                + "|".join(f"^{re.escape(s)}$" for s in self.val.array_string())
                + "}"
            )
        return self.val.value


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class EnvVarSchema:
    vars: Dict[str, EnvVarDefinition] = field(default_factory=dict)
    secrets: Dict[str, EnvVarDefinition] = field(default_factory=dict)

    def validate(
        self, typ: str, vars: Dict[str, Val], src: ProblemSource, append_name: bool
    ) -> List[Problem]:
        problems = []
        for var_name, var_def in self.vars.items():
            val = vars.get(var_name)
            if not val and var_def.required:
                src_copy = src
                if append_name:
                    src_copy.path = f"{src.path}.{var_name}"
                problems.append(
                    Problem(
                        type="VarNotFound",
                        message=f'{typ} "{var_name}" not found but is required.',
                        causes=[src_copy],
                    )
                )
            elif val and var_def.type and val.env_var_type() != var_def.type:
                src_copy = src
                src_copy.path = f"{src.path}.{var_name}.type"
                src_copy.value = var_def.type
                problems.append(
                    Problem(
                        type="VarWrongType",
                        message=f'{typ} "{var_name}" has wrong type; wanted "{
                        var_def.type}" got "{val.env_var_type()}".',
                        causes=[src_copy],
                    )
                )
        return problems
