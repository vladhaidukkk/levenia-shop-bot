import datetime as dt
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[dt.datetime, mapped_column(server_default=func.current_timestamp())]
