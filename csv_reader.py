import csv


def read_csv(file_path: str) -> list[list[str]]:
    rows = []

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.reader(file)

        for row in reader:
            rows.append(row)

    return rows