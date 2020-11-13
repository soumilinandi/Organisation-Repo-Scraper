# Organisation-Repo-Scraper
App to fetch top N repositories of an organisation and top M committees and number of commits of those repositories using Selenium, python and Flask

## About the app:
A simple app that used web scraping (BeautifulSoup and Selenium) to fetch results from github. </br> Edge cases : 
- When N < number of Repositories of the organisation : Displays only the number of Repositories available
- When M < number of Committees : Displays only the number of Committees available and their number of commits

A sleep time of 10s has been added to make sure that contributions pages is loaded when internet speed is slow. </br> It can be reduced accordingly for better performance.  Browser will be automatically opened to fetch html page and closed while processing.
### Running the app        
-  Clone the Repo
- **chromedriver** depending upon your OS, install chromedriver from :https://chromedriver.chromium.org/ [Pre-installed in repo for Linux]
- **set path for chromedriver** in *app.py* according to the location of chrome driver on your device on *line 28* and *line 98*
-  Open terminal in the directory and Run the commands : 
  
```
set FLASK_APP=app.py    
flask run
```

Go to http://127.0.0.1:5000/


### Installation

```
# Install request, BeautifulSoup , Selenium , Python , flask

pip install BeautifulSoup
pip install Selenium
pip install flask
pip install requests
```
## Alternate Option : CLI

To avoid installing flask and running it on browser, Go the sub-folder **CLI** :
- Open the terminal and run : 

```
python git.py

```


