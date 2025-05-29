import dataclasses


@dataclasses.dataclass
class SpeakerModel:
    id: int
    name: str
    company: str

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            "company": self.company,
        }

    @staticmethod
    def from_json(json: dict):
        return SpeakerModel(
            id=json['id'],
            name=json['name'],
            company=json['company'],
        )
