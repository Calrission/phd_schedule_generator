import dataclasses


@dataclasses.dataclass
class PaginationModel:
    page: int
    page_size: int
    page_count: int
    total: int

    @staticmethod
    def from_json(json: dict) -> 'PaginationModel':
        return PaginationModel(
            page=json['page'],
            page_size=json['pageSize'],
            page_count=json['pageCount'],
            total=json['total']
        )

    def __str__(self):
        return f"page={self.page} pageSize={self.page_size} pageCount={self.page_count} total={self.total}"
