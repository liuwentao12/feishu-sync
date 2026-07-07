import requests


def column_number_to_name(column_number: int) -> str:
    if column_number <= 0:
        raise ValueError("Column number must be greater than 0")

    letters = []

    while column_number > 0:
        column_number, remainder = divmod(
            column_number - 1,
            26,
        )

        letters.append(
            chr(ord("A") + remainder)
        )

    return "".join(reversed(letters))


def build_dimension_range(
    sheet_id: str,
    row_count: int,
    column_count: int,
) -> str:
    if row_count <= 0:
        raise ValueError("Row count must be greater than 0")

    if column_count <= 0:
        raise ValueError("Column count must be greater than 0")

    last_column = column_number_to_name(
        column_count
    )

    return (
        f"{sheet_id}!A1:"
        f"{last_column}{row_count}"
    )


def build_sheet_range(
    sheet_id: str,
    rows: list[list[str]],
) -> str:
    row_count, column_count = get_rows_dimensions(
        rows
    )

    return build_dimension_range(
        sheet_id=sheet_id,
        row_count=row_count,
        column_count=column_count,
    )


def get_rows_dimensions(
    rows: list[list[str]],
) -> tuple[int, int]:
    if not rows:
        raise ValueError("CSV contains no data")

    column_count = len(rows[0])

    if column_count == 0:
        raise ValueError("CSV contains no columns")

    for row_number, row in enumerate(rows, start=1):
        if len(row) != column_count:
            raise ValueError(
                f"Row {row_number} has {len(row)} columns, "
                f"expected {column_count}"
            )

    return len(rows), column_count


def get_sheet_dimensions(sheet: dict) -> tuple[int, int]:
    grid_properties = (
        sheet.get("grid_properties")
        or sheet.get("gridProperties")
        or {}
    )

    row_count = (
        grid_properties.get("row_count")
        or grid_properties.get("rowCount")
        or sheet.get("row_count")
        or sheet.get("rowCount")
    )

    column_count = (
        grid_properties.get("column_count")
        or grid_properties.get("columnCount")
        or sheet.get("column_count")
        or sheet.get("columnCount")
    )

    if row_count is None or column_count is None:
        raise RuntimeError(
            "Sheet dimensions are missing from Feishu response"
        )

    return int(row_count), int(column_count)


class FeishuClient:
    TOKEN_URL = (
        "https://open.feishu.cn/open-apis/"
        "auth/v3/tenant_access_token/internal"
    )

    def __init__(
        self,
        app_id: str,
        app_secret: str,
    ) -> None:
        self.app_id = app_id
        self.app_secret = app_secret
        self._access_token: str | None = None

    def get_access_token(self) -> str:
        if self._access_token:
            return self._access_token

        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
        }

        response = requests.post(
            self.TOKEN_URL,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if data["code"] != 0:
            raise RuntimeError(
                f"Feishu authentication failed: {data}"
            )

        self._access_token = data["tenant_access_token"]

        return self._access_token

    def get_sheets(
        self,
        spreadsheet_token: str,
    ) -> list[dict]:
        access_token = self.get_access_token()

        url = (
            "https://open.feishu.cn/open-apis/"
            f"sheets/v3/spreadsheets/{spreadsheet_token}/"
            "sheets/query"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )

        data = response.json()

        if response.status_code != 200 or data.get("code") != 0:
            raise RuntimeError(
                f"Failed to get sheets: "
                f"HTTP {response.status_code}, "
                f"response={data}"
            )

        return data["data"]["sheets"]

    def clear_values(
        self,
        spreadsheet_token: str,
        sheet_id: str,
        row_count: int,
        column_count: int,
    ) -> None:
        access_token = self.get_access_token()

        target_range = build_dimension_range(
            sheet_id=sheet_id,
            row_count=row_count,
            column_count=column_count,
        )

        print(f"Clearing range: {target_range}")

        url = (
            "https://open.feishu.cn/open-apis/"
            f"sheets/v2/spreadsheets/"
            f"{spreadsheet_token}/values_batch_clear"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "ranges": [
                target_range,
            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10,
        )

        data = response.json()

        if (
            response.status_code != 200
            or data.get("code") != 0
        ):
            raise RuntimeError(
                f"Failed to clear values: "
                f"HTTP {response.status_code}, "
                f"response={data}"
            )

    def write_values(
        self,
        spreadsheet_token: str,
        sheet_id: str,
        rows: list[list[str]],
    ) -> None:
        access_token = self.get_access_token()

        target_range = build_sheet_range(
            sheet_id=sheet_id,
            rows=rows,
        )

        print(f"Writing range: {target_range}")

        url = (
            "https://open.feishu.cn/open-apis/"
            f"sheets/v2/spreadsheets/"
            f"{spreadsheet_token}/values"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "valueRange": {
                "range": target_range,
                "values": rows,
            }
        }

        response = requests.put(
            url,
            headers=headers,
            json=payload,
            timeout=10,
        )

        data = response.json()

        if (
            response.status_code != 200
            or data.get("code") != 0
        ):
            raise RuntimeError(
                f"Failed to write values: "
                f"HTTP {response.status_code}, "
                f"response={data}"
            )
