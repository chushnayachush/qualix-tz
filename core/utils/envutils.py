from typing import NoReturn


def str2bool(value: str) -> bool | NoReturn:
    if value in ["true", "True"]:
        return True
    elif value in ["false", "False"]:
        return False

    raise ValueError(f"Expected bool str, got {repr(value), type(value)} instead")
