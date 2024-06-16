from secrets import token_hex

from main import settings


def gen_category_key() -> str:
    return token_hex(settings.CATEGORY_KEY_SIZE)

