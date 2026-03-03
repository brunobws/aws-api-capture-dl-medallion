"""
Unit tests for Athena connector and data processing utilities.

This module contains test cases for the Breweries Dashboard application.

Author: Data Team
Version: 1.0.0
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock


class TestAthenaConnector:
    """Test cases for AthenaConnector class."""

    @pytest.fixture
    def mock_boto3_client(self):
        """Create a mock boto3 client."""
        with patch("boto3.client") as mock_client:
            yield mock_client

    def test_connector_initialization(self, mock_boto3_client):
        """Test AthenaConnector initialization."""
        from streamlit_app.utils.athena_connector import AthenaConnector

        connector = AthenaConnector(
            database="gold",
            s3_output_location="s3://test-bucket/",
            region="sa-east-1"
        )

        assert connector.database == "gold"
        assert connector.region == "sa-east-1"

    def test_execute_query(self, mock_boto3_client):
        """Test query execution."""
        from streamlit_app.utils.athena_connector import AthenaConnector

        mock_client = MagicMock()
        mock_client.start_query_execution.return_value = {"QueryExecutionId": "test-123"}

        with patch("boto3.client", return_value=mock_client):
            connector = AthenaConnector()
            execution_id = connector.execute_query("SELECT * FROM test_table")

            assert execution_id == "test-123"
            mock_client.start_query_execution.assert_called_once()

    def test_health_check(self, mock_boto3_client):
        """Test Athena connection health check."""
        from streamlit_app.utils.athena_connector import AthenaConnector

        mock_client = MagicMock()
        mock_client.list_query_executions.return_value = {}

        with patch("boto3.client", return_value=mock_client):
            connector = AthenaConnector()
            health = connector.health_check()

            assert health is True


class TestDataProcessor:
    """Test cases for DataProcessor class."""

    @pytest.fixture
    def sample_dataframe(self):
        """Create a sample DataFrame for testing."""
        return pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "name": ["Brewery A", "Brewery B", "Brewery C", "Brewery B", "Brewery D"],
            "city": ["Denver", "Boulder", "Denver", "Boulder", "Fort Collins"],
            "state": ["CO", "CO", "CO", "CO", "CO"],
            "count": [10, 20, 15, 25, 30]
        })

    def test_clean_column_names(self, sample_dataframe):
        """Test column name cleaning."""
        from streamlit_app.utils.data_processing import DataProcessor

        df = sample_dataframe.copy()
        df.columns = ["ID Number", "Brewery-Name", "City Location"]

        cleaned = DataProcessor.clean_column_names(df)

        assert all("_" not in col or col.islower() for col in cleaned.columns)

    def test_remove_duplicates(self, sample_dataframe):
        """Test duplicate removal."""
        from streamlit_app.utils.data_processing import DataProcessor

        df = sample_dataframe.copy()
        df = pd.concat([df, df.iloc[[1]]], ignore_index=True)

        assert len(df) == 6
        cleaned = DataProcessor.remove_duplicates(df, subset=["name", "city"])
        assert len(cleaned) < len(df)

    def test_filter_dataframe(self, sample_dataframe):
        """Test DataFrame filtering."""
        from streamlit_app.utils.data_processing import DataProcessor

        df = sample_dataframe.copy()
        filters = {"state": "CO", "city": ["Denver", "Boulder"]}

        filtered = DataProcessor.filter_dataframe(df, filters)

        assert filtered["state"].unique().tolist() == ["CO"]
        assert all(city in ["Denver", "Boulder"] for city in filtered["city"])

    def test_sort_dataframe(self, sample_dataframe):
        """Test DataFrame sorting."""
        from streamlit_app.utils.data_processing import DataProcessor

        df = sample_dataframe.copy()
        sorted_df = DataProcessor.sort_dataframe(df, ["count"], ascending=False)

        assert sorted_df["count"].tolist() == sorted(df["count"], reverse=True)

    def test_aggregate_data(self, sample_dataframe):
        """Test data aggregation."""
        from streamlit_app.utils.data_processing import DataProcessor

        df = sample_dataframe.copy()
        result = DataProcessor.aggregate_data(
            df,
            group_by=["city"],
            aggregations={"count": "sum", "id": "count"}
        )

        assert len(result) == 3
        assert "sum_count" in result.columns or "count" in result.columns


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
