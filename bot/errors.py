class CustomError(Exception):
    pass


class UserAlreadyExistsError(CustomError):
    def __init__(self, tg_id: int) -> None:
        super().__init__(f"user with tg_id={tg_id} already exists")


class UserNotFoundError(CustomError):
    def __init__(self, tg_id: int) -> None:
        super().__init__(f"user with tg_id={tg_id} not found")


class ReferralAlreadyExistsError(CustomError):
    def __init__(self, user_tg_id: int) -> None:
        super().__init__(f"referral for user with tg_id={user_tg_id} already exists")


class ProductNotFoundError(CustomError):
    def __init__(self, id_: int) -> None:
        super().__init__(f"product with id={id_} not found")


class ProductAlreadyDeletedError(CustomError):
    def __init__(self, id_: int) -> None:
        super().__init__(f"product with id={id_} is already deleted")
