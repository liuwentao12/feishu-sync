import os

from dotenv import load_dotenv


load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return value


FEISHU_APP_ID = get_required_env(
    "FEISHU_APP_ID"
)

FEISHU_APP_SECRET = get_required_env(
    "FEISHU_APP_SECRET"
)

FEISHU_SPREADSHEET_TOKEN = get_required_env(
    "FEISHU_SPREADSHEET_TOKEN"
)

CSV_FILE_PATH = get_required_env(
    "CSV_FILE_PATH"
)