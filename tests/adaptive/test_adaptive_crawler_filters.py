import pytest

from crawl4ai.adaptive_crawler import AdaptiveCrawler, AdaptiveConfig
from crawl4ai.models import CrawlResult


class FakeAdaptiveCrawler(AdaptiveCrawler):
    async def _crawl_with_preview(self, url: str, query: str) -> CrawlResult:
        return CrawlResult(
            url=url,
            html="",
            success=True,
            links={
                "internal": [{"href": "https://example.com/internal"}],
                "external": [{"href": "https://external.example.net/"}],
            },
        )

    async def _crawl_batch(self, links_with_scores, query: str):
        return []


@pytest.mark.asyncio
async def test_adaptive_digest_filters_external_links():
    crawler = FakeAdaptiveCrawler(
        crawler=None,
        config=AdaptiveConfig(max_depth=1, max_pages=1),
    )

    state = await crawler.digest(
        start_url="https://example.com",
        query="test query",
    )

    hrefs = [link.href for link in state.pending_links]
    assert "https://example.com/internal" in hrefs
    assert "https://external.example.net/" not in hrefs
