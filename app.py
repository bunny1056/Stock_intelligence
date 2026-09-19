import streamlit as st
import pandas as pd
import plotly.express as px

from rag_pipeline import StockResearchRAG
from financial_data import get_metrics


st.set_page_config(
    page_title="Stock Research Intelligence",
    page_icon="",
    layout="wide"
)


@st.cache_resource
def load_rag():

    return StockResearchRAG()


rag = load_rag()


st.title("Stock Research Intelligence Platform")

st.markdown(
    """
    AI powered financial research assistant for querying
    annual reports, financial statements and company filings.
    """
)


tab1, tab2 = st.tabs([
    "Research Assistant",
    "Financial Dashboard"
])


# ---------------------------------------------------------
# RAG RESEARCH ASSISTANT
# ---------------------------------------------------------

with tab1:

    st.subheader("Financial Research Assistant")

    companies = [
        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK",
        "ICICIBANK",
        "ITC",
        "HINDUNILVR",
        "MARUTI",
        "SUNPHARMA",
        "BHARTIARTL"
    ]

    selected_companies = st.multiselect(
        "Select companies",
        companies
    )

    query = st.text_area(
        "Enter your research question",
        placeholder=(
            "Compare operating margins and major risks "
            "across the selected companies."
        )
    )

    if st.button("Analyze"):

        if not query:

            st.warning("Enter a research question.")

        else:

            with st.spinner("Searching financial reports..."):

                answer = rag.generate_answer(
                    query,
                    companies=selected_companies
                    if selected_companies
                    else None
                )

            st.markdown("### Research Output")

            st.write(answer)


# ---------------------------------------------------------
# FINANCIAL DASHBOARD
# ---------------------------------------------------------

with tab2:

    st.subheader("Financial Metrics Dashboard")

    df = get_metrics()

    sectors = ["All"] + sorted(
        df["Sector"].unique().tolist()
    )

    selected_sector = st.selectbox(
        "Sector",
        sectors
    )

    if selected_sector != "All":

        filtered_df = df[
            df["Sector"] == selected_sector
        ]

    else:

        filtered_df = df


    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


    metric = st.selectbox(
        "Metric",
        [
            "Revenue Growth (%)",
            "Operating Margin (%)",
            "Net Margin (%)"
        ]
    )


    fig = px.bar(
        filtered_df,
        x="Company",
        y=metric,
        title=f"{metric} by Company"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Stock Research Intelligence | "
    "LangChain + FAISS + RAG + Streamlit"
)
