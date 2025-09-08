from typing import Any, Dict, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import Client


class ServiceType:
    """Service types for scheduled jobs."""

    SMARTSCRAPER = "smartscraper"
    SEARCHSCRAPER = "searchscraper"
    SMARTCRAWLER = "smartcrawler"
    MARKDOWNIFY = "markdownify"


class CreateScheduledJobInput(BaseModel):
    job_name: str = Field(description="Name of the scheduled job")
    service_type: str = Field(
        description="Type of service to run (smartscraper, searchscraper, smartcrawler, markdownify)"
    )
    cron_expression: str = Field(
        description="Cron expression for scheduling (e.g., '0 9 * * *' for daily at 9 AM)"
    )
    job_config: Dict[str, Any] = Field(
        description="Configuration dictionary for the job (varies by service type)"
    )
    is_active: bool = Field(
        default=True, description="Whether the job should be active"
    )


class GetScheduledJobsInput(BaseModel):
    page: int = Field(default=1, description="Page number for pagination")
    page_size: int = Field(default=10, description="Number of jobs per page")
    service_type: Optional[str] = Field(
        default=None,
        description="Filter by service type (smartscraper, searchscraper, etc.)",
    )
    is_active: Optional[bool] = Field(
        default=None, description="Filter by active status"
    )


class GetScheduledJobInput(BaseModel):
    job_id: str = Field(description="ID of the scheduled job to retrieve")


class UpdateScheduledJobInput(BaseModel):
    job_id: str = Field(description="ID of the scheduled job to update")
    job_name: Optional[str] = Field(default=None, description="New job name")
    cron_expression: Optional[str] = Field(
        default=None, description="New cron expression"
    )
    job_config: Optional[Dict[str, Any]] = Field(
        default=None, description="New job configuration"
    )
    is_active: Optional[bool] = Field(default=None, description="New active status")


class JobControlInput(BaseModel):
    job_id: str = Field(description="ID of the scheduled job")


class GetJobExecutionsInput(BaseModel):
    job_id: str = Field(description="ID of the scheduled job")
    page: int = Field(default=1, description="Page number for pagination")
    page_size: int = Field(default=10, description="Number of executions per page")


