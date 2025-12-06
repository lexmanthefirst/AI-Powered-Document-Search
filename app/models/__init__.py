"""
Top-level package for models.

Import all models here to ensure SQLAlchemy sees every declarative model
before it configures mappers. This prevents relationship lookups from
failing due to import-order issues.
"""

from .base import Base, BaseModel
from .document import Document

__all__ = [
    "Base",
    "BaseModel",
    "Document",
]
