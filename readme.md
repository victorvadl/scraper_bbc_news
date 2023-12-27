News Collection and Storage Project
===================================

Repository Structure
--------------------

-   bbc_scrapper: Contains files related to the scrapper built with the Scrapy framework.
-   bbc_api: Contains files for the Flask server that provides the API for searching articles in BigQuery.
-   bbc_request: Contains a Python script to test the API, making requests with keywords and writing the results to JSON and CSV files.


Overview
--------

This project aims to create a solution for collecting, cleaning, and storing news content from a specific website ([www.bbc.com](http://www.bbc.com/)). The solution consists of three main parts:

1.  **Scrapper (bbc_scrapper):**

    -   Utilizes the Scrapy crawling framework to extract relevant information from news articles.
    -   Cleans superfluous content, such as ads, using a framework like Readability.
    - Filters out non-news articles by only selecting those with URLs starting with '/news', excluding content related to sports or other topics.
    -   Stores the data in BigQuery, including the original article URL.
2.  **API (bbc_api):**

    -   Built with Flask, provides access to the data stored in BigQuery.
    -   Allows users to search for articles by keyword.
3.  **API Test (bbc_request):**

- A Python script that makes a request to the API. The keyword is specified in the configuration file (config.cfg), and the script writes the results to both a JSON and CSV file.


Challenge Details
-----------------

The project addresses the challenge of collecting and storing news content, prioritizing the extraction of articles relevant to the project's interest. The scrapper was developed to exclude elements related to sports or that did not have the '/news/' subroute.

The API was built to allow users to query the data stored in BigQuery based on a keyword, checking if it is present in the title or text of the articles.


Running the Project
-------------------

1.  Scrapper:

    -   Execute the scrapper following the instructions in the bbc_scrapper directory.
    -   Navigate to the `bbc_scraper` directory: `cd bbc_scraper`.
    -   Update the BigQuery configuration variables in the `bbc.py` file, located at `bbc_scraper/bbc_scraper/spiders`.

        

        ```python
        # BigQuery Configuration 
        project_id = 'your_project_id'
        dataset_id = 'your_dataset_id'
        table_id = 'your_table_id'
        table_path = f'{project_id}.{dataset_id}.{table_id}'
        key_path = 'path/to/your/GBQ.json'
        credentials = service_account.Credentials.from_service_account_file(key_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])

    -   Run the scraper: `scrapy crawl bbc`.
2.  API:

    -   Configure the BigQuery credentials and run the Flask server in the bbc_api directory.
    -   Navigate to the `bbc_api` directory: `cd bbc_api`.
    -   Update the BigQuery query in the `api.py` file if necessary:

        ```python

        # Query to retrieve data containing the keyword in the title or text
        query = f"""
        SELECT *
        FROM `your_project_id.your_dataset_id.your_table_id`
        WHERE LOWER(title) LIKE LOWER('%{keyword}%') OR LOWER(text) LIKE LOWER('%{keyword}%')
        """

    -   Run the Flask server: `python api.py`.
3.  API Test:

    -   Edit the configuration file (`config.cfg`) in the `bbc_request` directory to provide the desired keyword.
    -   Navigate to the `bbc_request` directory: `cd bbc_request`.
    -   Run the Python script to make the request to the API: `python index.py`.

Make sure to replace placeholders such as `your_project_id`, `your_dataset_id`, `your_table_id`, and the path to `GBQ.json` with your actual values. Additionally, generate a new credentials file for BigQuery and update the `key_path` accordingly. Follow these steps to ensure a successful setup and execution of the project.

Bonus
-----

The solution includes an API that provides access to the content stored in BigQuery. Users can search for articles by keyword, offering a more flexible search experience.