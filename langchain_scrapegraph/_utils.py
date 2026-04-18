"""Internal helpers for translating ScrapeGraph AI v2 API types to LangChain tool outputs."""

from typing import Any, Dict, Optional

from scrapegraph_py import (
    BrandingFormatConfig,
    HtmlFormatConfig,
    ImagesFormatConfig,
    JsonFormatConfig,
    LinksFormatConfig,
    MarkdownFormatConfig,
    ScreenshotFormatConfig,
    SummaryFormatConfig,
)

_FORMAT_CONFIGS = {
    "markdown": MarkdownFormatConfig,
    "html": HtmlFormatConfig,
    "screenshot": ScreenshotFormatConfig,
    "branding": BrandingFormatConfig,
    "links": LinksFormatConfig,
    "images": ImagesFormatConfig,
    "summary": SummaryFormatConfig,
}


def format_config(name: str):
    cls = _FORMAT_CONFIGS.get(name)
    if cls is None:
        raise ValueError(
            f"Unsupported format '{name}'. Expected one of: {sorted(_FORMAT_CONFIGS)}"
        )
    return cls()


def json_format_config(
    prompt: str, schema: Optional[Dict[str, Any]] = None
) -> JsonFormatConfig:
    return JsonFormatConfig(prompt=prompt, schema=schema)


def result_to_dict(result: Any) -> Dict[str, Any]:
    if hasattr(result, "model_dump"):
        return result.model_dump(mode="json", by_alias=False)
    if isinstance(result, dict):
        return result
    return {"data": result}
