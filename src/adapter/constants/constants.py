from os import getenv

NAME_MIN_LENGTH = int(getenv("FLASK_APP_ORDER_NAME_MIN_LENGTH", 3))
NAME_MAX_LENGTH = int(getenv("FLASK_APP_ORDER_NAME_MAX_LENGTH", 300))
ADDRESS_MIN_LENGTH = int(getenv("FLASK_APP_ORDER_ADDRESS_MIN_LENGTH", 3))
ADDRESS_MAX_LENGTH = int(getenv("FLASK_APP_ORDER_ADDRESS_MAX_LENGTH", 300))
