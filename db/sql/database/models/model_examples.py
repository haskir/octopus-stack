from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.sql.database.base_model import BaseSQLModel, IntPK, Str128, Str8


class Account(BaseSQLModel):
    """ Example of Account model"""
    __tablename__ = "accounts"  # Table name
    model_name = "Account"  # Model name

    id: Mapped[IntPK]
    currency: Mapped[Str8] = mapped_column(default="USD")
    balance: Mapped[float] = mapped_column(default=100000.0)

    # Relationships
    user: Mapped["User"] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
        lazy="selectin",
        single_parent=True
    )


class Purchase(BaseSQLModel):
    """ Example of Purchase model"""
    __tablename__ = "purchases"  # Table name
    model_name = "Purchase"  # Model name

    id: Mapped[IntPK]
    amount: Mapped[float] = mapped_column(nullable=False)
    name: Mapped[Str128] = mapped_column(nullable=False)


class User(BaseSQLModel):
    """ Example of User model"""
    __tablename__ = "users"  # Table name
    model_name = "User"  # Model name

    id: Mapped[IntPK]
    description: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[Str128]

    # Relationships
    # One-to-one
    account: Mapped[Account] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
        single_parent=True
    )
    #  One-to-many
    purchases: Mapped[list[Purchase]] = relationship(
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        single_parent=True
    )