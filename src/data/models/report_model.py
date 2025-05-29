import dataclasses
from datetime import datetime
from typing import Optional
from src.core.datetime_utils import decoder, time2str
from src.data.models.map_object_model import MapObjectModel
from src.data.models.speaker_model import SpeakerModel
from src.data.models.tag_model import TagModel
from src.data.models.talk_type_model import TalkType


@dataclasses.dataclass
class ReportModel:
    id: int
    title: str
    start_date: datetime
    end_date: datetime
    description: Optional[str]
    speakers: list[SpeakerModel]
    talk_type: Optional[TalkType]
    is_visible_in_broadcast: bool
    tag: TagModel
    map_object: MapObjectModel

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "startDate": self.start_date.isoformat(),
            "endDate": self.end_date.isoformat(),
            "description": self.description,
            "speakers": [i.to_json() for i in self.speakers],
            "talkType": self.talk_type.to_json() if self.talk_type is not None else None,
            "isVisibleInBroadcast": self.is_visible_in_broadcast,
            "tag": self.tag.to_json(),
            "mapObject": self.map_object.to_json(),
        }

    @staticmethod
    def from_json(json: dict) -> 'ReportModel':
        return ReportModel(
            id=json["id"],
            title=json["title"],
            start_date=decoder(json["startDate"]),
            end_date=decoder(json["endDate"]),
            description=json["description"],
            speakers=[SpeakerModel.from_json(i) for i in json['speakers']],
            talk_type=TalkType.from_json(json["talkType"]) if json["talkType"] is not None else None,
            is_visible_in_broadcast=json["isVisibleInBroadcast"],
            tag=TagModel.from_json(json["tag"]),
            map_object=MapObjectModel.from_json(json["mapObject"]),
        )

    @property
    def time(self):
        return f"{time2str(self.start_date.time())}-{time2str(self.end_date.time())}"
