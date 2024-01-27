from typing import Optional
import aiohttp
from pydantic import BaseModel

base_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0"
}


def get_fields(model: BaseModel) -> list[str]:
    """Return fields of a model, preferring an alias if present."""
    attribs = []
    for name, field in model.model_fields.items():
        if field.alias:
            attribs.append(field.alias)
        else:
            attribs.append(name)
    return attribs


def construct_fields(fields: dict) -> str:
    """Construct a fields query string from a dictionary.

    Example:
    >>> d: StoryModelFieldsType = {
        "tags": True,
        "id": True,
        "parts": {"id": True},
        "tagRankings": True
    }
    >>> construct_fields(d)
    'tags,id,parts(id),tagRankings'"""
    fields_str = ""

    for key, value in fields.items():
        if value is False:
            continue

        if value is True:
            fields_str += f"{key},"

        if type(value) is dict:
            fields_str += f"{key}({construct_fields(value)}),"

    fields_str = fields_str.removesuffix(",")

    return fields_str


def build_url(
    path: str,
    fields: Optional[dict] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> str:
    """Build a URL."""
    base_url = f"https://www.wattpad.com/api/v3/{path}?"
    if fields:
        fields_str = construct_fields(fields)
        base_url += f"fields={fields_str}&"

    if limit:
        base_url += f"limit={limit}&"

    if offset:
        base_url += f"offset={offset}&"

    url = base_url.removesuffix("&")

    return url


async def fetch_url(url: str, headers: dict = {}) -> dict | list:
    use_headers = base_headers.copy()
    use_headers.update(headers)

    async with aiohttp.ClientSession(headers=use_headers) as session:
        async with session.get(url) as response:
            return await response.json()


def singleton(cls):
    # Thanks https://medium.com/@pavankumarmasters/exploring-the-singleton-design-pattern-in-python-a34efa5e8cfa
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
