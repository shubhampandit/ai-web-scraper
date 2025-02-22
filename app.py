import asyncio
import streamlit as st
import pandas as pd
import json
from web_crawler import WebCrawler
from config import DEFAULT_CSS_SELECTOR

def main():
    st.title("Automated Web Data Extractor")
    
    # UI Components
    url = st.text_input("Enter URL:")
    max_pages = st.number_input("Max Pages:", min_value=1, value=1)
    css_selector = st.text_input("Enter CSS Selector (optional):", DEFAULT_CSS_SELECTOR)
    data_points = st.text_input("Data points (comma-separated):")
    
    # Data processing
    data_points_list = [dp.strip() for dp in data_points.split(",") if dp.strip()]
    
    if st.button("Extract Data"):
        if not url or not data_points_list:
            st.warning("Please provide a URL and data points.")
            return
            
        with st.spinner("Extracting data..."):
            crawler = WebCrawler()
            # loop = asyncio.ProactorEventLoop()
            # asyncio.set_event_loop(loop)
            # results = loop.run_until_complete(
            #     crawler.paginated_scrape(
            #         start_url=url,
            #         css_selector=css_selector,
            #         data_points=data_points_list,
            #         max_pages=max_pages
            #     )
            # )
            results = asyncio.run(
                crawler.paginated_scrape(
                    start_url=url,
                    css_selector=css_selector,
                    data_points=data_points_list,
                    max_pages=max_pages
                )
            )
            
            _display_results(results)

    with st.expander("Advanced Settings"):
        st.checkbox("Process iframes", value=True)
        st.checkbox("Remove overlay elements", value=True)

def _display_results(results):
    if not results.get("data"):
        st.warning("No data found")
        return
    
    df = pd.DataFrame(results["data"])
    st.dataframe(df, use_container_width=True)
    
    # Export buttons
    csv = df.to_csv(index=False).encode("utf-8")
    json_data = json.dumps(results, indent=2)
    
    st.download_button(
        "Download CSV",
        csv,
        "extracted_data.csv",
        "text/csv"
    )
    st.download_button(
        "Download JSON",
        json_data,
        "extracted_data.json",
        "application/json"
    )

if __name__ == "__main__":
    main()