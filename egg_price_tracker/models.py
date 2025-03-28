from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EggPrice(BaseModel):
    """Data model for egg price information."""

    date: datetime
    price: float
    source: str
    notes: Optional[str] = None
