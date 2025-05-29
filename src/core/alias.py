from datetime import datetime

from src.data.models.report_model import ReportModel

ProgramDay = list[ReportModel]
ProgramPHD = dict[datetime.date, ProgramDay]
