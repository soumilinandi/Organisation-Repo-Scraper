from flask import Flask, redirect, url_for, request,render_template
import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 

###########################################################################################################
#  FUNCTION TO GET TOP M COMMITS OF A REPOSITORY
#
#  The function takes url for contribution page of the repo,m and produces the result
#
#  Input  - url<string> - url passed from organisation repo page
#         - m<int> - m is number of commitees and commits
#         - result<string> - string to be printed at end
#
#  Output - result<string> - string appended from this function added to result
#
###########################################################################################################
def getTopCommits(url,m,result):

    #url is the final modified url that contains list in order of number of commits
    url = url+ "/graphs/contributors"

    #get page by Selenium 
    
    #change path to the directory where chromedriver is installed
    driver = webdriver.Chrome('/home/mili/Downloads/chromedriver')  
    driver.get(url)  
  
    # this is just to ensure that the page is loaded 
    time.sleep(5)  
  
    #load the html content from driver into html
    html = driver.page_source 

    #Beutiful soup part
    soup = BeautifulSoup(html, "html.parser")

    #fetch users from class that surrounds every user
    users = soup.find_all('h3',class_="border-bottom p-2 lh-condensed")

    #counter for displaying user number in repo
    user_number = 1

    #----------------------------------------------------------------------
    # for loop to display all github userid and commit numbers
    # excluding 0th index as it shows irrelevant information 
    #----------------------------------------------------------------------
    for user in users[1:]:

        #class wrapping user_id stored in user_id
        user_id = user.find('a',class_="text-normal")

        #class wrapping commit number stored in user_commit_no
        user_commit_no = user.find('a',class_="link-gray text-normal")

        #result string appended to user_number counter, user_id, user commit number
        result = result + str(user_number) + " : " + str(user_id.text) + " : "
        result = result + str(user_commit_no.text) + "</br>"

        #user number counter incremented
        user_number = user_number + 1

        #m that is number of committes to be searched decremented
        m = m-1

        #break out of for loop when m reaches 0
        if(m==0):
            break

    #close the chrome driver
    driver.close()

    #return the modified result 
    return result


###########################################################################################################################
#  FUNCTION TO GET TOP N REPO OF AN ORGANISATION
#
#  The function takes organisation name and a predefined url to find top n repositories
#
#  Input  - organisation<string> - name of organisation
#         - n<int> - n is number of repo
#         - page<int> - page number on url for every 10 results
#         - m<int> - m is number of committes and commits
#         - result<string> - result to be printed at end
#
#  Output - result<string> - string appended from this function added to result
#
###########################################################################################################################
def getTopRepo(organisation,n,page,m,result):

    #get page by Selenium 
    
    #change path to the directory where chromedriver is installed
    driver = webdriver.Chrome('/home/mili/Downloads/chromedriver') 

    #url for every organisation is predefined, we append the organisation name and page number to make it work
    #every page has 10 results, for case when n is greater than 10, we keep generating next page
    url = "https://github.com/search?o=desc&p=" + str(page) + "&q=user%3A" + organisation + "+&s=forks&type=Repositories" 
    driver.get(url)  

    #load the html page into html  
    html = driver.page_source 

    #close the chrome driver
    driver.close()

    
    #Beutiful soup part
    soup = BeautifulSoup(html, "html.parser")

    #fetch the repo into repos by class surrounding every repo name
    repos = soup.find_all('a',class_="v-align-middle")

    #counter to keep track of repo number on current page
    i=0

    #----------------------------------------------------------------------
    # for loop to display all top repo on the current page url
    # stops when n becomes 0 or all repo on current page traversed
    #----------------------------------------------------------------------
    for repo in repos:

        #repo_link contains url to the repo
        repo_link = "https://github.com"+ str(repo['href'])

        #result is appended with Repo number, repo text 
        result = result +"</br><strong>"+"Repo " + str(((page-1)*10)+i+1) + " : " + str(repo.text) + "</strong></br>"
        result = result +  str("Top committes and commit number : </br>")

        #get top m commits and commitees for repo_link for each number in n
        result = getTopCommits(repo_link,m,result)

        #increment counter of current repository on current page
        i = i+1

        #decrement n
        n = n-1

        #stop and break out of loop when all n traversed
        if(n==0):
            break
 
    #incase number is greater than 10,20,30 and so on, function called recursively accordingly
    #10 repo loaded every time : for n=4, function called 4 times in total    
    if(n>0):
        #result modified by recurive call
        result = getTopRepo(organisation,n,page+1,result)

    #return final result to display on web browser
    return result

#flask app
app = Flask(__name__) 

#######################################################################################
# FUCTION to redirect to input.html
#######################################################################################
@app.route('/')
def main():
    return render_template('input.html')

#######################################################################################
# FUNCTION to redirect on success
#######################################################################################
@app.route('/success/<name>/<int:nnum>/<int:mnum>') 
def success(name,nnum,mnum): 
    #initalize res as empty
    res = ""

    #modify res by getTopRepo, 1 is the default starting page number as 1
    res = getTopRepo(name,nnum,1,mnum,res)

    #return res to screen
    return res

#######################################################################################
# FUNCTION executed when pressed submit on input.html
#######################################################################################
@app.route('/input',methods = ['POST', 'GET']) 
def input(): 

    #On POST request
    if request.method == 'POST': 
        #nm is org name
        org_name = request.form['nm'] 

        # n1 and nm1 is n
        n1 = request.form['nm1'] 

        # m1 and nm2 is m
        m1 = request.form['nm2'] 
        return redirect(url_for('success',name = org_name,nnum=n1,mnum=m1)) 

    #On GET request
    else: 
        #nm is org name
        user = request.args.get('nm') 

        # n1 and nm1 is n
        n1 = request.args.get('nm1') 

        # m1 and nm2 is m
        m1 = request.args.get('nm2') 
        return redirect(url_for('success',name = org_name,nnum=n1,mnum=m1)) 

if __name__ == '__main__': 
    app.run(debug = True) 
