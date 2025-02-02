import abc
import typing


class UsecaseBase(abc.ABC):
    @abc.abstractmethod
    def execute(
        self, *args: tuple[typing.Any, ...], **kwargs: dict[typing.Any, typing.Any]
    ) -> typing.Any: ...
