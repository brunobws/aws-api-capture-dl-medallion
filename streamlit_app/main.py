####################################################################
# Author: Bruno William da Silva
# Date: 03/03/2026
#
# Description:
#   Main orchestrator for the Data Platform Monitoring & Analytics
#   Dashboard. Initializes the Streamlit app, manages tabs, and
#   coordinates data fetching across all modules.
#
#   Features:
#   - 📊 Gold Analytics (brewery aggregations)
#   - 📈 Logs Observability (pipeline health)
#   - 🧪 Data Quality (DQ test results)
####################################################################

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import (
    APP_NAME, APP_VERSION, APP_DESCRIPTION, APP_ICON,
    STREAMLIT_LAYOUT
)
from utils.logger import get_logger
from utils.athena_service import AthenaService

logger = get_logger(__name__)


####################################################################
# PAGE CONFIGURATION
####################################################################
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout=STREAMLIT_LAYOUT,
    initial_sidebar_state="expanded",
)


####################################################################
# CACHE & SERVICE INITIALIZATION
####################################################################
@st.cache_resource
def get_athena_service() -> AthenaService:
    """
    Initialize and cache Athena service instance.
    
    Returns:
        AthenaService: Initialized Athena service or None if health check fails
    
    Raises:
        Exception: Logs error if service initialization fails
    """
    try:
        service = AthenaService()
        if service.health_check():
            logger.info("Athena service initialized successfully")
            return service
        else:
            logger.error("Athena health check failed")
            return None
    except Exception as e:
        logger.error(f"Error initializing Athena service: {str(e)}")
        return None


####################################################################
# UI COMPONENTS
####################################################################
def render_header():
    """
    Render application header with branding and version info.
    
    Displays the app name, description, and version in a formatted header.
    """
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown(f"# {APP_ICON} {APP_NAME}")
        st.markdown(f"*{APP_DESCRIPTION}*")

    with col3:
        st.caption(f"v{APP_VERSION}")
        st.caption("Data Team 2026")


def render_sidebar():
    """
    Render sidebar with application controls and information.
    
    Includes cache controls, app description, and tab information.
    """
    with st.sidebar:
        st.header("⚙️ Controls")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh All", use_container_width=True):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.rerun()

        with col2:
            if st.button("🗑️ Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.success("Cache cleared!")

        st.divider()

        st.subheader("📋 About")
        st.info(
            "Real-time monitoring and analytics for your "
            "Medallion Data Lake, including pipeline observability "
            "and data quality metrics."
        )

        st.divider()

        st.subheader("🔗 Tabs")
        st.markdown("""
        - **📊 Gold Analytics** - Brewery data insights
        - **📈 Logs Observability** - Pipeline health
        - **🧪 Data Quality** - Test results
        """)


####################################################################
# MAIN APPLICATION
####################################################################
def main():
    """
    Main application entry point.
    
    Initializes Athena service, renders UI components, and orchestrates
    the three main dashboard tabs.
    """
    render_header()

    athena_service = get_athena_service()

    if athena_service is None:
        st.error(
            "❌ **Connection Failed**\n\n"
            "Cannot connect to AWS Athena. Please check:\n"
            "1. AWS credentials are configured\n"
            "2. Correct region is set (sa-east-1)\n"
            "3. IAM permissions allow Athena access"
        )
        st.stop()

    render_sidebar()

    tab1, tab2, tab3 = st.tabs([
        "📊 Gold – Analytics",
        "📈 Logs – Observability",
        "🧪 Data Quality"
    ])

    with tab1:
        st.header("📊 Brewery Analytics")
        from gold_analytics import render_gold_analytics
        render_gold_analytics(athena_service)

    with tab2:
        st.header("📈 Pipeline Observability")
        from logs_observability import render_logs_observability
        render_logs_observability(athena_service)

    with tab3:
        st.header("🧪 Data Quality Dashboard")
        from data_quality import render_data_quality
        render_data_quality(athena_service)


if __name__ == "__main__":
    main()

