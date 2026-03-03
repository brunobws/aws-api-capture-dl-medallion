"""
AWS Athena connector module for querying brewery data.

This module provides functionality to connect to AWS Athena and execute queries
against the breweries data warehouse.

Author: Data Team
Version: 1.0.0
"""

import logging
import boto3
import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class AthenaConnector:
    """
    Connector class for AWS Athena operations.

    Handles connection setup, query execution, and result retrieval from Athena.
    Uses AWS credentials configured in the local environment.
    """

    def __init__(
        self,
        database: str = "gold",
        s3_output_location: str = "s3://bws-dl-logs-sae1-prd/athena/query_results/",
        region: str = "sa-east-1"
    ):
        """
        Initialize Athena connector.

        Args:
            database: Athena database name (default: "gold")
            s3_output_location: S3 path for query results
            region: AWS region (default: "sa-east-1")
        """
        self.database = database
        self.s3_output_location = s3_output_location
        self.region = region
        self.client = boto3.client("athena", region_name=region)

        logger.info(f"Athena connector initialized for database: {database}")

    def execute_query(self, query: str, query_execution_context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Execute a query in Athena and return the execution ID.

        Args:
            query: SQL query to execute
            query_execution_context: Optional query context with database info

        Returns:
            Query execution ID or None if failed
        """
        if query_execution_context is None:
            query_execution_context = {"Database": self.database}

        try:
            response = self.client.start_query_execution(
                QueryString=query,
                QueryExecutionContext=query_execution_context,
                ResultConfiguration={"OutputLocation": self.s3_output_location}
            )

            execution_id = response["QueryExecutionId"]
            logger.info(f"Query executed with ID: {execution_id}")
            return execution_id

        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise

    def get_query_status(self, execution_id: str) -> Dict[str, Any]:
        """
        Get the status of a query execution.

        Args:
            execution_id: The query execution ID

        Returns:
            Dictionary with query status information
        """
        try:
            response = self.client.get_query_execution(QueryExecutionId=execution_id)
            return response["QueryExecution"]
        except Exception as e:
            logger.error(f"Error getting query status: {str(e)}")
            raise

    def get_query_results(self, execution_id: str) -> pd.DataFrame:
        """
        Retrieve query results as a pandas DataFrame.

        Args:
            execution_id: The query execution ID

        Returns:
            DataFrame with query results

        Raises:
            ValueError: If query failed or is still running
            RuntimeError: If unable to fetch results
        """
        try:
            # Get query status
            query_status = self.get_query_status(execution_id)
            status = query_status["Status"]["State"]

            if status == "FAILED":
                error_msg = query_status.get("Status", {}).get("StateChangeReason", "Unknown error")
                raise ValueError(f"Query failed: {error_msg}")

            if status == "CANCELLED":
                raise ValueError("Query was cancelled")

            if status != "SUCCEEDED":
                raise RuntimeError(f"Query is still {status}. Please wait and try again.")

            # Use Athena's built-in result pagination
            result_paginator = self.client.get_paginator("get_query_results")
            pages = result_paginator.paginate(QueryExecutionId=execution_id)

            # Parse results
            result_rows = []
            column_names = None
            header_processed = False

            for page in pages:
                rows = page["ResultSet"]["Rows"]

                # First row of first page contains column names
                if not header_processed and len(rows) > 0:
                    column_names = [col["VarCharValue"] for col in rows[0]["Data"]]
                    header_processed = True
                    rows = rows[1:]  # Skip header row

                # Process data rows
                for row in rows:
                    data = [col.get("VarCharValue", "") for col in row["Data"]]
                    result_rows.append(data)

            if not result_rows:
                logger.warning("Query returned no results")
                return pd.DataFrame()

            df = pd.DataFrame(result_rows, columns=column_names)
            logger.info(f"Retrieved {len(df)} rows from Athena")
            return df

        except Exception as e:
            logger.error(f"Error retrieving query results: {str(e)}")
            raise

    def query_to_dataframe(self, query: str) -> pd.DataFrame:
        """
        Execute a query and return results as DataFrame in one operation.

        Note: This is a convenience method that blocks until query completes.
        For long-running queries, use execute_query and get_query_results separately.

        Args:
            query: SQL query to execute

        Returns:
            DataFrame with query results
        """
        import time

        try:
            # Execute query
            execution_id = self.execute_query(query)

            # Wait for completion
            max_attempts = 300  # 5 minutes with 1-second intervals
            attempt = 0

            while attempt < max_attempts:
                status = self.get_query_status(execution_id)
                state = status["Status"]["State"]

                if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
                    break

                time.sleep(1)
                attempt += 1

            if attempt >= max_attempts:
                raise RuntimeError("Query execution timeout after 5 minutes")

            # Get results
            return self.get_query_results(execution_id)

        except Exception as e:
            logger.error(f"Error in query_to_dataframe: {str(e)}")
            raise

    def health_check(self) -> bool:
        """
        Perform a health check on the Athena connection.

        Returns:
            True if connection is healthy, False otherwise
        """
        try:
            # Try to list databases
            response = self.client.list_query_executions()
            logger.info("Athena health check passed")
            return True
        except Exception as e:
            logger.error(f"Athena health check failed: {str(e)}")
            return False
