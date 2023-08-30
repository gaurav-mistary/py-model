from typing import Type, Optional

from src.custom_types import T


class ImproperlyConfigured(Exception):
    def __init__(self, msg: Optional[str] = None):
        if msg is None:
            self.msg = f"Application component seems to be improperly configured"
        else:
            self.msg = msg

        super().__init__(self.msg)


class MandatoryFieldHasNoneValue(ImproperlyConfigured):
    def __init__(self, cls: Type[T], field: str):
        self.msg = f"Field: '{field}' of MandatoryImmutable : '{cls.__name__}' is None"
        super().__init__(msg=self.msg)


class MutationNotAllowed(ImproperlyConfigured):
    def __init__(self, cls: Type[T], field: str):
        self.msg = f"[X] Mutation not allowed for class: {cls} , field: {field}"
        super().__init__(msg=self.msg)


class OnlyEitherMustBePresent(ImproperlyConfigured):
    def __init__(self, func_name: str, fields: tuple[str, ...]):
        self.msg = f"[X] Only either of {fields} must be present in func: {func_name}"
        super().__init__(msg=self.msg)


class InvalidInput(ImproperlyConfigured):
    def __init__(self, msg: str, field: str | None = None, value: str | None = None):
        if not msg:
            assert all([field, value]), ImproperlyConfigured(
                f"[x] If not providing message, "
                f"both 'field' and 'value' are mandatory"
            )
            msg = f"[X] Invalid input received for field: {field} := {value}"

        self.msg = msg

        super().__init__(self.msg)
