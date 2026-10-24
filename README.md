# 📊 Nginx Log File Analyzer

A Python tool that reads Apache/nginx-style access logs, parses each line with a regular expression, and produces a plain-text report of request counts, status codes, unique IPs, response size, and top URLs.

It streams files line by line, so you can analyze one or more logs without loading the whole input into memory first.

---

## 🚀 Setup and usage

**Requirements:** Python 3.12+ and [Poetry](https://python-poetry.org/).

```bash
poetry install --with dev
```

Analyze one or more log files (sample data lives in `data/`):

```bash
poetry run python -m src.main data/access_1.log
poetry run python -m src.main data/access_1.log data/access_2.log
```

Optional filters and output path:

```bash
poetry run python -m src.main data/access_1.log --status 404 --ip 192.168.1.10 --output reports/report.txt
```

| Flag | Meaning |
| --- | --- |
| `files` | One or more log file paths (required) |
| `--status` | Keep only this HTTP status code |
| `--ip` | Keep only this client IP |
| `--output` | Report path (default: `reports/report.txt`) |

The report is printed to the terminal and saved to the output file.

---

## 🔎 Regex explanation

Each valid line matches Common Log Format without ident/user fields, for example:

```text
192.168.1.10 - - [21/Oct/2026:12:50:00 +0200] "GET /index.html HTTP/1.1" 200 512
```

Named groups in `src/patterns.py`:

| Group | Captures |
| --- | --- |
| `ip` | Client IPv4 address (`192.168.1.10`) |
| `timestamp` | Request time inside `[...]` (`21/Oct/2026:12:50:00 +0200`) |
| `method` | HTTP verb (`GET`, `POST`, …) |
| `url` | Request path and query (`/index.html`) |
| `status` | Three-digit HTTP status (`200`) |
| `bytes` | Response size in bytes, or `-` when the size is unknown |

Lines that do not match are skipped. A `-` byte count becomes `None` after parsing.

---

## ⚙️ Functional pipeline

Parsed entries move through a lazy pipeline (`map` / `filter`) before aggregation:

1. **Transform** — uppercase the method and strip the URL.
2. **Filter** (optional) — keep entries by status, IP, and/or time range.
3. **Aggregate** — count requests, unique IPs, bytes, errors, methods, statuses, top URLs, and hourly volume.

```text
log files → read lines → parse → transform → filter → report
```

Nothing runs until the report consumes the iterator. Multiple files are chained into one stream.

---

## 🧠 Generators vs. lists

| | List | Generator |
| --- | --- | --- |
| **Memory** | Holds every line (or entry) at once | Holds one item at a time while reading |
| **Processing** | Work starts after the full load | Work happens as each line is read |
| **Reuse** | Can scan the same collection again | Consumed once; re-open the file to repeat |

This project uses generators for reading and filtering. `generate_report` still materializes the filtered entries so it can compute several stats in one pass.

---

## ⚡ Performance comparison

Measured on **`data/access_1.log`** (1,200 lines, 95,856 bytes). Both approaches parse each line and count statuses. Timing used `time.perf_counter()`; peak memory used `tracemalloc`. Figures are 5 runs after a warm-up (average time, highest peak).

| Approach | What it does | Avg time | Peak memory |
| --- | --- | --- | --- |
| **List** | `readlines()` into a list, then parse | 0.173 s | 168,709 bytes (~165 KiB) |
| **Generator** | Yield and parse one line at a time | 0.182 s | 22,806 bytes (~22 KiB) |

On this sample, times are close (the list path was slightly faster). Peak memory for the input sequence was about **7.4× higher** when all lines were stored first (≈146 KiB extra).

A generator cuts memory for the **input sequence**. Parsing, counters, and the report still use memory. Results depend on file size and what you keep after parsing — these numbers are from this workload, not a general guarantee.

---

## 🧪 Testing

```bash
poetry run pytest
```

Latest run:

```text
...................................................................      [100%]
67 passed in 0.36s
```

---

## 📄 Example report

```text
LOG FILE ANALYSIS REPORT
========================
Source: data/access_1.log
Generated: 2026-10-24 21:18:37 +0200

Total requests: 1152
Unique IP addresses: 26
Total response bytes: 2472716
Requests with 4xx/5xx status: 536

Requests by HTTP method:
  DELETE: 204
  GET: 554
  POST: 190
  PUT: 204

Requests by status code:
  200: 303
  201: 110
  204: 105
  301: 98
  400: 107
  401: 110
  403: 103
  404: 108
  500: 108

Top URLs:
  /login: 153
  /search?q=python: 149
  /health: 146
  /missing: 145
  /products/42: 144
  /products: 143
  /api/orders: 137
  /: 135
```
