import dataclasses


@dataclasses.dataclass
class MapObjectTypeModel:
    id: int
    name: str

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    @staticmethod
    def from_json(json: dict):
        return MapObjectTypeModel(
            id=json["id"],
            name=json["name"],
        )


@dataclasses.dataclass
class MapObjectModel:
    id: int
    title: str
    type: str
    event_type: str
    map_object_type: MapObjectTypeModel

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "eventType": self.event_type,
            "mapObjectType": self.map_object_type.to_json(),
        }

    @staticmethod
    def from_json(json: dict):
        return MapObjectModel(
            id=json["id"],
            title=json["title"],
            type=json["type"],
            event_type=json["eventType"],
            map_object_type=MapObjectTypeModel.from_json(json["mapObjectType"]),
        )
