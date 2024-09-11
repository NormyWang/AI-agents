import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from tools.xiaohongshu_search import XiaohongshuSearch

@pytest.mark.asyncio
async def test_xiaohongshu_search():
    search_query = "柏林旅游"  # "Berlin travel" in Chinese
    xiaohongshu_search = XiaohongshuSearch()
    print(xiaohongshu_search.tool_usage())
    search_results = await xiaohongshu_search.execute(query=search_query)
    
    # Save the page content to a file
    file_name = "xiaohongshu_berlin_travel.html"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(search_results)
