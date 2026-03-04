"""
Data processing utilities for breweries data.

This module contains helper functions for data transformation, aggregation,
and formatting for the dashboard.

Author: Data Team
Version: 1.0.0
"""

import pandas as pd
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class DataProcessor:
    """Utility class for data processing operations."""

    @staticmethod
    def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert data types to appropriate formats.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with converted data types
        """
        try:
            # Convert numeric columns
            numeric_cols = df.select_dtypes(include=["object"]).columns
            for col in numeric_cols:
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                except Exception:
                    pass

            logger.info("Data type conversion completed")
            return df
        except Exception as e:
            logger.error(f"Error in type conversion: {str(e)}")
            return df

    @staticmethod
    def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize column names.

        Converts to lowercase and replaces spaces with underscores.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with cleaned column names
        """
        df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")
        logger.info("Column names cleaned")
        return df

    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Remove duplicate rows from DataFrame.

        Args:
            df: Input DataFrame
            subset: Optional list of columns to check for duplicates

        Returns:
            DataFrame with duplicates removed
        """
        initial_count = len(df)
        df = df.drop_duplicates(subset=subset)
        removed_count = initial_count - len(df)

        if removed_count > 0:
            logger.info(f"Removed {removed_count} duplicate rows")

        return df

    @staticmethod
    def fill_missing_values(df: pd.DataFrame, method: str = "ffill") -> pd.DataFrame:
        """
        Fill missing values in DataFrame.

        Args:
            df: Input DataFrame
            method: Fill method ("ffill" for forward fill, "bfill" for backfill, or value)

        Returns:
            DataFrame with missing values filled
        """
        if method == "ffill":
            df = df.fillna(method="ffill")
        elif method == "bfill":
            df = df.fillna(method="bfill")
        else:
            df = df.fillna(method)

        logger.info(f"Missing values filled using method: {method}")
        return df

    @staticmethod
    def get_summary_statistics(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary statistics for numeric columns.

        Args:
            df: Input DataFrame

        Returns:
            Dictionary with summary statistics
        """
        numeric_df = df.select_dtypes(include=["number"])

        summary = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "numeric_columns": numeric_df.shape[1],
            "missing_values": df.isnull().sum().to_dict(),
            "statistics": numeric_df.describe().to_dict()
        }

        return summary

    @staticmethod
    def filter_dataframe(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply multiple filters to DataFrame.

        Args:
            df: Input DataFrame
            filters: Dictionary with column names as keys and filter values

        Returns:
            Filtered DataFrame
        """
        filtered_df = df.copy()

        for column, value in filters.items():
            if column in filtered_df.columns:
                if isinstance(value, list):
                    filtered_df = filtered_df[filtered_df[column].isin(value)]
                else:
                    filtered_df = filtered_df[filtered_df[column] == value]

        logger.info(f"Applied {len(filters)} filters, reduced from {len(df)} to {len(filtered_df)} rows")
        return filtered_df

    @staticmethod
    def sort_dataframe(df: pd.DataFrame, columns: List[str], ascending: bool = True) -> pd.DataFrame:
        """
        Sort DataFrame by one or more columns.

        Args:
            df: Input DataFrame
            columns: List of column names to sort by
            ascending: Sort in ascending order (default: True)

        Returns:
            Sorted DataFrame
        """
        valid_columns = [col for col in columns if col in df.columns]

        if valid_columns:
            df = df.sort_values(by=valid_columns, ascending=ascending)
            logger.info(f"Sorted by columns: {valid_columns}")

        return df

    @staticmethod
    def aggregate_data(
        df: pd.DataFrame,
        group_by: List[str],
        aggregations: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Aggregate data by grouping and applying functions.

        Args:
            df: Input DataFrame
            group_by: Columns to group by
            aggregations: Dictionary with column names as keys and aggregation functions as values

        Returns:
            Aggregated DataFrame
        """
        valid_group_by = [col for col in group_by if col in df.columns]

        if not valid_group_by:
            logger.warning("No valid grouping columns found")
            return df

        valid_agg = {col: func for col, func in aggregations.items() if col in df.columns}

        if not valid_agg:
            logger.warning("No valid aggregation columns found")
            return df

        aggregated_df = df.groupby(valid_group_by, as_index=False).agg(valid_agg)
        logger.info(f"Data aggregated by {valid_group_by}")

        return aggregated_df

    @staticmethod
    def sample_dataframe(df: pd.DataFrame, n: int = 1000) -> pd.DataFrame:
        """
        Sample n rows from DataFrame.

        Args:
            df: Input DataFrame
            n: Number of rows to sample

        Returns:
            Sampled DataFrame
        """
        if len(df) > n:
            sampled_df = df.sample(n=n, random_state=42)
            logger.info(f"Sampled {n} rows from {len(df)} total rows")
            return sampled_df

        return df
