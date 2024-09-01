from collections.abc import Callable
from functools import wraps

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.config import settings

engine = create_async_engine(
    url=settings.db.url,
    echo=settings.alchemy.echo,
    echo_pool=settings.alchemy.echo_pool,
    max_overflow=settings.alchemy.max_overflow,
)
session_factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def inject_session(fn: Callable) -> Callable:
    @wraps(fn)
    async def wrapper(*args: any, **kwargs: any) -> any:
        async with session_factory() as session:
            return await fn(session, *args, **kwargs)

    return wrapper