class CreateScheduledJobTool(BaseTool):
    """Tool for creating scheduled jobs with ScrapeGraph AI.

    This tool allows you to create recurring jobs that will automatically
    run at specified intervals using cron expressions.
    """

    name: str = "CreateScheduledJob"
    description: str = (
        "Create a new scheduled job that will run automatically at specified intervals. "
        "Supports SmartScraper, SearchScraper, SmartCrawler, and Markdownify services."
    )
    args_schema: Type[BaseModel] = CreateScheduledJobInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def _run(
        self,
        job_name: str,
        service_type: str,
        cron_expression: str,
        job_config: Dict[str, Any],
        is_active: bool = True,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Create a scheduled job."""
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.create_scheduled_job(
            job_name=job_name,
            service_type=service_type,
            cron_expression=cron_expression,
            job_config=job_config,
            is_active=is_active,
        )
        return response

    async def _arun(
        self,
        job_name: str,
        service_type: str,
        cron_expression: str,
        job_config: Dict[str, Any],
        is_active: bool = True,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Create a scheduled job asynchronously."""
        return self._run(
            job_name=job_name,
            service_type=service_type,
            cron_expression=cron_expression,
            job_config=job_config,
            is_active=is_active,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class GetScheduledJobsTool(BaseTool):
    """Tool for retrieving scheduled jobs from ScrapeGraph AI."""

    name: str = "GetScheduledJobs"
    description: str = (
        "Retrieve a list of scheduled jobs with optional filtering by service type and active status."
    )
    args_schema: Type[BaseModel] = GetScheduledJobsInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def _run(
        self,
        page: int = 1,
        page_size: int = 10,
        service_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Get scheduled jobs."""
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.get_scheduled_jobs(
            page=page,
            page_size=page_size,
            service_type=service_type,
            is_active=is_active,
        )
        return response

    async def _arun(
        self,
        page: int = 1,
        page_size: int = 10,
        service_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Get scheduled jobs asynchronously."""
        return self._run(
            page=page,
            page_size=page_size,
            service_type=service_type,
            is_active=is_active,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class GetScheduledJobTool(BaseTool):
    """Tool for retrieving a specific scheduled job by ID."""

    name: str = "GetScheduledJob"
    description: str = "Retrieve details of a specific scheduled job by its ID."
    args_schema: Type[BaseModel] = GetScheduledJobInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def _run(
        self,
        job_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Get a specific scheduled job."""
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.get_scheduled_job(job_id)
        return response

    async def _arun(
        self,
        job_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Get a specific scheduled job asynchronously."""
        return self._run(
            job_id=job_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class UpdateScheduledJobTool(BaseTool):
    """Tool for updating a scheduled job."""

    name: str = "UpdateScheduledJob"
    description: str = "Update properties of an existing scheduled job."
    args_schema: Type[BaseModel] = UpdateScheduledJobInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def _run(
        self,
        job_id: str,
        job_name: Optional[str] = None,
        cron_expression: Optional[str] = None,
        job_config: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Update a scheduled job."""
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.update_scheduled_job(
            job_id=job_id,
            job_name=job_name,
            cron_expression=cron_expression,
            job_config=job_config,
            is_active=is_active,
        )
        return response

    async def _arun(
        self,
        job_id: str,
        job_name: Optional[str] = None,
        cron_expression: Optional[str] = None,
        job_config: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Update a scheduled job asynchronously."""
        return self._run(
            job_id=job_id,
            job_name=job_name,
            cron_expression=cron_expression,
            job_config=job_config,
            is_active=is_active,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class PauseScheduledJobTool(BaseTool):
    """Tool for pausing a scheduled job."""

    name: str = "PauseScheduledJob"
    description: str = "Pause a scheduled job so it won't run until resumed."
    args_schema: Type[BaseModel] = JobControlInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def _run(
        self,
        job_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Pause a scheduled job."""
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.pause_scheduled_job(job_id)
        return response

    async def _arun(
        self,
        job_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Pause a scheduled job asynchronously."""
        return self._run(
            job_id=job_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class ResumeScheduledJobTool(BaseTool):
    """Tool for resuming a paused scheduled job."""

    name: str = "ResumeScheduledJob"
    description: str = "Resume a paused scheduled job so it will start running again."
    args_schema: Type[BaseModel] = JobControlInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def _run(
        self,
        job_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Resume a scheduled job."""
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.resume_scheduled_job(job_id)
        return response

    async def _arun(
        self,
        job_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Resume a scheduled job asynchronously."""
        return self._run(
            job_id=job_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class TriggerScheduledJobTool(BaseTool):
    """Tool for manually triggering a scheduled job."""

    name: str = "TriggerScheduledJob"
    description: str = "Manually trigger a scheduled job to run immediately."
    args_schema: Type[BaseModel] = JobControlInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def _run(
        self,
        job_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Trigger a scheduled job."""
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.trigger_scheduled_job(job_id)
        return response

    async def _arun(
        self,
        job_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Trigger a scheduled job asynchronously."""
        return self._run(
            job_id=job_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class GetJobExecutionsTool(BaseTool):
    """Tool for getting execution history of a scheduled job."""

    name: str = "GetJobExecutions"
    description: str = "Retrieve execution history for a scheduled job."
    args_schema: Type[BaseModel] = GetJobExecutionsInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def _run(
        self,
        job_id: str,
        page: int = 1,
        page_size: int = 10,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Get job executions."""
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.get_job_executions(
            job_id=job_id,
            page=page,
            page_size=page_size,
        )
        return response

    async def _arun(
        self,
        job_id: str,
        page: int = 1,
        page_size: int = 10,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Get job executions asynchronously."""
        return self._run(
            job_id=job_id,
            page=page,
            page_size=page_size,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class DeleteScheduledJobTool(BaseTool):
    """Tool for deleting a scheduled job."""

    name: str = "DeleteScheduledJob"
    description: str = "Delete a scheduled job permanently."
    args_schema: Type[BaseModel] = JobControlInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def _run(
        self,
        job_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Delete a scheduled job."""
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.delete_scheduled_job(job_id)
        return response

    async def _arun(
        self,
        job_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Delete a scheduled job asynchronously."""
        return self._run(
            job_id=job_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
