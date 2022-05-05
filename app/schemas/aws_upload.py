from typing import List

from pydantic import BaseModel, HttpUrl


class FileUpload(BaseModel):
    filename: str
    file_type: str


class PreSignField(BaseModel):
    key: str
    value: str


class PreSignData(BaseModel):

    fields: List[PreSignField]
    url: HttpUrl
    file_id: str
