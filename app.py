from flask import Flask, redirect, url_for, request,render_template
import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 

def getTopCommits(url,m,result):
    #response = requests.get(url)
    url = url+ "/graphs/contributors"

    #get page by Selenium 
    driver = webdriver.Chrome('/home/mili/Downloads/chromedriver')  
    driver.get(url)  
  
    # this is just to ensure that the page is loaded 
    time.sleep(5)  
  
    html = driver.page_source 

    #normal bs stuff
    soup = BeautifulSoup(html, "html.parser")
    users = soup.find_all('h3',class_="border-bottom p-2 lh-condensed")
    user_number = 1
    for user in users[1:]:
        user_id = user.find('a',class_="text-normal")
        user_commit_no = user.find('a',class_="link-gray text-normal")
        result = result + str(user_number) + " : " + str(user_id.text) + " : "
        result = result + str(user_commit_no.text) + "</br>"
        user_number = user_number + 1
        m = m-1
        if(m==0):
            break
    driver.close()
    return result

def getTopRepo(organisation,n,page,m,result):
    

    driver = webdriver.Chrome('/home/mili/Downloads/chromedriver') 

    url = "https://github.com/search?o=desc&p=" + str(page) + "&q=user%3A" + organisation + "+&s=forks&type=Repositories" 
    driver.get(url)  
  
    # this is just to ensure that the page is loaded 
  
    html = driver.page_source 
    driver.close()

    #normal bs stuff
    soup = BeautifulSoup(html, "html.parser")
    repos = soup.find_all('a',class_="v-align-middle")

    i=0
    
    for repo in repos:
        repo_link = "https://github.com"+ str(repo['href'])

        result = result +"</br>"+"Repo " + str(((page-1)*10)+i+1) + " : " + str(repo.text) + "</br>"
        result = result +  str("Top committes and commit number : </br>")
        result = getTopCommits(repo_link,m,result)
        i = i+1
        n = n-1
        if(n==0):
            break
    
    if(n>0):
        #driver.close()
        result = getTopRepo(organisation,n,page+1,result)
    return result

app = Flask(__name__) 

@app.route('/')
def main():
    return render_template('input.html')
    
@app.route('/success/<name>/<int:nnum>/<int:mnum>') 
def success(name,nnum,mnum): 
    res = ""
    res = getTopRepo(name,nnum,1,mnum,res)
    return res

@app.route('/input',methods = ['POST', 'GET']) 
def input(): 
    if request.method == 'POST': 
        org_name = request.form['nm'] 
        n1 = request.form['nm1'] 
        m1 = request.form['nm2'] 
        return redirect(url_for('success',name = org_name,nnum=n1,mnum=m1)) 
    else: 
        user = request.args.get('nm') 
        n1 = request.args.get('nm1') 
        m1 = request.args.get('nm2') 
        return redirect(url_for('success',name = org_name,nnum=n1,mnum=m1)) 

if __name__ == '__main__': 
    app.run(debug = True) 
