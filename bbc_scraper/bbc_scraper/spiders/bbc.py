import scrapy
from readability import Document
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


class BbcSpider(scrapy.Spider):
    name = "bbc"
    allowed_domains = ["bbc.com"]
    start_urls = ["https://bbc.com/news"]
    data = []

    def parse(self, response):

        base_url = response.url.rstrip('/news')

        # Find links to articles on the homepage
        article_links = response.css('a.gs-c-promo-heading::attr(href)').extract()
        link_split_anchors = response.css('.nw-o-link-split__anchor::attr(href)').getall()

        # Combine links from both selectors
        all_article_links = article_links + link_split_anchors
    
        # Follow each article link and call the parse_article method
        for article_link in all_article_links:
            if article_link.startswith('/news'):
                full_article_link = response.urljoin(base_url + article_link)
                yield scrapy.Request(url=full_article_link, callback=self.parse_article)


    def parse_article(self, response):
        # Use Readability to extract the main content of the page
        doc = Document(response.text)
        content = doc.summary()

        # Extract basic article information
        date = response.css('time[data-testid="timestamp"]::attr(datetime)').get()
        title = response.css('#main-heading::text').get()
        author = response.css('meta[property="article:author"]::attr(content)').get()
        contributor = response.css('.ssrcss-68pt20-Text-TextContributorName::text').get()
        text = response.css('.e5tfeyi1 .e1jhz7w10::text').getall()
        # Convert the list of paragraphs into a single string with line breaks
        text_as_string = '\n'.join(text)

        # Add schema to the article link
        article_url = response.urljoin(response.url)

        data = {
            'title': title,
            'author': author,
            'text': text_as_string,
            'contributor': contributor,
            'date': date,
            'url': article_url,
        }
        self.data.append(data)


    def closed(self, reason):

        df = pd.DataFrame(self.data)

        # BigQuery Configuration
        project_id = 'databuilder-409318'  
        dataset_id = 'bbc_news' 
        table_id = 'articles'  
        table_path = f'{project_id}.{dataset_id}.{table_id}'
        key_path = 'D:/Projetos/Pessoal/scraper_bbc/GBQ.json'
        credentials = service_account.Credentials.from_service_account_file(key_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])

        df.to_csv("output.csv", index=False)
        # Upload DataFrame to BigQuery
        df.to_gbq(credentials=credentials, destination_table=table_path, if_exists='replace')
        