####################################################################
# Tests for aws/lambda_scripts/BronzeApiCaptureBreweries.py
#
# Strategy: the Lambda executes AWS calls at module-level (Logs,
# Dynamo, AwsManager). We inject mocks into sys.modules BEFORE
# importing the Lambda so no real AWS calls are made.
# All tests run fully offline — no credentials required.
####################################################################

import sys
import os
import json
import re
import importlib
from unittest.mock import MagicMock, patch, call
import pytest
import urllib3

# ── Environment variables required by the Lambda at import time ──────────────
os.environ.setdefault("S3_BUCKET", "test-bucket")
os.environ.setdefault("ENV", "test")

# ── Add Lambda directory to path (flat imports: from utils import ...) ────────
_LAMBDA_DIR  = os.path.join(os.path.dirname(__file__), "..", "aws", "lambda_scripts")
_MODULES_DIR = os.path.join(os.path.dirname(__file__), "..", "aws", "modules")
sys.path.insert(0, os.path.abspath(_LAMBDA_DIR))
sys.path.insert(0, os.path.abspath(_MODULES_DIR))

# ── Stub custom AWS modules before the Lambda is imported ────────────────────
_mock_logger  = MagicMock()
_mock_dynamo  = MagicMock()
_mock_manager = MagicMock()

_mock_dynamo.get_dynamo_records.return_value = {}
_mock_dynamo.get_email_notif.return_value    = ([], [], [])

_mock_logs_module    = MagicMock()
_mock_utils_module   = MagicMock()
_mock_support_module = MagicMock()

_mock_logs_module.Logs.return_value         = _mock_logger
_mock_utils_module.Dynamo.return_value      = _mock_dynamo
_mock_utils_module.AwsManager.return_value  = _mock_manager

sys.modules.setdefault("logs",    _mock_logs_module)
sys.modules.setdefault("utils",   _mock_utils_module)
sys.modules.setdefault("support", _mock_support_module)

# ── Safe to import  ────────────────────────────────────────────
import BronzeApiCaptureBreweries as lm


########## get_json ##########

class TestGetJson:

    def test_returns_parsed_json_on_200(self):
        mock_resp        = MagicMock()
        mock_resp.status = 200
        mock_resp.data   = json.dumps({"total": "100"}).encode()

        with patch.object(lm.http, "request", return_value=mock_resp):
            result = lm.get_json("https://example.com")

        assert result == {"total": "100"}

    def test_raises_after_all_retries_on_5xx(self):
        mock_resp        = MagicMock()
        mock_resp.status = 500

        with patch.object(lm.http, "request", return_value=mock_resp), \
             patch("BronzeApiCaptureBreweries.time.sleep"):
            with pytest.raises(RuntimeError, match="attempts failed"):
                lm.get_json("https://example.com")

    def test_raises_after_all_retries_on_connection_error(self):
        with patch.object(lm.http, "request", side_effect=urllib3.exceptions.HTTPError("timeout")), \
             patch("BronzeApiCaptureBreweries.time.sleep"):
            with pytest.raises(RuntimeError, match="attempts failed"):
                lm.get_json("https://example.com")

    def test_retries_correct_number_of_times(self):
        mock_resp        = MagicMock()
        mock_resp.status = 503

        with patch.object(lm.http, "request", return_value=mock_resp) as mock_req, \
             patch("BronzeApiCaptureBreweries.time.sleep"):
            with pytest.raises(RuntimeError):
                lm.get_json("https://example.com")

        assert mock_req.call_count == lm.MAX_RETRIES


########## fetch_all_breweries ##########

