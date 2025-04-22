import re

from src.utils.colors import Bgcolor
from src.utils.parse import no_data
from src.helpers.console import Console
from src.utils.exceptions import GodorkNoData

from urllib.parse import urlparse, unquote
from datetime import datetime
from bs4 import BeautifulSoup

def extract_pages(html):
    """
    This function will use a pattern to extract each available page and will return the last page.
    """

    pages = re.findall(r'aria-label=\"Page ([0-9]+)\"', html)
    return pages[-1]

def extract_title(html):
    """
    This function extracts each title based on the <h3> tag and adds the title data to a list. It then returns a list containing the title content.
    """

    data_title = []
    soup = BeautifulSoup(html, "html.parser")

    for title in soup.find_all("h3"):
        if not re.search("Google Search Console|Google Search", title.getText()):
            data_title.append(title.getText().strip())
    
    return data_title

def extract_link(text):
    """
    This function extracts all available links from the search results by applying various patterns to assist in the extraction. 
    It also checks if a domain is part of the excluded domains list. The function returns a list of links.
    """

    data_links = []
    exclude_domains = re.findall(r'https?://([a-zA-Z0-9\-.]+\.google\.com)', text)

    pattern = re.compile(
        r'\"><a href=\"\/url\?q=(.*?)&amp|href=\"/url\?q=(.*?)&amp;sa=U&amp;ved=|&amp;url=(.*?)&amp;ved='
    )

    links = pattern.findall(text)
    if links:
        for link in links:
            link = "".join(list(dict.fromkeys(link)))
            if link.startswith(('http', 'https')) and urlparse(link).netloc not in exclude_domains:
                data_links.append(unquote(link))
    
    return data_links

def extract_data(html, reports, metadata):
    """
    This function combines title and link extraction to process the data. If both the title and link are valid, they will be printed. 
    Additionally, the function generates a report if valid data is found.
    """

    query = metadata.get("query")
    num_page = metadata.get("num_page")

    data_title = extract_title(html)
    data_links = extract_link(html)

    if no_data(data_title) == True:
        raise GodorkNoData(f"No data can be collected on page {num_page}")
        
    if len(data_title) > 0 and len(data_links) > 0:
        reports.logs_report("info", data=f"Found {len(data_title)} title and {len(data_links)} links on page {num_page}")
        Console().log_print("info", msg=f"Found {len(data_title)} title and {len(data_links)} links on page {num_page}")

        reports.json_report({
            "timestamp": str(datetime.now()),
            "query": query,
            "page": num_page,
            "size_page": len(html),
            "data_output": {
                "title": data_title,
                "links": data_links
            },
        })

        for i, title in enumerate(data_title):
            try:
                print(f"{title} [{Bgcolor.GREEN}{data_links[i]}{Bgcolor.DEFAULT}]")
            except IndexError:
                pass