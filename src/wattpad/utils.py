"""Copyright (C) 2024 TheOnlyWayUp

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

---

Utility functions for the wattpad package."""

from typing import Any, Optional
import aiohttp
import weakref
from threading import Lock  # https://stackoverflow.com/a/77918570
from os import environ
from aiohttp_client_cache.session import CachedSession
from pydantic import BaseModel

base_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0"
}


def get_fields(model: BaseModel) -> list[str]:
    """Retrieve the fields of a Pydantic Model. Prefer field aliases if present.

    Args:
        model (BaseModel): The model to retrieve fields from.

    Returns:
        list[str]: A list of fields.
    """
    attribs = []
    for name, field in model.model_fields.items():
        if field.alias:
            attribs.append(field.alias)
        else:
            attribs.append(name)
    return attribs


def construct_fields(fields: dict) -> str:
    """Constructs a field query string from a dictionary representing the same.

    Example:
    ```py
    >>> d: StoryModelFieldsType = {
        "tags": True,
        "id": True,
        "parts": {"id": True},
        "tagRankings": True
    }
    >>> construct_fields(d)
    'tags,id,parts(id),tagRankings'
    ```

    Args:
        fields (dict): Field Data.

    Returns:
        str: Field Query String.
    """
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
    """Build an API Request URL.

    Args:
        path (str): The API Endpoint to request.
        fields (Optional[dict], optional): Fields Data, processed by `construct_fields`. Defaults to None.
        limit (Optional[int], optional): Number of records to limit the response to. Defaults to None.
        offset (Optional[int], optional): Number of records to skip before beginning the response. Defaults to None.

    Returns:
        str: The built URL.
    """
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
    """Perform a GET Request to the provided URL, merging the provided headers with `base_headers`.
    **Note**: API Responses are cached using the URL as a key. Set the `WPPY_SKIP_CACHE` Environment Variable to True to bypass the cache.

    Args:
        url (str): The URL to request.
        headers (dict, optional): Additional headers to merge atop of `base_headers`. Defaults to {}.

    Returns:
        dict | list: The JSON-Decoded Response.
    """
    use_headers = base_headers.copy()
    use_headers.update(headers)

    if environ.get("WPPY_SKIP_CACHE", False):
        session = aiohttp.ClientSession
    else:
        session = CachedSession

    async with session(headers=use_headers) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()


def create_singleton() -> Any:
    """Make a class a singleton using the first argument as the key.

    Thanks https://medium.com/@pavankumarmasters/exploring-the-singleton-design-pattern-in-python-a34efa5e8cfa#:~:text=Code%20Magic%3A%20Conjuring%20Singletons%20with%20Metaclasses.

    Returns:
        SingletonMeta: The Singleton metaclass.
    """

    class SingletonMeta(type):
        _instances = (
            weakref.WeakValueDictionary()
        )  # Thanks to https://stackoverflow.com/a/77918570
        # ! This is to prevent memory leaking. Python objects are only GC'd when their reference count hits zero. Due the reference from the singleton dict, the RC will be 1 at minimum, when no user-facing code is interfacing with it. To prevent this, the WeakValueDictionary is used. It's values don't count their presence in this dict as a reference, and hence, there's no interference with garbage collection.  |  Thanks to ChatGPT for giving me the idea of looking into the weakref package.
        LOCK = Lock()

        def __call__(cls, *args, **kwargs):
            with cls.LOCK:  # To prevent cases where two threads see a missing entry and both threads try to populate it. | https://stackoverflow.com/questions/77918487/python-magic-method-for-when-the-objects-reference-count-changes#comment137367057_77918570
                if args:
                    key: str = args[0].lower()
                else:
                    if "username" in kwargs:
                        key: str = kwargs["username"]
                    else:
                        key: str = kwargs["id"]

                if key not in cls._instances:
                    new = super(SingletonMeta, cls).__call__(*args, **kwargs)
                    cls._instances[key] = new
                return cls._instances[key]

    return SingletonMeta