class TestFetchAllBreweries:

    def test_returns_all_records_single_page(self):
        breweries = [{"id": "1"}, {"id": "2"}, {"id": "3"}]

        with patch.object(lm, "get_json", side_effect=[{"total": "3"}, breweries]):
            result = lm.fetch_all_breweries()

        assert len(result) == 3
        assert result[0]["id"] == "1"

    def test_raises_when_total_is_zero(self):
        with patch.object(lm, "get_json", return_value={"total": "0"}):
            with pytest.raises(ValueError, match="total=0"):
                lm.fetch_all_breweries()

    def test_paginates_across_multiple_pages(self):
        meta  = {"total": "3"}
        page1 = [{"id": "1"}, {"id": "2"}]
        page2 = [{"id": "3"}]

        original_per_page = lm.PER_PAGE
        lm.PER_PAGE = 2
        try:
            with patch.object(lm, "get_json", side_effect=[meta, page1, page2]):
                result = lm.fetch_all_breweries()
        finally:
            lm.PER_PAGE = original_per_page

        assert len(result) == 3

    def test_ceiling_division_page_count(self):
        # 5 records / 2 per page → 3 pages (ceiling)
        meta  = {"total": "5"}
        pages = [[{"id": str(i)}] for i in range(3)]  # 3 page responses

        original_per_page = lm.PER_PAGE
        lm.PER_PAGE = 2
        try:
            with patch.object(lm, "get_json", side_effect=[meta] + pages):
                result = lm.fetch_all_breweries()
        finally:
            lm.PER_PAGE = original_per_page

        assert len(result) == 3  # 1 record per page in our mock


########## upload_to_s3 ##########

class TestUploadToS3:

    def setup_method(self):
        lm.manager.s3.put_s3_file.reset_mock()

    def test_calls_s3_put_once(self):
        lm.upload_to_s3([{"id": "1"}])
        lm.manager.s3.put_s3_file.assert_called_once()

    def test_uses_correct_bucket(self):
        lm.upload_to_s3([{"id": "1"}])
        kwargs = lm.manager.s3.put_s3_file.call_args.kwargs
        assert kwargs["bucket"] == "test-bucket"

    def test_key_contains_ingestion_date_partition(self):
        ingestion_date, _ = lm.upload_to_s3([{"id": "1"}])
        kwargs = lm.manager.s3.put_s3_file.call_args.kwargs
        assert f"ingestion_date={ingestion_date}" in kwargs["key"]

    def test_returns_valid_ingestion_date_format(self):
        ingestion_date, _ = lm.upload_to_s3([{"id": "1"}])
        assert re.match(r"^\d{4}-\d{2}-\d{2}$", ingestion_date)

    def test_returns_filename_with_json_extension(self):
        _, filename = lm.upload_to_s3([{"id": "1"}])
        assert filename.startswith("data_") and filename.endswith(".json")

    def test_body_is_valid_json_string(self):
        data = [{"id": "1", "name": "Test Brewery"}]
        lm.upload_to_s3(data)
        kwargs = lm.manager.s3.put_s3_file.call_args.kwargs
        parsed = json.loads(kwargs["body"])
        assert parsed[0]["name"] == "Test Brewery"


########## lambda_handler ##########

class TestLambdaHandler:

    def test_returns_200_on_success(self):
        breweries = [{"id": "1"}]

        with patch.object(lm, "fetch_all_breweries", return_value=breweries), \
             patch.object(lm, "upload_to_s3", return_value=("2026-03-08", "data_120000.json")):
            response = lm.lambda_handler({}, None)

        assert response["statusCode"] == 200

    def test_response_includes_total_records(self):
        breweries = [{"id": str(i)} for i in range(42)]

        with patch.object(lm, "fetch_all_breweries", return_value=breweries), \
             patch.object(lm, "upload_to_s3", return_value=("2026-03-08", "data_120000.json")):
            response = lm.lambda_handler({}, None)

        assert response["total_records"] == 42

    def test_raises_and_sends_email_on_failure(self):
        lm.manager.ses.send_email_on_failure.reset_mock()

        with patch.object(lm, "fetch_all_breweries", side_effect=RuntimeError("API down")):
            with pytest.raises(RuntimeError):
                lm.lambda_handler({}, None)

        lm.manager.ses.send_email_on_failure.assert_called_once()
