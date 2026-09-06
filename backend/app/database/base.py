import uuid
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import DateTime, MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Standardized Naming Convention for Constraints and Indexes
POSTGRES_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all SQLAlchemy 2.0 models in the application.
    Enforces unified metadata naming conventions and common helpers.
    """
    metadata = MetaData(naming_convention=POSTGRES_NAMING_CONVENTION)

    def to_dict(self) -> dict[str, Any]:
        """Convert model instance attributes to a dictionary."""
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
        }
