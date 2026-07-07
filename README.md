# feishu-sync

Synchronize a local CSV file to a Feishu Spreadsheet.

一个轻量级的 CSV → 飞书电子表格同步工具。

`feishu-sync` 读取本地 CSV 文件，通过飞书开放平台 API 将数据写入指定的飞书电子表格。

目前项目处于早期开发阶段，支持手动执行单向全量同步。

## Features

- Read local CSV files
- Authenticate with Feishu Open Platform
- Query spreadsheet sheets automatically
- Automatically calculate the target spreadsheet range
- Write CSV data to Feishu Sheets
- Validate inconsistent CSV row lengths
- Keep application credentials outside source code with `.env`

## How It Works

```text
Local CSV File
       │
       ▼
  csv_reader.py
       │
       ▼
Python 2D List
       │
       ▼
Range Calculation
A1:H17 / A1:AA100
       │
       ▼
 Feishu Sheets API
       │
       ▼
Feishu Spreadsheet
```

Example:

```csv
time,device,version,port,result
2026-07-07 10:20,ESP32,v2.1.0,COM7,SUCCESS
2026-07-07 10:32,ESP32,v2.1.1,COM7,FAILED
```

The CSV data will be written to the target Feishu Spreadsheet.

## Project Structure

```text
feishu-sync/
├── main.py
├── config.py
├── csv_reader.py
├── feishu_client.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Module Responsibilities

`main.py`

Coordinates the synchronization workflow.

`config.py`

Loads and validates environment variables.

`csv_reader.py`

Reads CSV files and converts them into two-dimensional Python lists.

`feishu_client.py`

Handles Feishu authentication, spreadsheet queries, range calculation, and data writing.

## Requirements

- Python 3.10+
- A Feishu custom application
- A Feishu Spreadsheet
- Feishu Sheets API permission
- The application must have access to the target spreadsheet

## Installation

Clone the repository:

```bash
git clone https://github.com/your-name/feishu-sync.git
cd feishu-sync
```

Create a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Copy the example environment file:

### Windows

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Configure `.env`:

```env
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_SPREADSHEET_TOKEN=your_spreadsheet_token
CSV_FILE_PATH=production_records.csv
```

### Spreadsheet Token

For a spreadsheet URL such as:

```text
https://example.feishu.cn/sheets/xxxxxxxxxxxxxxxx
```

the spreadsheet token is:

```text
xxxxxxxxxxxxxxxx
```

## Feishu Configuration

Before running the program:

1. Create a custom application in Feishu Open Platform.
2. Obtain the application's `App ID` and `App Secret`.
3. Enable spreadsheet read/write API permissions.
4. Publish or enable the application as required by your Feishu tenant.
5. Add the application to the target spreadsheet's document applications or collaborators.

Do not commit your real `.env` file.

## Usage

Run:

```bash
python main.py
```

Example output:

```text
CSV file: production_records.csv
CSV size: 17 rows x 8 columns
Sheet: Sheet1, ID: IGxLIP
Clearing range: IGxLIP!A1:H1000
Writing range: IGxLIP!A1:H17
Sync completed
```

## Dynamic Range Calculation

The target range is calculated automatically from the CSV dimensions.

Examples:

```text
3 rows × 5 columns
→ A1:E3

100 rows × 8 columns
→ A1:H100

50 rows × 27 columns
→ A1:AA50
```

Column names beyond `Z` are supported.

## Current Limitations

The current version performs a manual full refresh:

```text
production_records.csv
       |
       v
Read all CSV rows
       |
       v
Clear old Sheet values
       |
       v
Write all CSV rows
       |
       v
Sync completed
```

It does not yet support:

- Automatic file watching
- Incremental synchronization
- Multiple CSV-to-Sheet mappings
- Conflict detection
- Bidirectional synchronization
- CLI commands

## Roadmap

### v0.1

- [x] Read CSV files
- [x] Feishu application authentication
- [x] Query Sheet information
- [x] Dynamic range calculation
- [x] Write CSV data to Feishu Sheets
- [x] Clear stale spreadsheet data before synchronization

### v0.2

- [ ] Select Sheet by name
- [ ] Better configuration validation
- [ ] Improved error handling

### v0.3

- [ ] Watch CSV file changes
- [ ] Debounce frequent file updates
- [ ] Automatic synchronization

### Future

- [ ] Incremental synchronization
- [ ] Multiple file mappings
- [ ] CLI interface
- [ ] Retry and rate-limit handling
- [ ] Docker support
- [ ] GitHub Actions integration

## Security

Never commit:

```text
.env
```

The `.env` file may contain:

- Feishu App ID
- Feishu App Secret
- Spreadsheet Token
- Local file paths

Only `.env.example` should be committed.

## License

MIT License
