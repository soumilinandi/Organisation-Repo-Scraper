# Organisation-Repo-Scraper
App to fetch top N repositories of an organisation and top M commits of those repositories using Selenium, python and Flask

### Running app'
-  Clone the Repo
- **chromedriver** depending upon your OS, install chromedriver from :https://chromedriver.chromium.org/ [Pre-installed in repo for Linux]
- **set path for chromedriver** in *app.py* according to the location of chrome driver on your device on *line 28* and *line 98*
-  Open terminal in the directory and Run the commands : 
  
```
set FLASK_APP=app.py    
flask run
```

Go to http://127.0.0.1:5000/


#### Installation

```
# Install request, BeautifulSoup , Selenium , Python , flask

pip install BeautifulSoup
pip install Selenium
pip install flask
pip install requests
```


