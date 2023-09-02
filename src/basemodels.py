from typing import Any, Generic, Self, TypeVar
from pydantic import BaseModel
from pydantic.config import ConfigDict
from pydantic.functional_validators import model_validator

from src.exceptions import MandatoryFieldHasNoneValue, MutationNotAllowed
from src.custom_types import T


class Model(BaseModel):
    pass


class MutableModel(Model):
    model_config = ConfigDict(extra="allow", frozen=False, arbitrary_types_allowed=True)


class ImmutableModel(MutableModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    def _nested_getattr(self, key: str) -> Self:
        """
        So the idea is that we get
            key = "a.b.c"
        where all a,b,c are nested ImmutableModels of self, we have to return c using getattr method
        :param key: str
        :return: Self
        """
        key_split = key.split(".")

        value: Self = getattr(self, key_split.pop(0))

        for _field in key_split:
            value = getattr(value, _field)

        return value

    def _copy(self, key: str, value: T, deep: bool = False) -> Self:
        """
        The core of my recursive genius!

        _copy is responsible for updating the nested attribute and reattaching of the
        attributes as it moves outward.

        Details:
        --------------------------------------------------------
        key = "a.b.c"
        value = Object)

        in try block:
            model_attr_name = "b"
            attr_name = "c"

            # self.model_fields in the following lines also make sure that '_copy'
            # and in turn 'new' is called only on the current object.
            # It is the current object we are editing

            _obj = self.model_fields[model_attr_name] # So a FieldInfo object
            _obj.default contains value of model_attr_name for the "a" class
            model_attr_name must be a Basemodel subclass name, better if it's my ImmutableModel subclass name

            recursive call _copy (

                key = "a.b",

                # Remember _obj.default (b) being a BaseModel subclass
                value = _obj.default.model_copy(
                        update = { attr_name , value }
                )

            )

        in Except block

        :param key:
        :param value:
        :return:
        """

        key_split = key.split(".")

        try:
            model_attr_name = key_split[-2]  # this will raise the IndexError
            attr_name = key_split[-1]
            model_attr_key = ".".join(key_split[:-1])

            if (_obj := self._nested_getattr(key=model_attr_key)) is None:
                raise AttributeError(
                    f"[X] Field: {key} is missing attribute: {model_attr_name}"
                )

            if not hasattr(_obj, "model_copy"):
                raise ValueError(
                    f"[X] Key: {key} includes a non-pydantic model class "
                    f"attribute: {model_attr_name}, with class: {_obj.__class__}"
                )

            return self._copy(
                key=model_attr_key,
                value=_obj.model_copy(update={attr_name: value}, deep=deep),
                deep=deep,
            )

        except IndexError:
            model_attr_name = key_split.pop(0)
            _obj = getattr(self, model_attr_name)
            return self.model_copy(update={model_attr_name: value}, deep=deep)

    def new(self, key: str, value: T, deep: bool = False) -> Self:
        """
        This is probably my best contribution to recursive coding,
        The new method relies on internal _copy method which in-turn relies on Model.model_copy method
        so the reliance priority is:
            new -> _copy -> Model.model_copy

        This acts as a bridge between the _copy method for additional experiments!
        :param deep: boolean for deep copy propagation of other attributes too.
        :param key: name of the attribute to be changed during copy generation
        :param value: value of the attribute to be set
        :return: a new model of Self
        """
        return self._copy(key=key, value=value, deep=deep)


TImm = TypeVar("TImm", bound=ImmutableModel)


class MandatoryImmutable(ImmutableModel):
    @model_validator(mode="before")
    def validate_mandatory(cls, data: dict[str, Any]) -> dict[str, Any]:
        for field_name, field_value in data.items():
            if field_value is None:
                raise MandatoryFieldHasNoneValue(field=field_name, cls=cls.__class__)

        return data


class Proxy(MandatoryImmutable, Generic[T]):
    of: T

    def mutation_not_allowed(self, *args, **kwargs):
        raise MutationNotAllowed(cls=self.__class__, field="of")


class DictProxy(Proxy[dict[Any, Any]]):
    def get(self, key, *args, **kwargs):
        return self.of.get(key, *args, **kwargs)

    def __getitem__(self, item):
        return self.of.__getitem__(item)

    def __contains__(self, item):
        return self.of.__contains__(item)

    def values(self):
        return self.of.values()

    def items(self):
        return self.of.items()

    def keys(self):
        return self.of.keys()

    def __iter__(self, *args, **kwargs):
        return self.of.__iter__()

    def clear(self):
        return self.mutation_not_allowed()

    def pop(self, k, d=None):
        return self.mutation_not_allowed(k, d)

    def popitem(self, *args, **kwargs):
        return self.mutation_not_allowed(*args, **kwargs)

    def update(self, E=None, **F):
        return self.mutation_not_allowed(E, **F)

    def setdefault(self, *args, **kwargs):
        return self.mutation_not_allowed(*args, **kwargs)

    def some(self, within: frozenset[T]) -> Self:
        patch_details = {}

        for elem in within:
            if (details := self.get(key=elem)) is None:
                continue
            patch_details[elem] = details

        return self.new(key="of", value=patch_details)


class EnvVar(MandatoryImmutable, Generic[T]):
    name: str
    value: T
