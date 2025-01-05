# Create a dependency container
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.rate_limiters import InMemoryRateLimiter

# from search.client import TavilySearch
# from tavily import AsyncTavilyClient


class Dependencies:
    def __init__(
        self,
        model_name: str = "claude-3-5-sonnet-20240620",
        model_timeout: int = 100,
        requests_per_second: float = 0.6,
    ):
        self.llm_client = ChatAnthropic(
            model_name=model_name,
            timeout=model_timeout,
            stop=None,
            rate_limiter=InMemoryRateLimiter(
                requests_per_second=requests_per_second,
                check_every_n_seconds=0.1,
                max_bucket_size=10,
            ),
        )
        # self.search_client = TavilySearch(client=AsyncTavilyClient())
