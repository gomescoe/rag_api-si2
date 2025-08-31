# app/models.py
import hashlib
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from app.config import DEFAULT_TOP_K, MAX_TOP_K

class DocumentResponse(BaseModel):
    page_content: str
    metadata: dict

class DocumentModel(BaseModel):
    page_content: str
    metadata: Optional[dict] = {}

    def generate_digest(self):
        hash_obj = hashlib.md5(self.page_content.encode())
        return hash_obj.hexdigest()

class StoreDocument(BaseModel):
    filepath: str
    filename: str
    file_content_type: str
    file_id: str

class QueryRequestBody(BaseModel):
    query: str
    file_id: str
    k: int = Field(default=DEFAULT_TOP_K, ge=1, le=MAX_TOP_K)
    entity_id: Optional[str] = None

    # NOVOS:
    filter: Optional[Dict[str, Any]] = None             # ex.: {"page":{"$gte":3,"$lte":8}, "keywords":{"$contains":["física"]}}
    max_distance: Optional[float] = Field(default=None, ge=0.0)  # filtrar por score (distância) se disponível
    search_type: Literal["similarity", "mmr"] = "similarity"
    fetch_k: Optional[int] = Field(default=None, ge=1)  # pool inicial p/ MMR
    lambda_mult: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)

class CleanupMethod(str, Enum):
    incremental = "incremental"
    full = "full"

class QueryMultipleBody(BaseModel):
    query: str
    file_ids: List[str]
    k: int = Field(default=DEFAULT_TOP_K, ge=1, le=MAX_TOP_K)

    # idem:
    filter: Optional[Dict[str, Any]] = None
    max_distance: Optional[float] = Field(default=None, ge=0.0)
    search_type: Literal["similarity", "mmr"] = "similarity"
    fetch_k: Optional[int] = Field(default=None, ge=1)
    lambda_mult: Optional[float] = Field(default=0.5, ge=0.0, le=1.0)
