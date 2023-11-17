from __future__ import annotations

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class WebhallenProductIn(BaseModel):
    """The Webhallen product used for FastAPI endpoints."""

    product_id: int
    product_json: str


class WebhallenProduct(SQLModel, table=True):
    """The Webhallen product.

    Args:
        SQLModel: The SQLModel class.
        table: Whether or not this class should be a table.
    """

    product_id: int | None = Field(default=None, primary_key=True)
    product_json: str | None = Field(default=None)
