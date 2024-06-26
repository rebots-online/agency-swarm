from abc import ABC, abstractmethod
from typing import Optional, Any, ClassVar

from instructor import OpenAISchema

from pydantic import Field
from agency_swarm.util import shared_state
from agency_swarm.util.shared_state import SharedState


class BaseTool(OpenAISchema, ABC):
    shared_state: ClassVar[SharedState] = shared_state
    caller_agent: Any = None
    event_handler: Any = None
    one_call_at_a_time: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # # Exclude 'run' method from Pydantic model fields
        # self.model_fields.pop("run", None)

    @classmethod
    @property
    def openai_schema(cls):
        schema = super(BaseTool, cls).openai_schema

        properties = schema.get("parameters", {}).get("properties", {})

        properties.pop("caller_agent", None)
        properties.pop("shared_state", None)
        properties.pop("event_handler", None)
        properties.pop("one_call_at_a_time", None)

        required = schema.get("parameters", {}).get("required", [])
        if "caller_agent" in required:
            required.remove("caller_agent")
        if "shared_state" in required:
            required.remove("shared_state")
        if "event_handler" in required:
            required.remove("event_handler")
        if "one_call_at_a_time" in required:
            required.remove("one_call_at_a_time")

        return schema

    def model_dump(self, **kwargs):
        return super().model_dump(exclude={"caller_agent", "shared_state", "event_handler", "one_call_at_a_time"},
                                  **kwargs)

    @abstractmethod
    def run(self, **kwargs):
        pass
