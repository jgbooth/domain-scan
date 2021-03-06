import logging
import requests

###
# Very simple scanner that follows redirects for a number of pages
# per domain to see if there is a 200 at the end or not.


# Set a default number of workers for a particular scan type.
# Overridden by a --workers flag. XXX not actually overridden?
workers = 50


# This is the list of pages that we will be checking.
pages = [
    "/",
    "/code.json",
    "/coronavirus",
    "/data.json",
    "/data",
    "/developer",
    "/digitalstrategy",
    "/open",
    "/privacy",
    "/robots.txt",
    "/sitemap.xml",
    "/cj",
    "/digitalstrategy/datacenteroptimizationstrategicplan.json",
    "/digitalstrategy/FITARAmilestones.json",
    "/digitalstrategy/governanceboards.json",
    "/digitalstrategy/costsavings.json",
    "/digitalstrategy/bureaudirectory.json",
    "/redirecttest-foo-bar-baz",
]


# Optional one-time initialization for all scans.
# If defined, any data returned will be passed to every scan instance and used
# to update the environment dict for that instance
# Will halt scan execution if it returns False or raises an exception.
#
# Run locally.
def init(environment: dict, options: dict) -> dict:
    logging.debug("Init function.")
    return {'pages': pages}


# Required scan function. This is the meat of the scanner, where things
# that use the network or are otherwise expensive would go.
#
# Runs locally or in the cloud (Lambda).
def scan(domain: str, environment: dict, options: dict) -> dict:
    logging.debug("Scan function called with options: %s" % options)

    results = {}

    # Perform the "task".
    for page in environment['pages']:
        results[page] = {}
        try:
            response = requests.head("https://" + domain + page, allow_redirects=True, timeout=4)
            results[page] = str(response.status_code)
        except Exception:
            logging.debug("could not get data from %s%s", domain, page)
            results[page] = str(-1)

    logging.warning("200 %s Complete!", domain)

    return results


# Required CSV row conversion function. Usually one row, can be more.
#
# Run locally.
def to_rows(data):
    row = []
    for page in headers:
        row.extend([data[page]])
    return [row]


# CSV headers for each row of data. Referenced locally.
headers = pages
