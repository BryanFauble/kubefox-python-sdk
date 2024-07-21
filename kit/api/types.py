from typing import Dict, List
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Object:
    def get_namespace(self) -> str:
        pass

    def get_name(self) -> str:
        pass

    def get_resource_version(self) -> str:
        pass

    def get_generation(self) -> int:
        pass


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class EnvVarDefinition:
    type: str
    required: bool


EnvVarSchema = Dict[str, EnvVarDefinition]


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class EnvSchema:
    vars: EnvVarSchema
    secrets: EnvVarSchema


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class ComponentDefinition:
    type: str
    routes: List['RouteSpec']
    default_handler: bool
    env_var_schema: EnvVarSchema
    dependencies: Dict[str, 'Dependency']
    hash: str
    image: str


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class RouteSpec:
    id: int
    rule: str
    priority: int
    env_var_schema: EnvVarSchema


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Dependency:
    type: str


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Details:
    title: str
    description: str


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class ProblemSource:
    kind: str
    name: str
    observed_generation: int
    path: str
    value: str


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class Problem:
    type: str
    message: str
    causes: List[ProblemSource]
