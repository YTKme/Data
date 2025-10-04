"""
Constellation Module
~~~~~~~~~~~~~~~~~~~~

The constellation module define the model for the constellation data.
"""

#########
# Table #
#########

import uuid

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):

    # Local Type Annotation Map
    type_annotation_map = {
        dict[str, any]: JSONB,
    }


class Constellation(Base):
    """Constellation Table"""

    __tablename__ = "constellation"

    # Data Class
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        name="id",
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    name: Mapped[str] = mapped_column(
        TEXT(collation="unicode"),
        name="name",
        nullable=True,
    )
