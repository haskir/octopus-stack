import json
from datetime import datetime, timezone, date
from enum import Enum, StrEnum, IntEnum
from typing import Annotated

from pydantic import BaseModel
from sqlalchemy import String, Integer, UUID, text
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


def get_utc_now():
    return datetime.now(tz=timezone.utc).replace(tzinfo=None)


# Integer primary key (1, 2, 3 etc.)
IntPK = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
# UUID primary key
StrPK = Annotated[str, mapped_column(UUID(as_uuid=True), primary_key=True, default=text("gen_random_uuid()"))]

CreatedAt = Annotated[datetime, mapped_column(nullable=False, default=get_utc_now())]
UpdatedAt = Annotated[datetime, mapped_column(nullable=False, default=get_utc_now(), onupdate=get_utc_now())]

Str8 = Annotated[str, 8]  # Annotated for length-string
Str16 = Annotated[str, 16]  # Annotated for length-string
Str32 = Annotated[str, 32]  # Annotated for length-string
Str64 = Annotated[str, 64]  # Annotated for length-string
Str128 = Annotated[str, 128]  # Annotated for length-string
Str256 = Annotated[str, 256]  # Annotated for length-string
Second = int


class Base(DeclarativeBase):
    type_annotation_map = {
        Str8: String(8),
        Str16: String(16),
        Str32: String(32),
        Str64: String(64),
        Str128: String(128),
        Str256: String(256),
    }

    repr_cols_num = 10
    repr_cols: tuple = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class BaseSQLModel(Base):
    __abstract__ = True
    model_name: str

    # JSON fields that should be serialized
    json_slots: tuple[str] = ()

    # Non-table properties
    non_table_properties: set = set()

    # Automatically set on create or update
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    def from_dict[T](self, data: dict | BaseModel, raise_error: bool = True) -> T:
        """ Load model from dict | Pydantic model.
        Use to create new (new = Model().from_dict(data));
        Use to update existing (existing.update(data))
        """
        if isinstance(data, BaseModel):
            data = dict(data)
        invalid_keys = {
            key for key in data.keys() if
            key not in self.__table__.columns.keys() and key not in self.non_table_properties
        }
        if invalid_keys and raise_error:
            raise ValueError(f'"{self.__class__.__name__}" Invalid keys: {", ".join(invalid_keys)}')
        for field in data.keys():
            if field in invalid_keys:
                continue
            if field in self.json_slots:
                setattr(self, field, json.dumps(data[field]))
            else:
                setattr(self, field, data[field])
        return self

    def to_dict(self) -> dict:
        """ Dump model to dict """
        result = dict()
        for column in self.__table__.columns.keys():
            value = getattr(self, column)
            if column in self.json_slots:
                result[column] = json.loads(getattr(self, column))
            elif isinstance(value, (date, datetime)):
                result[column] = value.isoformat()
            elif issubclass(value.__class__, (StrEnum, IntEnum, Enum)):
                result[column] = value.name
            elif isinstance(value, (int, float, str, bool)) or value is None:
                result[column] = value
            else:
                result[column] = str(value)
        return result


__all__ = [
    "get_utc_now",
    "IntPK",
    "StrPK",
    "CreatedAt",
    "UpdatedAt",
    "Str8",
    "Str16",
    "Str32",
    "Str64",
    "Str128",
    "Str256",
    "Second",
    "Base",
    "BaseSQLModel"
]
