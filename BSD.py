from requests import get
from bs4 import BeautifulSoup
import pandas as pd

BSD = []

# For every season in the series
for sn in range(1,4):
    response = get('https://www.imdb.com/title/tt5679720/episodes?season=' + str(sn))
    page_html = BeautifulSoup(response.text, 'html.parser')
    episode_containers = page_html.find_all('div', class_ = 'info')

    for episodes in episode_containers:
            # Get the info of each episode on the page
            season = sn
            episode_number = episodes.meta['content']
            title = episodes.a['title']
            airdate = episodes.find('div', class_='airdate').text.strip()
            rating = episodes.find('span', class_='ipl-rating-star__rating').text
            total_votes = episodes.find('span', class_='ipl-rating-star__total-votes').text
            desc = episodes.find('div', class_='item_description').text.strip()

            # Compiling episode info
            episode_data = [season, episode_number, title, airdate, rating, total_votes, desc]

            # Append episode info to the complete dataset
            BSD.append(episode_data)

BSD = pd.DataFrame(BSD, columns = ['season', 'episode_number', 'title', 'airdate', 'rating', 'total_votes', 'desc'])

def remove_str(votes):
    for r in ((',', ''), ('(', ''), (')', '')):
        votes = votes.replace(*r)

    return votes

BSD['total_votes'] = BSD.total_votes.apply(remove_str).astype(int)
BSD.head()

BSD['rating'] = BSD.rating.astype(float)
BSD['airdate'] = pd.to_datetime(BSD.airdate)

BSD.to_csv('BSD_IMDb.csv',index=False)
