from typing import Any, List, Optional

from pydantic import BaseModel


class Header(BaseModel):
    name: str
    value: str

class RequestModel(BaseModel):
    method: str
    url: str
    headers: List[Header]
    postData: Optional[Any] = None
    queryString: Optional[List[Header]] = None

class ResponseContent(BaseModel):
    text: str
    mimeType: Optional[str] = None

class ResponseModel(BaseModel):
    status: int
    headers: List[Header]
    content: ResponseContent
