import datetime

tz_info = datetime.datetime.now().astimezone().tzinfo


def decoder(*args) -> datetime.datetime:
    return datetime.datetime.fromisoformat(*args).astimezone(tz_info)


def datetime2str(dt: datetime.datetime) -> str:
    return dt.strftime('%d.%m.%Y %H:%M')


def date2str(dt: datetime.date) -> str:
    return dt.strftime('%d.%m.%Y')


def time2str(time: datetime.time) -> str:
    return time.strftime('%H:%M')


def str2date(date: str) -> datetime.date:
    return datetime.datetime.strptime(date, '%d.%m.%Y').date()


def unix(dt: datetime.datetime) -> float:
    return int(dt.timestamp() * 1000)


def date2datetime(dt: datetime.date, time: datetime.time) -> datetime.datetime:
    return datetime.datetime.combine(dt, time)


def addDelta2Time(time: datetime.time, delta: datetime.timedelta) -> datetime.time:
    return (datetime.datetime.combine(datetime.date(year=1, month=1, day=1), time) + delta).time()
