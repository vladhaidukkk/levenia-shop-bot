class CustomError(Exception):
    pass


class UserAlreadyExistsError(CustomError):
    def __init__(self, tg_id: int) -> None:
        super().__init__(f"user with tg_id={tg_id} already exists")


class UserNotFoundError(CustomError):
    def __init__(self, tg_id: int) -> None:
        super().__init__(f"user with tg_id={tg_id} not found")
