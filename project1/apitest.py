import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "qXpPQv2DwijzCIgVO2BQ", "isbns": "9781632168146"}).json()
grrating=res['books'][0]['average_rating']
grcount=res['books'][0]['work_ratings_count']
print(grrating)
print(grcount)
