from datetime import datetime

from sqlalchemy import func, Column, String, Integer, DateTime
from sqlalchemy.orm import Mapped, registry, mapped_column

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True
    )
    username: Mapped[str] = mapped_column(init=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
