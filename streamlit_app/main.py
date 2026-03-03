"""
Breweries Dashboard - Main Streamlit Application.

This is the main entry point for the Breweries Dashboard application.
It provides an interactive interface for querying and visualizing brewery data
from AWS Athena.

Author: Data Team
Version: 1.0.0
"""

import streamlit as st
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from config import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    STREAMLIT_LAYOUT,
    ENABLE_CACHE,
    CACHE_TTL,
    LOG_LEVEL,
    LOG_FORMAT,
    COLUMN_DISPLAY_NAMES,
    SAMPLE_QUERIES,
    DEFAULT_ROWS_TO_DISPLAY,
)
from utils.athena_connector import AthenaConnector
from utils.data_processing import DataProcessor


# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🍺",
    layout=STREAMLIT_LAYOUT,
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_athena_connector():
    """Get or create Athena connector instance (cached)."""
    try:
        connector = AthenaConnector()
        if connector.health_check():
            logger.info("Athena connector initialized successfully")
            return connector
        else:
            st.error("Failed to connect to AWS Athena. Please check your AWS credentials.")
            return None
    except Exception as e:
        logger.error(f"Error initializing Athena connector: {str(e)}")
        st.error(f"Connection Error: {str(e)}")
        return None


def render_header():
    """Render application header."""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.title(f"🍺 {APP_NAME}")
        st.caption(APP_DESCRIPTION)

    with col2:
        st.caption(f"v{APP_VERSION}")


def render_sidebar():
    """Render sidebar with controls and information."""
    with st.sidebar:
        st.header("Dashboard Controls")

        st.subheader("Quick Actions")
        col1, col2 = st.columns(2)

        with col1:
            refresh_button = st.button("🔄 Refresh", use_container_width=True)

        with col2:
            clear_cache = st.button("🗑️ Clear Cache", use_container_width=True)

        if clear_cache:
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("Cache cleared!")

        st.divider()

        # Sample queries section
        st.subheader("Sample Queries")
        selected_sample = st.selectbox(
            "Select a sample query:",
            options=list(SAMPLE_QUERIES.keys()),
            key="sample_query_select"
        )

        st.divider()

        # Settings
        st.subheader("Settings")
        rows_to_display = st.slider(
            "Rows to display:",
            min_value=100,
            max_value=5000,
            value=DEFAULT_ROWS_TO_DISPLAY,
            step=100,
            key="rows_slider"
        )

        st.divider()

        # Help and Information
        st.subheader("ℹ️ Information")
        st.info(
            "**How to use this dashboard:**\n\n"
            "1. Enter your SQL query in the main area\n"
            "2. Click 'Run Query' to execute\n"
            "3. View results and statistics\n"
            "4. Export data using the download button"
        )

        st.divider()

        # Footer
        st.caption("Powered by Streamlit & AWS Athena")


def render_query_section(connector, sample_query):
    """Render query input and execution section."""
    st.subheader("Query Editor")

    # Use sample query if selected
    query_placeholder = sample_query if sample_query else "SELECT * FROM gold.tb_ft_breweries_agg LIMIT 1000"

    query = st.text_area(
        "Enter your SQL query:",
        value=query_placeholder,
        height=150,
        key="query_input"
    )

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        run_query = st.button("▶️ Run Query", type="primary", use_container_width=True)

    with col2:
        clear_query = st.button("🗑️ Clear", use_container_width=True)

    if clear_query:
        st.rerun()

    return run_query, query


def render_results_section(df):
    """Render results display section."""
    if df is None or df.empty:
        st.warning("No results to display")
        return

    st.subheader("Results")

    # Display statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Rows", len(df))

    with col2:
        st.metric("Total Columns", len(df.columns))

    with col3:
        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    with col4:
        st.metric("Data Types", f"{len(df.select_dtypes(include=['number']).columns)} Numeric")

    st.divider()

    # Display data table
    st.dataframe(
        df,
        use_container_width=True,
        height=400,
    )

    st.divider()

    # Export options
    col1, col2, col3 = st.columns(3)

    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="breweries_data.csv",
            mime="text/csv",
        )

    with col2:
        json = df.to_json(orient="records")
        st.download_button(
            label="📥 Download JSON",
            data=json,
            file_name="breweries_data.json",
            mime="application/json",
        )

    with col3:
        parquet = df.to_parquet()
        st.download_button(
            label="📥 Download Parquet",
            data=parquet,
            file_name="breweries_data.parquet",
            mime="application/octet-stream",
        )


def render_statistics_section(df):
    """Render data statistics section."""
    st.subheader("📊 Data Statistics")

    # Numeric columns statistics
    numeric_df = df.select_dtypes(include=["number"])

    if not numeric_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Numeric Summary**")
            st.dataframe(numeric_df.describe())

        with col2:
            st.write("**Missing Values**")
            missing_data = df.isnull().sum()
            missing_data = missing_data[missing_data > 0]

            if missing_data.empty:
                st.success("No missing values found!")
            else:
                st.dataframe(missing_data)

    # Categories analysis
    categorical_df = df.select_dtypes(include=["object"])

    if not categorical_df.empty:
        st.write("**Categorical Columns Unique Values**")

        col1, col2 = st.columns(2)

        for idx, col in enumerate(categorical_df.columns):
            if idx % 2 == 0:
                with col1:
                    st.write(f"**{col}**")
                    st.write(f"Unique values: {categorical_df[col].nunique()}")
            else:
                with col2:
                    st.write(f"**{col}**")
                    st.write(f"Unique values: {categorical_df[col].nunique()}")


def main():
    """Main application entry point."""
    # Render header
    render_header()

    # Get Athena connector
    connector = get_athena_connector()

    if connector is None:
        st.error("Cannot proceed without Athena connection")
        st.stop()

    # Render sidebar
    sample_query = render_sidebar()

    if st.session_state.get("sample_query_select"):
        sample_query = SAMPLE_QUERIES.get(st.session_state.sample_query_select)

    # Main content area
    run_query, query = render_query_section(connector, sample_query)

    if run_query and query.strip():
        try:
            with st.spinner("Executing query..."):
                logger.info(f"Executing query: {query[:100]}...")
                df = connector.query_to_dataframe(query)

                # Store results in session state for later use
                st.session_state.query_results = df

                st.success("Query executed successfully!")

        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            st.error(f"Query Error: {str(e)}")

    # Display results if available
    if "query_results" in st.session_state:
        df = st.session_state.query_results

        render_results_section(df)

        # Additional statistics tab
        if len(df) > 0:
            st.divider()
            render_statistics_section(df)


if __name__ == "__main__":
    main()
