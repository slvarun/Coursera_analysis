import requests
from bs4 import BeautifulSoup
import json

def find(course_cards,domain):
    courses = []
    c = 1
    for course in course_cards:
        print("course: ",c)
        c+=1
        course_details = {"Title": "","Enrolled":"", "Skills": [], "Rating": "", "Review": "", "Level": "", "Type": "", "Time": "","Link":"","Domain":domain}
        course_details["Link"] = course.find('a')['href']
        url1 = "https://www.coursera.org"+course_details["Link"]
        r1 = requests.get(url1)
        # print(url1)
        soup1 = BeautifulSoup(r1.text, "lxml")
        enrolled = soup1.find_all('div',class_="css-kd6yq1")
        if enrolled:
            course_details["Enrolled"] = enrolled[1].text
        # languages = soup1.find_all("div",class_="cds-Dialog-dialog")[0]
        # print(languages)
        # # .find("p"," css-4s48ix").text
        # break
        skills = course.find("div",class_="cds-ProductCard-body")
        if skills:
          course_details['Skills'] = skills.text.split(":")[1].split(",")
        title = course.find('h3', class_="cds-CommonCard-title")
        if title:
            course_details["Title"] = title.text.strip()
        review = course.find('div', class_="product-reviews css-pn23ng")
        if review:
            course_details["Rating"] = review.text.strip().split("(")[0]
            course_details["Review"] = review.text.strip().split("(")[1].split()[0]
        metadata = course.find('div', class_="cds-CommonCard-metadata")
        if metadata:
            metadata_parts = metadata.text.strip().split(" Â· ")
            course_details["Level"] = metadata_parts[0]
            course_details["Type"] = metadata_parts[1]
            course_details["Time"] = metadata_parts[2]
        # print(course_details)
        courses.append(course_details)
    return courses

courses = []
c = 1
domains = ["Business"]  #define all the domains you want to scrape
for domain in domains:
    print("-----------------------------------------")
    print(domain , c)
    c+=1
    print("-----------------------------------------")
    url = "https://www.coursera.org/search?topic="+domain+"&sortBy=BEST_MATCH"
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    course_cards = soup.find_all('li', class_="cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76 cds-90")
    n = soup.find_all('button', class_='cds-149 cds-paginationItem-default cds-button-disableElevation cds-button-ghost css-m6o159')
    while(not n):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        course_cards = soup.find_all('li', class_="cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76 cds-90")
        n = soup.find_all('button', class_='cds-149 cds-paginationItem-default cds-button-disableElevation cds-button-ghost css-m6o159')
    n = int(n[-1].text)
    for i in range(1,n):
        print("-----------------------------------------")
        print("page :",i," of ",n)
        print("-----------------------------------------")
        url = "https://www.coursera.org/search?topic="+domain+"&page="+str(i)+"&sortBy=BEST_MATCH"
        while(course_cards[0].find("div",class_="cds-ProductCard-body") == None):
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "lxml")
            course_cards = soup.find_all('li', class_="cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76 cds-90")
        courses.extend(find(course_cards,domain))
    break


file_path = 'COURSERA_DATA.json'
print(len(courses))
with open(file_path, 'w', encoding='utf-8') as f:
  f.write(json.dumps({'history':courses}, ensure_ascii=False,indent=2))