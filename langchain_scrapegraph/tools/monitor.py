from typing import Any, Dict, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import Client


class MonitorCreateInput(BaseModel):
    name: str = Field(description="Name of the monitor")
    url: str = Field(description="URL to monitor")
    prompt: str = Field(description="Prompt for AI extraction")
    cron: str = Field(
        description="Cron expression for scheduling (e.g., '0 9 * * *' for daily at 9 AM)"
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional JSON Schema for structured output"
    )


class MonitorIdInput(BaseModel):
    monitor_id: str = Field(description="The monitor ID")


class MonitorCreateTool(BaseTool):
    """Tool for creating a monitor using ScrapeGraph AI v2 API."""

    name: str = "MonitorCreate"
    description: str = (
        "Create a new monitor that automatically extracts data from a URL on a schedule."
    )
    args_schema: Type[BaseModel] = MonitorCreateInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        name: str,
        url: str,
        prompt: str,
        cron: str,
        output_schema: Optional[Dict[str, Any]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.monitor.create(
            name=name,
            url=url,
            prompt=prompt,
            cron=cron,
            output_schema=output_schema,
        )
        return response

    async def _arun(
        self,
        name: str,
        url: str,
        prompt: str,
        cron: str,
        output_schema: Optional[Dict[str, Any]] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            name=name,
            url=url,
            prompt=prompt,
            cron=cron,
            output_schema=output_schema,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class MonitorListTool(BaseTool):
    """Tool for listing all monitors."""

    name: str = "MonitorList"
    description: str = "List all monitors in your ScrapeGraph AI account."
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")
        return self.client.monitor.list()

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(run_manager=run_manager.get_sync() if run_manager else None)


class MonitorGetTool(BaseTool):
    """Tool for getting a specific monitor."""

    name: str = "MonitorGet"
    description: str = "Get details of a specific monitor by its ID."
    args_schema: Type[BaseModel] = MonitorIdInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        monitor_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")
        return self.client.monitor.get(monitor_id)

    async def _arun(
        self,
        monitor_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            monitor_id=monitor_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class MonitorPauseTool(BaseTool):
    """Tool for pausing a monitor."""

    name: str = "MonitorPause"
    description: str = "Pause a monitor so it stops running until resumed."
    args_schema: Type[BaseModel] = MonitorIdInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        monitor_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")
        return self.client.monitor.pause(monitor_id)

    async def _arun(
        self,
        monitor_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            monitor_id=monitor_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class MonitorResumeTool(BaseTool):
    """Tool for resuming a paused monitor."""

    name: str = "MonitorResume"
    description: str = "Resume a paused monitor so it starts running again."
    args_schema: Type[BaseModel] = MonitorIdInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        monitor_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")
        return self.client.monitor.resume(monitor_id)

    async def _arun(
        self,
        monitor_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            monitor_id=monitor_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class MonitorDeleteTool(BaseTool):
    """Tool for deleting a monitor."""

    name: str = "MonitorDelete"
    description: str = "Delete a monitor permanently."
    args_schema: Type[BaseModel] = MonitorIdInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        monitor_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")
        return self.client.monitor.delete(monitor_id)

    async def _arun(
        self,
        monitor_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            monitor_id=monitor_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
