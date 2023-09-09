from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from db.models.base import Base
from uuid import UUID as UUIDPython
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

class Session(Base):
    __tablename__ = "session"
    id: Mapped[UUIDPython] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="sessions")
