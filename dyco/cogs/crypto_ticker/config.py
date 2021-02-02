import typing
import dataclasses


@dataclasses.dataclass
class Config:
    channel: int
    separator: str
    pairs: typing.List[typing.Mapping[str, str]]

    @property
    def pairs_dict(self) -> typing.Mapping[str, typing.Mapping[str, str]]:
        return {x["pair"]: x for x in self.pairs}
