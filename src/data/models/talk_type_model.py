import dataclasses


@dataclasses.dataclass
class TalkType:
    id: int
    name: str

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    @staticmethod
    def from_json(json: dict) -> 'TalkType':
        return TalkType(
            id=json["id"],
            name=json["name"],
        )
