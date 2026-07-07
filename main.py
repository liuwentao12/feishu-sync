from config import (
    CSV_FILE_PATH,
    FEISHU_APP_ID,
    FEISHU_APP_SECRET,
    FEISHU_SPREADSHEET_TOKEN,
)
from csv_reader import read_csv
from feishu_client import (
    FeishuClient,
    get_rows_dimensions,
    get_sheet_dimensions,
)


def main() -> None:
    rows = read_csv(CSV_FILE_PATH)
    csv_row_count, csv_column_count = get_rows_dimensions(
        rows
    )

    print(f"CSV file: {CSV_FILE_PATH}")
    print(
        f"CSV size: "
        f"{csv_row_count} rows x {csv_column_count} columns"
    )

    client = FeishuClient(
        app_id=FEISHU_APP_ID,
        app_secret=FEISHU_APP_SECRET,
    )

    sheets = client.get_sheets(
        FEISHU_SPREADSHEET_TOKEN
    )

    if not sheets:
        raise RuntimeError(
            "No sheets found in the spreadsheet"
        )

    sheet = sheets[0]
    sheet_id = sheet["sheet_id"]
    row_count, column_count = get_sheet_dimensions(
        sheet
    )

    print(
        f"Sheet: {sheet['title']}, "
        f"ID: {sheet_id}"
    )

    client.clear_values(
        spreadsheet_token=FEISHU_SPREADSHEET_TOKEN,
        sheet_id=sheet_id,
        row_count=row_count,
        column_count=column_count,
    )

    client.write_values(
        spreadsheet_token=FEISHU_SPREADSHEET_TOKEN,
        sheet_id=sheet_id,
        rows=rows,
    )

    print("Sync completed")


if __name__ == "__main__":
    main()
