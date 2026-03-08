####################################################################
# Tests for aws/modules/support.py
#
# All functions here are pure Python with no AWS dependencies,
# so no mocking is required — tests run fully offline.
####################################################################

import re
import pytest
from unittest.mock import MagicMock

from aws.modules.support import (
    summarize_exception,
    get_date_and_time,
    split_target_table,
    eval_values,
    write_error_logs,
)


########## summarize_exception ##########

class TestSummarizeException:

    def test_returns_empty_string_for_none(self):
        assert summarize_exception(None) == ""

    def test_returns_empty_string_for_empty_file_sentinel(self):
        assert summarize_exception(Exception("empty_file")) == ""

    def test_empty_file_sentinel_is_case_insensitive(self):
        assert summarize_exception(Exception("EMPTY_FILE")) == ""
        assert summarize_exception(Exception("Empty_File")) == ""

    def test_returns_structured_string_for_python_exception(self):
        try:
            raise ValueError("something went wrong")
        except ValueError as e:
            result = summarize_exception(e)

        assert "ValueError" in result
        assert "something went wrong" in result
        assert "Python interpreter" in result

    def test_includes_line_number_in_result(self):
        try:
            raise RuntimeError("bad state")
        except RuntimeError as e:
            result = summarize_exception(e)

        assert "line_number" in result

    def test_different_exception_types_are_reflected(self):
        try:
            raise KeyError("missing key")
        except KeyError as e:
            result = summarize_exception(e)

        assert "KeyError" in result


########## get_date_and_time ##########

class TestGetDateAndTime:

    def test_returns_string(self):
        result = get_date_and_time()
        assert isinstance(result, str)

    def test_format_is_correct(self):
        result = get_date_and_time()
        assert re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", result)


########## split_target_table ##########

class TestSplitTargetTable:

    def test_standard_two_segment_table(self):
        table_name, source = split_target_table("breweries_tb_breweries")
        assert table_name == "tb_breweries"
        assert source == "breweries"

    def test_multi_segment_table_name(self):
        table_name, source = split_target_table("src_tb_fact_sales")
        assert table_name == "tb_fact_sales"
        assert source == "src"

    def test_source_is_always_first_segment(self):
        _, source = split_target_table("openbrewery_tb_breweries_agg")
        assert source == "openbrewery"

    def test_table_name_joins_remaining_segments(self):
        table_name, _ = split_target_table("openbrewery_tb_breweries_agg")
        assert table_name == "tb_breweries_agg"


########## eval_values ##########

class TestEvalValues:

    def test_true_string_returns_bool_true(self):
        assert eval_values("true") is True

    def test_false_string_returns_bool_false(self):
        assert eval_values("false") is False

    def test_boolean_strings_are_case_insensitive(self):
        assert eval_values("True") is True
        assert eval_values("FALSE") is False

    def test_dict_string_returns_dict(self):
        result = eval_values('{"key": "value"}')
        assert result == {"key": "value"}

    def test_list_string_returns_list(self):
        result = eval_values("[1, 2, 3]")
        assert result == [1, 2, 3]

    def test_integer_string_returns_int(self):
        assert eval_values("42") == 42

    def test_non_string_passthrough(self):
        assert eval_values(100) == 100
        assert eval_values(3.14) == 3.14

    def test_none_returns_none(self):
        assert eval_values(None) is None

    def test_empty_string_returns_empty_string(self):
        assert eval_values("") == ""

    def test_invalid_string_raises_exception(self):
        with pytest.raises(Exception, match="Parsing error"):
            eval_values("not_a_valid_python_expression ::::")


########## write_error_logs ##########

class TestWriteErrorLogs:

    def test_always_raises_exception(self):
        with pytest.raises(Exception):
            write_error_logs(
                logger=None,
                error_msg="job failed",
                e=Exception("some error"),
            )

    def test_exception_message_contains_error_msg(self):
        with pytest.raises(Exception, match="job failed"):
            write_error_logs(
                logger=None,
                error_msg="job failed",
                e=Exception("some error"),
            )

    def test_calls_logger_error_when_logger_is_provided(self):
        mock_logger = MagicMock()
        try:
            raise Exception("some error")
        except Exception as e:
            caught = e
        with pytest.raises(Exception):
            write_error_logs(
                logger=mock_logger,
                error_msg="job failed",
                e=caught,
            )
        mock_logger.error.assert_called_once()

    def test_sends_email_when_destination_is_set(self):
        mock_super = MagicMock()
        with pytest.raises(Exception):
            write_error_logs(
                logger=None,
                error_msg="job failed",
                e=Exception("some error"),
                destination=["user@example.com"],
                super=mock_super,
                target_tbl="breweries_tb_breweries",
            )
        mock_super.send_email_on_failure.assert_called_once()

    def test_skips_email_for_empty_file_sentinel(self):
        mock_super = MagicMock()
        with pytest.raises(Exception):
            write_error_logs(
                logger=None,
                error_msg="no data",
                e=Exception("empty_file"),
                destination=["user@example.com"],
                super=mock_super,
                target_tbl="breweries_tb_breweries",
            )
        mock_super.send_email_on_failure.assert_not_called()
