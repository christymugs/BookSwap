import json
import requests
import datetime
import time
from dateutil.relativedelta import relativedelta

NYT_URL = 'https://api.nytimes.com/svc/books/v3/lists.json'
API_KEY = '73JJTrck6XGqrqSA2iYYyZGIFscNHdOG' 
dupe_list = []
reduced_data = []
count = 0
p_date = datetime.date(2024, 12, 2)

try:
    while count < 120: #last 7 years
        
        print(p_date)
        params = {'api-key': API_KEY,
                'list': 'hardcover-nonfiction', 
                'published-date': p_date}
        
        #other lists: hardcover-fiction

        r = requests.get(url= NYT_URL, params=params)
        r.raise_for_status()
        data = r.json()

        books_data = data['results']
        count += 1
        new_date = p_date + relativedelta(months=-1)
        p_date = new_date

        for book in books_data:


            book_details = book['book_details'][0]
            isbn = book_details['primary_isbn13']
            if (isbn not in dupe_list):
                dupe_list.append(isbn)
                reviews = book['reviews'][0]
                review_link = ""
                if len(reviews['book_review_link']) != 0:
                    review_link = reviews['book_review_link']
                elif len(reviews['sunday_review_link']) != 0:
                    review_link = reviews['book_review_link']
                    
                reduced_data.append(
                    {
                        "isbn13" : isbn,
                        "title" : book_details['title'],
                        "author" : book_details['author'],
                        "description" : book_details['description'],
                        "review_link" : review_link,
                        "amazon_link" : book['amazon_product_url']
                    }
                )
        
        time.sleep(13) #limit of 500 recs per day with 5 per minute. this ensures we won't hit the limit
except requests.exceptions.RequestException as e:
    print(e)
    print(reduced_data)
finally:
    with open("books_reduced.json", "w", encoding='utf-8') as outfile:
        json.dump(reduced_data, outfile)
        outfile.close()