import dataclasses

from src.data.models.pagination_model import PaginationModel
from src.data.models.report_model import ReportModel


@dataclasses.dataclass
class ResponseModel:
    data: list[ReportModel]
    pagination: PaginationModel
    placeholders: dict[str, object]

    @staticmethod
    def from_dict(json: dict, placeholders: dict) -> 'ResponseModel':
        return ResponseModel(
            data=[ReportModel.from_json(i) for i in json["data"]],
            pagination=PaginationModel.from_json(json["pagination"]),
            placeholders=placeholders
        )
