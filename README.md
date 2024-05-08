## Movie Information Retrieval System

### Overview
This Python program fetches movie information for the top 500 most popular movies from Metacritic. It then allows users to interact with the collected data by providing three choices: retrieving information about a specific movie, a director, or comparing two directors based on their movie genres.
Website Link - "https://www.metacritic.com/browse/movie/"

### Step-by-Step Guide

#### 1. Scraping Metacritic
- Use the `requests` library to fetch the top 500 movies from Metacritic.
- Parse the HTML content of the webpage using `BeautifulSoup`.
- Extract movie titles, directors, and genres from the webpage.

#### 2. Extracting Information
- Process the extracted data to handle cases like multiple directors or missing genre information.
- Organize the data into a dictionary structure.

#### 3. Building a Dictionary
- Create a dictionary where movie titles are keys and director(s) and genres are values.

#### 4. Storing Data
- Save the collected information into a CSV file named `[your name]_movies.csv` using Pandas.

#### 5. User Interaction
- Write a main program to interact with the user, offering three options: 'movie', 'director', or 'comparison'.

#### 6. Option 1: Movie Information
- If the user selects 'movie', prompt for a movie name, search the dictionary, and display its director(s) and genre(s).

#### 7. Option 2: Director Information
- If the user selects 'director', prompt for a director's name, search the dictionary for movies directed by them, and summarize the genres.

#### 8. Option 3: Director Comparison
- If the user selects 'comparison', prompt for two director names, and calculate their cosine similarity based on their directed movie genres.

#### 9. Writing Task
- Write a short report comparing the careers of three favorite directors from the top 500 movies list, focusing on genre and thematic similarities.

### Usage
1. Clone or download the repository.
2. Run the Python script `movie_information_retrieval.py`.
3. Follow the prompts to interact with the program.

### Submission
Your submission should include the following files:
1. `movie_information_retrieval.py`: Python script containing the program.
2. `[your name]_movies.csv`: CSV file storing the collected movie information.
3. `director_comparison_report.docx`: Word document containing the short report on director comparisons.
