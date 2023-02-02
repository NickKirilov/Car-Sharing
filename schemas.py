import pydantic
import typing as t

from passlib.context import CryptContext
from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR


pwd_context = CryptContext(schemes=["bcrypt"])


class UserOutput(SQLModel):
    id: int
    username: str


class User(SQLModel, table=True):
    id: t.Optional[int] = Field(primary_key=True, default=None)
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str = ""

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class TripInput(SQLModel):
    start: int
    end: int
    description: str

    class Config:
        schema_extra = {
            "example": {
                "start": 0,
                "end": 5,
                "description": "manual"
            }
        }


class Trip(TripInput, table=True):
    id: t.Optional[int] = Field(primary_key=True, default=None)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")


class TripOutput(TripInput):
    id: int


class CarInput(SQLModel):
    size: str
    fuel: t.Optional[str] = pydantic.Field(
        default="electric"
    )
    doors: t.Optional[int] = pydantic.Field(
        default=5
    )
    transmission: t.Optional[str] = pydantic.Field(
        default="auto"
    )

    class Config:
        schema_extra = {
            "example": {
                "size": "m",
                "doors": 5,
                "transmission": "manual",
                "fuel": "hybrid"
            }
        }


class Car(CarInput, table=True):
    id: int = Field(primary_key=True, default=None)
    trips: t.Optional[list[Trip]] = Relationship(back_populates="car")


class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []
