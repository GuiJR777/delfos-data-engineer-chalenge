# Calculo de intervalo de datas do ETL.

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta


@dataclass(frozen=True)
class DateRange:
    start: datetime
    end: datetime


class EtlDateRangeCalculator:
    def get_date_range(self, target_date: date) -> DateRange:
        day_start = datetime.combine(target_date, time.min)
        day_end = day_start + timedelta(days=1)
        return DateRange(start=day_start, end=day_end)

