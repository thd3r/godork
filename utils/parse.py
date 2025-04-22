from urllib.parse import urlparse, parse_qs, unquote

def get_page_num(url):
    """
    This function handles URL parsing, extracts query parameters, gets their values and returns the value
    """

    parsed = urlparse(unquote(url))
    query_params = parse_qs(parsed.query)

    return query_params["start"][0]

def get_query(url):
    """
    This function handles URL parsing, extracts query parameters, gets their values and returns the value
    """

    query_params = parse_qs(urlparse(unquote(str(url))).query)

    try:
        query_params = parse_qs(urlparse(query_params["continue"][0]).query)
        return query_params["q"][0]
    except KeyError:
        return query_params["q"][0]

def set_page_num(num):
    """
    This is where the page data is set.
    """
    
    return int(num) // 10 + 1

def no_data(data_title):
    """
    This function checks if the desired data is not present and returns a boolean value
    """

    try:
        return len(data_title) < 1
    except:
        return False