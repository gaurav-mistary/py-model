from pydantic.functional_validators import field_validator
from pydantic.types import PositiveInt
from pydantic import EmailStr

from src.basemodels import ImmutableModel
from src.exceptions import InvalidInput


# ANSWER
class EmailValidator:
    @field_validator("email_addresses")
    @classmethod
    def validate_emails(cls, value: tuple[EmailStr, ...]) -> tuple[EmailStr, ...]:
        if len(value) < 1:
            raise InvalidInput(f"[X] At least one email required, provided {value}")

        return value


class PersonDetailsWithEmail(ImmutableModel, EmailValidator):
    name: str
    age: PositiveInt
    email_addresses: tuple[EmailStr, ...]
    blood_group: str


# If not in use, deprecate
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


# If this class is no longer in use, deprecase
class AddressValidator:
    @field_validator("addresses")
    @classmethod
    def validate_addresses(cls, addresses: tuple[Address]) -> tuple[Address]:
        if len(addresses) < 1:
            raise InvalidInput(
                msg=f"[X] At least one address expected, provided: {addresses}"
            )

        return addresses


# If this class is no longer in use, deprecate
class PersonDetails(ImmutableModel, AddressValidator):
    name: str
    age: PositiveInt
    addresses: tuple[Address, ...]
    blood_group: str


# If this class is no longer in use, deprecate
class PersonDetailsWithoutAddress(ImmutableModel):
    name: str
    age: PositiveInt
    addresses: tuple[Address, ...]
    blood_group: str
