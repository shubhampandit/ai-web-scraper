import asyncio
from typing import List, Dict, Any
from crawl4ai import AsyncWebCrawler, RegexChunking
from crawl4ai.async_configs import CrawlerRunConfig, CacheMode
from crawl4ai.async_dispatcher import (
    MemoryAdaptiveDispatcher, 
    RateLimiter, 
    CrawlerMonitor, 
    DisplayMode
)
from llm_clients import fetch_urls_using_llm, process_content_with_gemini
from config import CONCURRENCY_LEVEL

class WebCrawler:
    def __init__(self):
        self.chunker = RegexChunking()
        
    async def _configure_dispatcher(self):
        return MemoryAdaptiveDispatcher(
            memory_threshold_percent=85.0,
            check_interval=0.5,
            max_session_permit=CONCURRENCY_LEVEL,
            rate_limiter=RateLimiter(
                base_delay=(1.0, 2.0),
                max_delay=30.0,
                max_retries=3
            ),
            monitor=CrawlerMonitor(
                max_visible_rows=10,
                display_mode=DisplayMode.AGGREGATED
            )
        )

    async def paginated_scrape(
        self,
        start_url: str,
        css_selector: str,
        data_points: List[str],
        max_pages: int
    ) -> Dict[str, Any]:
        urls = await fetch_urls_using_llm(start_url, max_pages)
        run_config = CrawlerRunConfig(
            css_selector=css_selector,
            cache_mode=CacheMode.BYPASS,
            excluded_tags=["nav", "header", "footer", "script", "style"],
            remove_overlay_elements=True
        )

        dispatcher = await self._configure_dispatcher()
        all_data = []

        async with AsyncWebCrawler() as crawler:
            results = await crawler.arun_many(
                urls=urls,
                config=run_config,
                dispatcher=dispatcher
            )

            successful_results = [
                result.markdown for result in results if result.success
            ]
            all_data = "\n\n".join(successful_results)

            chunks = self.chunker.chunk(all_data)
            processed_chunks = await asyncio.gather(*[
                process_content_with_gemini(chunk, data_points)
                for chunk in chunks
            ])

        return self._merge_results(processed_chunks)

    def _merge_results(self, processed_chunks: List[Dict]) -> Dict[str, Any]:
        merged_data = {
            "data": [
                entry for res in processed_chunks
                for entry in res.get("data", [])
            ]
        }
        return merged_data