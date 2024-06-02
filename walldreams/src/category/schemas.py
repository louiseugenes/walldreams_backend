from pydantic import BaseModel
from typing import Optional
from pydantic.fields import Field
from typing import Generic, TypeVar, List
from pydantic.generics import GenericModel


T = TypeVar('T')

class CategorySchema(BaseModel):
    category_id: Optional[int]=None
    name: Optional[str]=None
    count: Optional[int]=None

    class Config:
        from_attributes = True

class RequestCategory(BaseModel):
    parameter: CategorySchema = Field(...)

class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[List[T]] = None