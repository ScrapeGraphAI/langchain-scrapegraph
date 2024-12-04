from typing import Any, Dict, Optional

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import model_validator
from scrapegraph_py import SyncClient


class GetCreditsTool(BaseTool):
    name: str = "GetCredits"
    description: str = (
        "Get the current credits available in your ScrapeGraph AI account"
    )
    return_direct: bool = True
    client: Optional[SyncClient] = None
    api_key: str
    testing: bool = False

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = SyncClient(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(self, run_manager: Optional[CallbackManagerForToolRun] = None) -> dict:
        """Get the available credits."""
        if not self.client:
            raise ValueError("Client not initialized")
        return self.client.get_credits()

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> int:
        """Get the available credits asynchronously."""
        return self._run(run_manager=run_manager.get_sync() if run_manager else None)
