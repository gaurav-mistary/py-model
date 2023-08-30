from pydantic.functional_validators import field_validator
from pydantic.types import PositiveInt

from src.basemodels import ImmutableModel
from src.exceptions import InvalidInput


class Address(ImmutableModel):
    street: str
    area: str
    pincode: int

    @field_validator("pincode")
    @classmethod
    def validate_field(cls, value: int) -> int:
        if not 99999 <= value <= 99999999:
            raise InvalidInput(
                msg=f"[X] Pincode has length: {value}. Expected 6-8 chars"
            )

        return value


class AddressValidator:
    @field_validator("addresses")
    @classmethod
    def validate_addresses(cls, addresses: tuple[Address]) -> tuple[Address]:
        if len(addresses) < 1:
            raise InvalidInput(
                msg=f"[X] At least one address expected, provided: {addresses}"
            )

        return addresses


class PersonDetails(ImmutableModel, AddressValidator):
    name: str
    age: PositiveInt
    addresses: tuple[Address, ...]
    blood_group: str


class PersonDetailsWithoutAddress(ImmutableModel):
    name: str
    age: PositiveInt
    addresses: tuple[Address, ...]
    blood_group: str
