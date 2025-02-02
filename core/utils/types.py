import typing
from pathlib import Path

Certfile = typing.NewType("Certfile", str)
Keyfile = typing.NewType("Keyfile", str)
KeyfilePassword = typing.NewType("KeyfilePassword", str)
CAPath = typing.NewType("CAPath", Path)
