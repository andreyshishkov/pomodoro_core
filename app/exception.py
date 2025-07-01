class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "User not correct password"


class TokenExpiredException(Exception):
    detail = "Access token has expired"


class TokenNotCorrectedError(Exception):
    detail = "Token is not corrected"


class TaskNotFoundedException(Exception):
    detail = "Task is not founded"
