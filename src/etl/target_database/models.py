# Modelos ORM do banco alvo.

from datetime import datetime

from sqlalchemy import Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from etl.target_database.constants import (
    DATA_TABLE_NAME,
    DATA_UNIQUE_CONSTRAINT_NAME,
    SIGNAL_NAME_MAX_LENGTH,
    SIGNAL_TABLE_NAME,
)

DATA_UNIQUE_CONSTRAINT: UniqueConstraint = UniqueConstraint(
    "timestamp",
    "signal_id",
    name=DATA_UNIQUE_CONSTRAINT_NAME,
)


class Base(DeclarativeBase):
    pass


class SignalModel(Base):
    __tablename__ = SIGNAL_TABLE_NAME

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String(SIGNAL_NAME_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    data_points: Mapped[list["DataModel"]] = relationship(
        "DataModel",
        back_populates="signal",
    )


class DataModel(Base):
    __tablename__ = DATA_TABLE_NAME
    __table_args__ = (DATA_UNIQUE_CONSTRAINT,)

    timestamp: Mapped[datetime] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    signal_id: Mapped[int] = mapped_column(
        ForeignKey(f"{SIGNAL_TABLE_NAME}.id"),
        primary_key=True,
        nullable=False,
    )
    value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    signal: Mapped[SignalModel] = relationship(
        "SignalModel",
        back_populates="data_points",
    )

