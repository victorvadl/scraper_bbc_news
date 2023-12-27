from flask import Flask, request, jsonify
from google.cloud import bigquery
from google.oauth2 import service_account


app = Flask(__name__)

# BigQuery credentials configuration
key_path = 'D:/Projetos/Pessoal/scraper_bbc/GBQ.json'
credentials = service_account.Credentials.from_service_account_file(key_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])

# Creates BigQuery client with credentials
client = bigquery.Client(credentials=credentials)

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')

    # Query to retrieve data containing the keyword in the title or text
    query = f"""
    SELECT *
    FROM `databuilder-409318.bbc_news.articles`
    WHERE LOWER(title) LIKE LOWER('%{keyword}%') OR LOWER(text) LIKE LOWER('%{keyword}%')
    """

    # Executes the query
    query_job = client.query(query)

    # Gets query results
    results = query_job.result()

    # Converts results to a format that can be returned as JSON
    data = []
    for row in results:
        data.append({
            'title': row['title'],
            'author': row['author'],
            'text': row['text'],
            'contributor': row['contributor'],
            'date': row['date'],
            'url': row['url'],
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
