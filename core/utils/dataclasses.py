from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class FrozenPatchedDataclass:
    def as_dict(self):
        return asdict(self)
