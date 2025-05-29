import dataclasses


@dataclasses.dataclass
class TagModel:
    id: int
    name: str
    slug: str
    event_type: str

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "eventType": self.event_type,
        }

    @staticmethod
    def from_json(json: dict):
        return TagModel(
            id=json["id"],
            name=json["name"],
            slug=json["slug"],
            event_type=json["eventType"],
        )
