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
#   - Analytics (brewery aggregations)
#   - Observability (pipeline health)
#   - Data Quality (test results)
####################################################################

########### imports ################
import streamlit as st
import sys
from pathlib import Path
###################################

sys.path.insert(0, str(Path(__file__).parent))

from config import APP_NAME, APP_VERSION, APP_DESCRIPTION, STREAMLIT_LAYOUT
from utils.logger import get_logger
from utils.athena_service import AthenaService
from theme import (
    COLOR_DARK_GRAY, COLOR_LIGHT_GRAY, COLOR_ORANGE, COLOR_WHITE,
    COLOR_TEXT, COLOR_BORDER
)

logger = get_logger(__name__)


####################################################################
# PAGE CONFIGURATION
####################################################################
st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout=STREAMLIT_LAYOUT,
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    body {
        background-color: #FAFAFA;
    }
    .stApp {
        background-color: #FAFAFA;
    }
</style>
""", unsafe_allow_html=True)


####################################################################
# SERVICE INITIALIZATION
####################################################################
@st.cache_resource
def get_athena_service() -> AthenaService:
    """
    Initialize and cache Athena service instance.
    
    Returns:
        AthenaService: Initialized Athena service or None if health check fails
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
    Render ultra-compact professional header (SaaS style).
    """
    st.markdown(f"""
    <div style="padding: 8px 0 10px 0; margin-bottom: 12px; border-bottom: 1px solid {COLOR_BORDER};">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <h3 style="margin: 0; font-size: 18px; color: {COLOR_DARK_GRAY}; font-weight: 600;">Data Platform Monitoring</h3>
                <p style="margin: 0; font-size: 11px; color: {COLOR_LIGHT_GRAY}; letter-spacing: 0.5px;">Medallion Architecture Analytics</p>
            </div>
            <div style="text-align: right; white-space: nowrap;">
                <p style="margin: 0 0 6px 0; font-size: 12px; color: {COLOR_DARK_GRAY}; font-weight: 500;">Bruno William da Silva</p>
                <div style="font-size: 12px;">
                    <a href="https://github.com/brunobws/aws-api-capture-dl-medallion" target="_blank" style="color: {COLOR_ORANGE}; text-decoration: none; font-weight: 600;">GitHub</a> &nbsp;|&nbsp;
                    <a href="https://www.linkedin.com/in/brunowsilva/" target="_blank" style="color: {COLOR_ORANGE}; text-decoration: none; font-weight: 600;">LinkedIn</a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """
    Render sidebar with application controls and information.
    """
    with st.sidebar:
        st.header("Controls")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Refresh Data", use_container_width=True):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.rerun()

        with col2:
            if st.button("Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.success("Cache cleared!")

        st.divider()

        st.subheader("About")
        st.info(
            "Real-time monitoring and analytics platform for "
            "Medallion Data Lake architecture. Monitor pipeline health, "
            "analyze aggregated data, and track data quality metrics."
        )

        st.divider()

        st.subheader("Navigation")
        st.markdown("""
        **Analytics**  
        Brewery data insights and aggregations

        **Observability**  
        Pipeline health and execution monitoring

        **Data Quality**  
        Test results and data validation metrics
        """)


def render_footer():
    """
    Render professional footer.
    """
    st.markdown(f"""
    <div style="border-top: 1px solid {COLOR_BORDER}; padding: 20px 0; margin-top: 40px; text-align: center; color: {COLOR_LIGHT_GRAY}; font-size: 12px;">
        <p style="margin-bottom: 5px;">Project: AWS API Capture Data Lake — Medallion Architecture</p>
        <p>Developed by Bruno William da Silva</p>
    </div>
    """, unsafe_allow_html=True)


####################################################################
# MAIN APPLICATION
####################################################################
def main():
    """
    Main application entry point and tab orchestrator.
    """
    render_header()

    athena_service = get_athena_service()

    if athena_service is None:
        st.error(
            "Connection Error: Cannot connect to AWS Athena.\n\n"
            "Please verify:\n"
            "1. AWS credentials are configured\n"
            "2. Correct region is set (sa-east-1)\n"
            "3. IAM permissions allow Athena access"
        )
        st.stop()

    render_sidebar()

    tab1, tab2, tab3 = st.tabs(["Analytics", "Observability", "Data Quality"])

    with tab1:
        from gold_analytics import render_gold_analytics
        render_gold_analytics(athena_service)

    with tab2:
        from logs_observability import render_logs_observability
        render_logs_observability(athena_service)

    with tab3:
        from data_quality import render_data_quality
        render_data_quality(athena_service)

    render_footer()


if __name__ == "__main__":
    main()

