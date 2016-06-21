import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

def scrap_data(year,link,check,total_element):
    if year == 2011:
        collection = db.imdb_updated_eleven_collection
    elif year == 2012:
	collection = db.imdb_updated_twelve_collection
    elif year == 2013:
        collection = db.imdb_updated_thirteen_collection
    elif year == 2014:
        collection = db.imdb_updated_forteen_collection
    else :
        collection = db.imdb_updated_fifteen_collection
    while check:
        try:
            url = "http://www.imdb.com/search/title?sort=year&start="+str(link)+"&title_type=feature&year="+str(year)+","+str(year)
            source_code=requests.get(url)
            plain_text=source_code.text
            soup=BeautifulSoup(plain_text)
            main = soup.find("div",{"id":"main"})
            result =  main.find("table",{"class":"results"})
            container = result.find_all("tr",{"class":"odd detailed"})
            for items in container:
                total_element = total_element +1
                print "MOVIE"
                description = items.find("td",{"class":"title"})
                movie_name = description.find("a").string
                movie_year = description.find("span",{"class":"year_type"}).string
                movie_ratings = description.find("div",{"class":"user_rating"}).find("div",{"class":"rating rating-list"})["title"].split(' ')[3].split('/')[0]
                if movie_ratings == '-':
		    movie_ratings = '0'
                genres = description.find("span",{"class":"genre"}).find_all("a")
                movie_genre = []
                for genre in genres:
                    genre = str(genre.string)
                    movie_genre.append(genre)
                first_genre = movie_genre[0]
		second_genre = ''
		if len(movie_genre) > 1:
		    second_genre = movie_genre[1]
		else:
		    second_genre = 'blank'

	        print "movie_name - "+str(movie_name)
                print "movie_year - "+str(movie_year)
                print "movie_ratings - "+str(movie_ratings)
		print "Genre - "+str(movie_genre)
		collection.insert_one({'movie_name': movie_name,'movie_year': movie_year,'movie_ratings' : movie_ratings,'First_Genre': first_genre,'Second_Genre':second_genre})
                     
            container = result.find_all("tr",{"class":"even detailed"})
            for items in container:
                print "MOVIE"
		total_element = total_element
                description = items.find("td",{"class":"title"})
                movie_name = description.find("a").string
                movie_year = description.find("span",{"class":"year_type"}).string
                movie_ratings = description.find("div",{"class":"user_rating"}).find("div",{"class":"rating rating-list"})["title"].split(' ')[3].split('/')[0]
                if movie_ratings == '-':
                    movie_ratings = '0'
		genres = description.find("span",{"class":"genre"}).find_all("a")
                movie_genre = []
                for genre in genres:
                    genre = str(genre.string)
                    movie_genre.append(genre)
		first_genre = movie_genre[0]
		if len(movie_genre) > 1:
		    second_genre = movie_genre[1]
		else:
		    second_genre = 'blank'
                print "movie_name - "+str(movie_name)
		print "movie_year - "+str(movie_year)
		print "movie_ratings - "+str(movie_ratings)
                print "Genre - "+str(movie_genre)
                collection.insert_one({'movie_name': movie_name,'movie_year': movie_year,'movie_ratings' : movie_ratings,'Firsr_Genre': first_genre,'Second_Genre':second_genre})


        except:
            pass     
        try:
            fetch_link = main.find("span",{"class":"pagination"}).find_all("a")
            list = []
            for next in fetch_link:
                next = re.sub(r'[^\x00-\x7F]',' ', next.string)
                next = next.strip()
                list.append(next)
            if len(list) == 1:
                list.append("dumpy_data")
            if list[0] == "Next" or list[1] == "Next":
                link = link + 50
            else:
                check = 0    
  

        except:
            link = link +50

    return total_element

if __name__ ==  "__main__":
    link = 1
    check = 1
    total_element = 0
    years = [2011,2012,2013,2014,2015]
    client = MongoClient('localhost',27017)
    db = client.imdb_database
    for year in years:
        total_element = total_element + scrap_data(year,link,check,total_element)
    print total_element


