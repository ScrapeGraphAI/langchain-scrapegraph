from typing import Any, Dict, Optional

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import model_validator
from scrapegraph_py import Client


class GetCreditsTool(BaseTool):
    """Tool for checking remaining credits on your ScrapeGraph AI account.

    Setup:
        Install ``langchain-scrapegraph`` python package:

        .. code-block:: bash

            pip install langchain-scrapegraph

        Get your API key from ScrapeGraph AI (https://scrapegraphai.com)
        and set it as an environment variable:

        .. code-block:: bash

            export SGAI_API_KEY="your-api-key"

    Key init args:
        api_key: Your ScrapeGraph AI API key. If not provided, will look for SGAI_API_KEY env var.
        client: Optional pre-configured ScrapeGraph client instance.

    Instantiate:
        .. code-block:: python

            from langchain_scrapegraph.tools import GetCreditsTool

            # Will automatically get SGAI_API_KEY from environment
            tool = GetCreditsTool()

            # Or provide API key directly
            tool = GetCreditsTool(api_key="your-api-key")

    Use the tool:
        .. code-block:: python

            result = tool.invoke({})

            print(result)
            # {
            #     "remaining_credits": 100,
            #     "total_credits_used": 50
            # }

    Async usage:
        .. code-block:: python

            result = await tool.ainvoke({})
    """

    name: str = "GetCredits"
    description: str = (
        "Get the current credits available in your ScrapeGraph AI account"
    )
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
