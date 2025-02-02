import abc
import typing

from core.third_party.requests.entities import Response


class RequestsBase(abc.ABC):
    possible_exceptions: tuple[type[Exception], ...] = ()

    @abc.abstractmethod
    def post_request(
        self,
        url: str,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[str, typing.Any],
    ) -> Response: ...

    @abc.abstractmethod
    def get_request(
        self,
        url: str,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[str, typing.Any],
    ) -> Response: ...

    @abc.abstractmethod
    def delete_request(
        self,
        url: str,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[str, typing.Any],
    ) -> Response: ...

    @abc.abstractmethod
    def patch_request(
        self,
        url: str,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[str, typing.Any],
    ) -> Response: ...

    @abc.abstractmethod
    def put_request(
        self,
        url: str,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[str, typing.Any],
    ) -> Response: ...
