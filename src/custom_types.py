import typing

from pydantic import BaseModel

T = typing.TypeVar("T")

TModel = typing.TypeVar("TModel", bound=BaseModel)


@typing.runtime_checkable
class ProxyType(typing.Protocol[T]):
    of: T


def either(*args) -> bool:

    if any(args) and not all(args):
        return True

    from src.exceptions import OnlyEitherMustBePresent
    raise OnlyEitherMustBePresent(fields=args, func_name="either")


def pass_through_callables(
    callables: tuple[typing.Callable[[T], T], ...],
    initial: T,
) -> T:

    i_callables: typing.Iterator[typing.Callable[[T], T]] = iter(callables)
    result = next(i_callables)(initial)

    for caller in i_callables:
        result: T = caller(result)  # type: ignore

    return result
