"""
File: autobyteus/tools/browser/xiaohongshu_search_ui.py

This module provides a XiaohongshuSearch tool for performing searches on Xiaohongshu using Playwright.

The XiaohongshuSearch class allows users to search Xiaohongshu and retrieve cleaned search results.
It inherits from BaseTool and UIIntegrator, providing a seamless integration with web browsers.

Classes:
    XiaohongshuSearch: A tool for performing Xiaohongshu searches and retrieving cleaned results.
"""

import asyncio
from autobyteus.tools.base_tool import BaseTool
from llm_ui_integration.ui_integrator import UIIntegrator
from autobyteus.utils.html_cleaner import clean, CleaningMode


class XiaohongshuSearch(BaseTool, UIIntegrator):
    """
    A tool that allows for performing a Xiaohongshu search using Playwright and retrieving the search results.

    This class inherits from BaseTool and UIIntegrator. Upon initialization via the UIIntegrator's
    initialize method, self.page becomes available as a Playwright page object for interaction
    with the web browser.

    Attributes:
        search_input_selector (str): The CSS selector for the Xiaohongshu search input.
        search_button_selector (str): The CSS selector for the Xiaohongshu search button.
        search_results_selector (str): The CSS selector for the Xiaohongshu search results container.
        cleaning_mode (CleaningMode): The level of cleanup to apply to the HTML content.
    """

    def __init__(self, cleaning_mode=CleaningMode.THOROUGH):
        """
        Initialize the XiaohongshuSearch tool with a specified content cleanup level.

        Args:
            cleaning_mode (CleaningMode, optional): The level of cleanup to apply to
                the HTML content. Defaults to CleaningMode.THOROUGH.
        """
        BaseTool.__init__(self)
        UIIntegrator.__init__(self)

        self.search_input_selector = '#search-input'
        self.search_button_selector = '.input-button'
        self.search_results_selector = '.feeds-container'
        self.cleaning_mode = cleaning_mode

    def tool_usage(self):
        """
        Return a string describing the usage of the XiaohongshuSearch tool.
        """
        return 'XiaohongshuSearch: Searches Xiaohongshu for information. Usage: <<<XiaohongshuSearch(query="search query")>>>, where "search query" is a string.'

    def tool_usage_xml(self):
        """
        Return an XML string describing the usage of the XiaohongshuSearch tool.
        """
        return '''XiaohongshuSearch: Searches Xiaohongshu for information. Usage:
    <command name="XiaohongshuSearch">
    <arg name="query">search query</arg>
    </command>
    where "search query" is a string.
    '''

    async def _execute(self, **kwargs):
        """
        Perform a Xiaohongshu search using Playwright and return the search results.

        This method initializes the Playwright browser, navigates to Xiaohongshu, performs the search,
        and retrieves the results. After initialization, self.page is available as a Playwright
        page object for interacting with the web browser.

        Args:
            **kwargs: Keyword arguments containing the search query. The query should be specified as 'query'.

        Returns:
            str: A string containing the cleaned HTML of the search results.

        Raises:
            ValueError: If the 'query' keyword argument is not specified.
        """
        query = kwargs.get('query')
        if not query:
            raise ValueError("The 'query' keyword argument must be specified.")

        # Call the initialize method from the UIIntegrator class to set up the Playwright browser
        await self.initialize()
        # After initialization, self.page is now available as a Playwright page object

        try:
            await self.page.goto('https://www.xiaohongshu.com/explore')

            # Find the search input element, type in the search query
            search_input = self.page.locator(self.search_input_selector)
            await search_input.fill(query)

            # Click the search button
            search_button = self.page.locator(self.search_button_selector)
            await search_button.click()

            # Wait for the search results container to be visible
            search_results_element = await self.page.wait_for_selector(self.search_results_selector, state="visible", timeout=10000)
            await asyncio.sleep(2)  # Allow time for any dynamic content to load

            # Get the content of the search results
            search_result = await search_results_element.inner_html()
            cleaned_search_result = clean(search_result, mode=self.cleaning_mode)

            return f'''Here are the Xiaohongshu search results:
                      <XiaohongshuSearchResultStart>
                            {cleaned_search_result}
                      </XiaohongshuSearchResultEnd>
                    '''
        except Exception as e:
            return f"An error occurred while searching Xiaohongshu: {str(e)}"
        finally:
            await self.close()