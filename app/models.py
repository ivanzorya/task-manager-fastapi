import uuid

from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)


class Task(Base):
    __tablename__ = "task"

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))
    subject = Column(String(500), nullable=False)
    done = Column(Boolean, default=False)
