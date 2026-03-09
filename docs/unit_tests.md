# Unit Tests

All tests run **fully offline** — no AWS credentials, no network access, no infrastructure required.

> [!NOTE]
> For project context, see the [Architecture Overview](architecture.md) and [Modules Reference](modules.md).

---

## How to Run

**Install pytest:**
```bash
pip install pytest
```

**Run all tests:**
```bash
pytest tests/ -v
```

**On Linux/macOS only:**
```bash
make test
```

---

## Test Files

| File | Module Tested | Tests |
|---|---|---|
| [tests/test_support.py](../tests/test_support.py) | `aws/modules/support.py` | 27 |
| [tests/test_lambda_bronze.py](../tests/test_lambda_bronze.py) | `aws/lambda_scripts/BronzeApiCaptureBreweries.py` | 17 |

**Total: 44 tests**

---

## test_support.py — 27 tests

Tests for `support.py`, which contains pure Python utility functions with no AWS dependencies. No mocking required.

### TestSummarizeException (6 tests)

| Test | Description |
|---|---|
| `test_returns_empty_string_for_none` | `None` as input returns `""` |
| `test_returns_empty_string_for_empty_file_sentinel` | `Exception("empty_file")` returns `""` |
| `test_empty_file_sentinel_is_case_insensitive` | `EMPTY_FILE`, `Empty_File` all return `""` |
| `test_returns_structured_string_for_python_exception` | Result includes exception type and message |
| `test_includes_line_number_in_result` | Result includes `line_number` field |
| `test_different_exception_types_are_reflected` | Exception type (e.g. `KeyError`) appears in result |

### TestGetDateAndTime (2 tests)

| Test | Description |
|---|---|
| `test_returns_string` | Return value is a string |
| `test_format_is_correct` | Format matches `YYYY-MM-DD HH:MM:SS` |

### TestSplitTargetTable (4 tests)

| Test | Description |
|---|---|
| `test_standard_two_segment_table` | `"breweries_tb_breweries"` → `("tb_breweries", "breweries")` |
| `test_multi_segment_table_name` | `"src_tb_fact_sales"` → `("tb_fact_sales", "src")` |
| `test_source_is_always_first_segment` | Source is always the first segment |
| `test_table_name_joins_remaining_segments` | Table name joins all segments after the first |

### TestEvalValues (10 tests)

| Test | Description |
|---|---|
| `test_true_string_returns_bool_true` | `"true"` → `True` |
| `test_false_string_returns_bool_false` | `"false"` → `False` |
| `test_boolean_strings_are_case_insensitive` | `"True"`, `"FALSE"` handled correctly |
| `test_dict_string_returns_dict` | `'{"key": "value"}'` → `dict` |
| `test_list_string_returns_list` | `"[1, 2, 3]"` → `list` |
| `test_integer_string_returns_int` | `"42"` → `42` |
| `test_non_string_passthrough` | `int` and `float` passed through unchanged |
| `test_none_returns_none` | `None` → `None` |
| `test_empty_string_returns_empty_string` | `""` → `""` |
| `test_invalid_string_raises_exception` | Invalid expression raises `Exception("Parsing error")` |

### TestWriteErrorLogs (5 tests)

| Test | Description |
|---|---|
| `test_always_raises_exception` | Function always raises after logging |
| `test_exception_message_contains_error_msg` | Raised exception message contains `error_msg` |
| `test_calls_logger_error_when_logger_is_provided` | `logger.error()` is called once |
| `test_sends_email_when_destination_is_set` | `send_email_on_failure` called when `destination` is provided |
| `test_skips_email_for_empty_file_sentinel` | Email skipped when exception is the `empty_file` sentinel |

---

## test_lambda_bronze.py — 17 tests

Tests for `BronzeApiCaptureBreweries.py`. The Lambda instantiates AWS clients (`Logs`, `Dynamo`, `AwsManager`) at module level, so mocks are injected into `sys.modules` before the import. No real AWS calls are made.

### TestGetJson (4 tests)

| Test | Description |
|---|---|
| `test_returns_parsed_json_on_200` | HTTP 200 returns parsed JSON |
| `test_raises_after_all_retries_on_5xx` | 5xx response raises `RuntimeError` after all retries |
| `test_raises_after_all_retries_on_connection_error` | Connection error raises `RuntimeError` after all retries |
| `test_retries_correct_number_of_times` | Request is called exactly `MAX_RETRIES` times |

### TestFetchAllBreweries (4 tests)

| Test | Description |
|---|---|
| `test_returns_all_records_single_page` | Single page returns all records |
| `test_raises_when_total_is_zero` | `total=0` raises `ValueError` |
| `test_paginates_across_multiple_pages` | Correctly aggregates results across multiple pages |
| `test_ceiling_division_page_count` | Page count uses ceiling division (`math.ceil`) |

### TestUploadToS3 (6 tests)

| Test | Description |
|---|---|
| `test_calls_s3_put_once` | `put_s3_file` is called exactly once |
| `test_uses_correct_bucket` | Uses the bucket from `S3_BUCKET` env var |
| `test_key_contains_ingestion_date_partition` | S3 key includes `ingestion_date=YYYY-MM-DD` partition |
| `test_returns_valid_ingestion_date_format` | Returned date matches `YYYY-MM-DD` |
| `test_returns_filename_with_json_extension` | Returned filename starts with `data_` and ends with `.json` |
| `test_body_is_valid_json_string` | S3 body is valid JSON with correct content |

### TestLambdaHandler (3 tests)

| Test | Description |
|---|---|
| `test_returns_200_on_success` | Successful run returns `statusCode: 200` |
| `test_response_includes_total_records` | Response includes correct `total_records` count |
| `test_raises_and_sends_email_on_failure` | On failure, raises exception and calls `send_email_on_failure` |
