####################################################################
# Author: Bruno William da Silva
# Date: 03/03/2026
#
# Description:
#   Gold Analytics tab module for brewery data insights.
#   Displays aggregated brewery data by country, state, and type
#   with cascading filters and responsive visualizations.
#
#   Features:
#   - Cascading multiselect filters
#   - KPI metrics (totals, counts)
#   - Bar charts (breweries by type, top states)
#   - Detailed sortable data table
#   - Export functionality (CSV, JSON)
####################################################################

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.logger import get_logger
from utils.athena_service import AthenaService
from utils.cache_manager import cached_query
from config import (
    ATHENA_DATABASE, GOLD_TABLE, CHART_HEIGHT,
    CHART_COLOR_PRIMARY, CHART_COLOR_SUCCESS
)

logger = get_logger(__name__)


@cached_query(ttl_seconds=300)
def fetch_gold_data(athena_service: AthenaService) -> pd.DataFrame:
    """
    Fetch complete brewery aggregation dataset from gold table.
    
    Returns:
        DataFrame with all brewery data (nm_country, nm_state, ds_brewery_type, nr_total_breweries)
    """
    query = f"""
    SELECT
        nm_country,
        nm_state,
        ds_brewery_type,
        nr_total_breweries
    FROM "{ATHENA_DATABASE}"."{GOLD_TABLE}"
    WHERE nm_country IS NOT NULL
    ORDER BY nm_country, nm_state, ds_brewery_type
    """
    try:
        logger.info("Fetching complete gold dataset")
        return athena_service.query_gold(query)
    except Exception as e:
        logger.error(f"Error fetching gold data: {str(e)}")
        st.error(f"Failed to fetch data: {str(e)}")
        return pd.DataFrame()


def render_gold_analytics(athena_service: AthenaService):
    """
    Render the Gold Analytics tab with cascading filters and responsive charts.
    
    Flow:
    1. Fetch complete dataset once
    2. Apply cascading filters (Country → State → Type)
    3. Generate all analytics from filtered data
    4. Display charts, KPIs, and table
    """

    ####################################################################
    # LOAD FULL DATASET
    ####################################################################
    with st.spinner("Loading brewery data..."):
        df = fetch_gold_data(athena_service)

    if df.empty:
        st.warning("No data available")
        return

    # Convert to proper types
    df["nr_total_breweries"] = pd.to_numeric(df["nr_total_breweries"], errors="coerce")

    st.subheader("🔍 Filters")

    col1, col2, col3 = st.columns(3)

    ####################################################################
    # CASCADING FILTER 1: COUNTRY
    ####################################################################
    with col1:
        all_countries = sorted(df["nm_country"].unique())
        selected_countries = st.multiselect(
            "Country",
            options=all_countries,
            default=all_countries,
            key="gold_countries"
        )

    ####################################################################
    # CASCADING FILTER 2: STATE
    ####################################################################
    with col2:
        # Filter states based on selected countries
        available_states = sorted(
            df[df["nm_country"].isin(selected_countries)]["nm_state"].unique()
        )
        selected_states = st.multiselect(
            "State",
            options=available_states,
            default=available_states,
            key="gold_states"
        )

    ####################################################################
    # CASCADING FILTER 3: BREWERY TYPE
    ####################################################################
    with col3:
        # Filter types based on selected countries and states
        available_types = sorted(
            df[
                (df["nm_country"].isin(selected_countries)) &
                (df["nm_state"].isin(selected_states))
            ]["ds_brewery_type"].unique()
        )
        selected_types = st.multiselect(
            "Brewery Type",
            options=available_types,
            default=available_types,
            key="gold_types"
        )

    ####################################################################
    # APPLY ALL FILTERS
    ####################################################################
    filtered_df = df[
        (df["nm_country"].isin(selected_countries)) &
        (df["nm_state"].isin(selected_states)) &
        (df["ds_brewery_type"].isin(selected_types))
    ].copy()

    st.divider()

    ####################################################################
    # KPIs
    ####################################################################
    st.subheader("📊 Key Performance Indicators")

    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    # Calculate KPIs from filtered data
    total_breweries = filtered_df["nr_total_breweries"].sum()
    total_countries = filtered_df["nm_country"].nunique()
    total_states = filtered_df["nm_state"].nunique()
    total_types = filtered_df["ds_brewery_type"].nunique()

    with kpi_col1:
        st.metric("Total Breweries", f"{int(total_breweries):,}")

    with kpi_col2:
        st.metric("Countries", total_countries)

    with kpi_col3:
        st.metric("States", total_states)

    with kpi_col4:
        st.metric("Brewery Types", total_types)

    st.divider()

    ####################################################################
    # CHARTS
    ####################################################################
    col1, col2 = st.columns(2)

    # Chart 1: Breweries by Type (from filtered data)
    with col1:
        st.subheader("Breweries by Type")

        type_agg = (
            filtered_df.groupby("ds_brewery_type", as_index=False)
            ["nr_total_breweries"].sum()
            .sort_values("nr_total_breweries", ascending=False)
        )

        if not type_agg.empty:
            fig = px.bar(
                type_agg,
                x="ds_brewery_type",
                y="nr_total_breweries",
                title="Total Breweries by Type",
                labels={"ds_brewery_type": "Type", "nr_total_breweries": "Count"},
                color_discrete_sequence=[CHART_COLOR_PRIMARY],
                height=CHART_HEIGHT
            )
            fig.update_layout(xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No data for selected filters")

    # Chart 2: Top 10 States (from filtered data)
    with col2:
        st.subheader("Top 10 States by Breweries")

        state_agg = (
            filtered_df.groupby("nm_state", as_index=False)
            ["nr_total_breweries"].sum()
            .sort_values("nr_total_breweries", ascending=False)
            .head(10)
        )

        if not state_agg.empty:
            state_agg_sorted = state_agg.sort_values("nr_total_breweries", ascending=True)
            fig = px.bar(
                state_agg_sorted,
                y="nm_state",
                x="nr_total_breweries",
                title="Top 10 States by Total Breweries",
                labels={"nm_state": "State", "nr_total_breweries": "Count"},
                color_discrete_sequence=[CHART_COLOR_SUCCESS],
                height=CHART_HEIGHT,
                orientation="h"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No data for selected filters")

    st.divider()

    ####################################################################
    # DETAILED DATA TABLE
    ####################################################################
    st.subheader("📋 Detailed Data")

    display_df = filtered_df[
        ["nm_country", "nm_state", "ds_brewery_type", "nr_total_breweries"]
    ].copy()
    display_df.columns = ["Country", "State", "Brewery Type", "Total Breweries"]
    display_df = display_df.sort_values("Total Breweries", ascending=False)

    st.dataframe(
        display_df,
        width='stretch',
        height=400,
    )

    ####################################################################
    # EXPORT
    ####################################################################
    col1, col2, col3 = st.columns(3)

    with col1:
        csv_data = display_df.to_csv(index=False)
        st.download_button(
            label="📥 CSV",
            data=csv_data,
            file_name="gold_breweries.csv",
            mime="text/csv",
        )

    with col2:
        json_data = display_df.to_json(orient="records")
        st.download_button(
            label="📥 JSON",
            data=json_data,
            file_name="gold_breweries.json",
            mime="application/json",
        )

    with col3:
        parquet_data = display_df.to_parquet()
        st.download_button(
            label="📥 Parquet",
            data=parquet_data,
            file_name="gold_breweries.parquet",
            mime="application/octet-stream",
        )
