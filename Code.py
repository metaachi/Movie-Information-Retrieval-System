import json
import requests
from bs4 import BeautifulSoup

# Scraping data using requests from html session
from requests_html import HTMLSession
def MakeData():
    tr= []
    print("Scraping website...")
    for i in range(5):
        url = "https://www.metacritic.com/browse/movies/score/metascore/all/filtered?sort=desc&page="+str(i)
        session = HTMLSession() #session object
        r = session.get(url) #fecthing html
        soup = BeautifulSoup(r.content, "html.parser") #converting to soup object using beautifulSoup
        # print(soup)
        tr.extend(soup.find_all("tr",class_="")) #The data is in the tr tags inside the html elements of the site
    print("scraping complete")
    return tr

tr = MakeData()

# Helper functions ---

# For extracting the text inside a html tag
def extract(item):
    if item != None:
        return item.text
    return ""

# For getting and scraping the data from the a tag where the director and genre details are stored
def getdata(link):
    # Adding the main domain path and the route for the specific movie 
    link = "https://www.metacritic.com/"+link
    session = HTMLSession()
    r = session.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    # Creating session object and scraping data using beautifulsoup
    # Fetching director data
    director = soup.find("div",class_="director").find("a",class_="").text
    # Fetching genre data
    genre = soup.find("div",class_="genres").find("span",class_="").text.strip("\n")
    # Returning the obtained data
    return (director,genre)

movies = []
# Making empty movies list
# Count = 0
# Keys for generating the dictionary and values so that it can be easily converted to a dataframe or can be saved to a csv file
keys = ["Number","Movie","Genre","Date","UserScore","MetaScore","CertRating","Director"]
# c=0
# Running loop for items in tr and fetching all details of movie on each loop
for i in tr:
    # Movie name is under h3 tag so we extract from it
    movie = extract(i.find("h3"))
    # Metascore is stored in a class named metascore_w large movie positive perfect
    metascore = extract(i.find("div",class_="metascore_w large movie positive perfect"))
    if metascore == '':
        metascore = extract(i.find("div",class_="metascore_w large movie positive"))
    # Serial number
    no = extract(i.find("span",class_="title")).strip("\n").strip(" ").strip("\n")
    # Cert rating
    cert_rating = extract( i.find("span",class_="cert_rating")).split("|") 
    # Forming list of the values split and getting data
    if len(cert_rating)>1:
        cert_rating = cert_rating[1].strip()
    else:
        cert_rating = cert_rating[0]
    # For getting the date of the movie
    date = extract(i.find("div",class_="clamp-details").find("span",class_=""))
    userscore = extract(i.find("div",class_="metascore_w user large movie positive"))
    extra = i.find("td",class_="clamp-image-wrap")
#     Using getdata and obtaining data from another link inside 'a' tag
    director,genre = getdata(extra.find("a")['href'])
    # Making a list of values
    values = [no,movie,genre,date,userscore,metascore,cert_rating,director]
#     print("end")
    # print(values)
    # Adding the keys and values , making a dictionary and adding it to the movies list
    movies.append(dict(zip(keys,values)))

import csv # For making csv
# Defining header names
field_names= ["Number","Movie","Genre","Date","UserScore","MetaScore","CertRating","Director"]
with open('Reviews.csv', 'w') as csvfile:
    # Creating a dictwroter object
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    # Now writing the rows of movies to csv file based on keys of dictionary as column/header of csv file
    writer.writerows(movies)

import pandas as pd
# Now converting the list of dicts into a dataframe for easy processing of data

# Helper function to find the movie details by its name
def findByMovie(name):
    name = name.lower()
    for i in movies:
        if i["Movie"].lower() == name:
            return i
    return None 

# Forming counts of the genres using a dictionary 
def mdg(list):
    d ={}
    for i in list:
        k = i.split(",")
        for j in k:
            p = j.strip()
            if p in d.keys():
                d[p]+=1
            else:
                d[p]=1
    return d

# Finding by director name and getting his details by using getdata function and movies he directed for
def getdata(name,df):
    # Finding rows that matches the director name without considering case of name of director for comparison
    data = df[df["Director"].str.strip(" ").str.contains(name.strip(),case=False,na=False)]
#     print(data)
    movies = list(data['Movie'])
    genres = mdg(list(data['Genre']))
    st = []
    for i,j in genres.items():
        st.append(f"{i.strip()}:{j}")
    return (movies,st,genres)
    
# For calculating cosine score between two vectors....here vectors of counts of genres for two directors
def cosine(d1,d2):
    denom1 = 0
    for i,j in d1.items():
        if i not in d2.keys():
            d2[i] = 0
        denom1+=j*j
    denom1 = denom1**0.5
    denom2=0
    for i,j in d2.items():
        if i not in d1.keys():
            d1[i] = 0
        denom2+=j*j
    denom1 = denom1**0.5
    sum = 0
    den = (denom1*denom2)
    for i in d1.keys():
        sum+=d1[i]*d2[i]
    return sum/den
    
# Main function to run the main loop of menu which displays options for user to select by
# Find by movie
# Find by director and find cosine score

def main(movies):
    # Converting the movies list obtained above from scraping to a dataframe
    df = pd.DataFrame.from_dict(movies)
    # Running main menu loop
    while True:
        print("What do you want to check on Metacritic? (Please choose 'movie', 'director', or 'comparison'..'stop' to exit) ")
        choice = input("input: ")
        if choice.lower() =="movie":
            name = input("What movie do you want to check? \ninput: ")
            data = df[df['Movie'].str.strip(" ").str.contains(name.strip(),case=False,na=False)]
            print(len(data))
            # If no results found printout that no movies found
            if len(data)<1:
                print("No movie found with the input")
                continue
            elif len(data)>1:
                data = data[0]
            movie = list(data['Movie'])[0]
            genre = list(data['Genre'])[0]
            # Printing search result details by movie search
            print(f"The director of the movie is {movie}\nThe genre of the movie is {genre}")
        elif choice.lower() == "director":
            # If search by director is asked 
            name = input("What director's movies do you want to check? \ninput: ")
            # Using getdata for getting director info and the counts of genres and printing
            movies,st,d1 = getdata(name,df)
            print(f"{name} has directed {','.join(movies)}\nHis most directed genres are {','.join(st)}\n")
        elif choice.lower() == "comparison":
            name1 = input("What is the first director you want to compare? \ninput1: ")
            name2 = input("What is the second director you want to compare? \ninput2: ")
            # Using getdata for getting directors  info for both directors to calculate cosine score and the counts of genres and printing
            movies1,st1,d1 = getdata(name1,df)
            movies2,st2,d2 = getdata(name2,df)
            if len(movies1)==0 or len(movies2)==0:
                print("No data found for the inputs")
                continue
            # Print the result data of genres counts and cosine score calculated above
            print(f"{name1} has directed {','.join(movies1)}\nHis most directed genres are {','.join(st1)} \n")
            print(f"{name2} has directed {','.join(movies2)}\nHis most directed genres are {','.join(st2)}")
            print(f"Based on that, they have a cosine similarity score of: {cosine(d1,d2)}")
        # If choice is stop break out of loop
        elif choice.lower() == "stop":
            break

main(movies)
