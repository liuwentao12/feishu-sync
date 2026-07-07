from config import (
    CSV_FILE_PATH,
    FEISHU_APP_ID,
    FEISHU_APP_SECRET,
    FEISHU_SPREADSHEET_TOKEN,
)
from csv_reader import read_csv
from feishu_client import FeishuClient


def main() -> None:
    # 1. 读取真实生产记录
    rows = read_csv(CSV_FILE_PATH)

    print(f"CSV rows: {len(rows)}")

    # 2. 创建飞书客户端
    client = FeishuClient(
        app_id=FEISHU_APP_ID,
        app_secret=FEISHU_APP_SECRET,
    )

    # 3. 查询电子表格中的工作表
    sheets = client.get_sheets(
        FEISHU_SPREADSHEET_TOKEN
    )

    if not sheets:
        raise RuntimeError(
            "No sheets found in the spreadsheet"
        )

    # 4. 当前使用第一个 Sheet
    sheet = sheets[0]
    sheet_id = sheet["sheet_id"]

    print(
        f"Sheet: {sheet['title']}, "
        f"ID: {sheet_id}"
    )

    # 5. 写入 CSV
    client.write_values(
        spreadsheet_token=FEISHU_SPREADSHEET_TOKEN,
        sheet_id=sheet_id,
        rows=rows,
    )

    print(
        "CSV written to Feishu successfully"
    )


if __name__ == "__main__":
    main()