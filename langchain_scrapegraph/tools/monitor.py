from typing import Any, Dict, List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import MonitorCreateRequest, ScrapeGraphAI

from langchain_scrapegraph._utils import (
    format_config,
    json_format_config,
    result_to_dict,
)


class MonitorCreateInput(BaseModel):
    url: str = Field(description="URL to monitor")
    interval: str = Field(
        description="Monitor interval (e.g. '1h', '30m', or a cron expression)"
    )
    name: Optional[str] = Field(default=None, description="Name of the monitor")
    prompt: Optional[str] = Field(
        default=None,
        description="Optional prompt for AI-driven JSON extraction on each tick",
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional JSON Schema for structured output (requires prompt)",
    )
    formats: Optional[List[str]] = Field(
        default=None,
        description=(
            "List of non-json formats to capture (markdown, html, links, images, "
            "summary, branding, screenshot). Defaults to ['markdown']."
        ),
    )
    webhook_url: Optional[str] = Field(
        default=None, description="Optional webhook URL to notify on changes"
    )


class MonitorIdInput(BaseModel):
    monitor_id: str = Field(description="The monitor ID")


def _make_client(values: Dict) -> Dict:
    values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
    values["client"] = ScrapeGraphAI(api_key=values["api_key"])
    return values


class MonitorCreateTool(BaseTool):
    """Tool for creating a monitor using ScrapeGraph AI v2 API."""

    name: str = "MonitorCreate"
    description: str = (
        "Create a new monitor that automatically scrapes a URL on a schedule "
        "and reports changes."
    )
    args_schema: Type[BaseModel] = MonitorCreateInput
    return_direct: bool = True
    client: Optional[ScrapeGraphAI] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        return _make_client(values)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        url: str,
        interval: str,
        name: Optional[str] = None,
        prompt: Optional[str] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        formats: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")

        format_entries = [format_config(f) for f in (formats or ["markdown"])]
        if prompt:
            format_entries.append(json_format_config(prompt, output_schema))

        request = MonitorCreateRequest(
            url=url,
            name=name,
            interval=interval,
            formats=format_entries,
            webhook_url=webhook_url,
        )
        return result_to_dict(self.client.monitor.create(request))

    async def _arun(
        self,
        url: str,
        interval: str,
        name: Optional[str] = None,
        prompt: Optional[str] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        formats: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        return self._run(
            url=url,
            interval=interval,
            name=name,
            prompt=prompt,
            output_schema=output_schema,
            formats=formats,
            webhook_url=webhook_url,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class MonitorListTool(BaseTool):
    """Tool for listing all monitors."""

    name: str = "MonitorList"
    description: str = "List all monitors in your ScrapeGraph AI account."
    return_direct: bool = True
    client: Optional[ScrapeGraphAI] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        return _make_client(values)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")
        return result_to_dict(self.client.monitor.list())

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        return self._run(run_manager=run_manager.get_sync() if run_manager else None)


class MonitorGetTool(BaseTool):
    """Tool for getting a specific monitor."""

    name: str = "MonitorGet"
    description: str = "Get details of a specific monitor by its ID."
    args_schema: Type[BaseModel] = MonitorIdInput
    return_direct: bool = True
    client: Optional[ScrapeGraphAI] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        return _make_client(values)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        monitor_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")
        return result_to_dict(self.client.monitor.get(monitor_id))

    async def _arun(
        self,
        monitor_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
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
    client: Optional[ScrapeGraphAI] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        return _make_client(values)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        monitor_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")
        return result_to_dict(self.client.monitor.pause(monitor_id))

    async def _arun(
        self,
        monitor_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
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
    client: Optional[ScrapeGraphAI] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        return _make_client(values)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        monitor_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")
        return result_to_dict(self.client.monitor.resume(monitor_id))

    async def _arun(
        self,
        monitor_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
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
    client: Optional[ScrapeGraphAI] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        return _make_client(values)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        monitor_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")
        return result_to_dict(self.client.monitor.delete(monitor_id))

    async def _arun(
        self,
        monitor_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        return self._run(
            monitor_id=monitor_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
