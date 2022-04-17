import requests
import os
from bs4 import BeautifulSoup



headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}

os.system("clear")

def extract_wwr_jobs(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, "html.parser")
  links = soup.find("div", {"class":"jobs-container"}).find_all("li", {"class":"view-all"})
  wwr_jobs = []
  
  for link in links:
    link = "https://weworkremotely.com" + link.find("a")["href"]
    print("\n---------new page------------\n")
  
    link_r = requests.get(link)
    link_soup = BeautifulSoup(link_r.text, "html.parser")
    job_list = link_soup.find("article").find_all("li", {"class":"feature"})
    
       
    for item in job_list:
        company = item.find("span", {"class":"company"}).string
        title = item.find("span", {"class":"title"}).string
        links = item.find_all("a")
        apply_link = links[1]['href']
        
        job = {
          "company": company,
          "title": title,
          "link": "https://weworkremotely.com" + apply_link
        }
        wwr_jobs.append(job)
    return wwr_jobs

  
def extract_so_jobs(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, "html.parser")
  pagination = soup.find("div", {"class":"s-pagination"})
  pages = pagination.find_all("a")[:-2]
  so_jobs = []

  for page in pages:
    print("\n---------new page------------\n")
    so_r = requests.get("https://stackoverflow.com/" + page["href"])
    so_soup = BeautifulSoup(so_r.text, "html.parser")
    job_list = so_soup.find("div", {"class":"listResults"}).find_all("div", {"class":"js-result"})
    
    for item in job_list:
      company = item.find("h3").find("span").text.strip()
      title = item.find("h2").find("a")["title"]
      apply_link = item.find("h2").find("a")["href"]
      
      job = {
          "company": company,
          "title": title,
          "link": "https://stackoverflow.com" + apply_link
        }
      so_jobs.append(job)
    return so_jobs



def extract_ro_jobs(url):
  r = requests.get(url, headers=headers)
  soup = BeautifulSoup(r.text, "html.parser")
  job_list = soup.find("table", {"id":"jobsboard"}).find_all("tr", {"class":"job"})

  ro_jobs=[]
  
  for item in job_list:
    company = item["data-company"]
    title = item.find("td", {"class":"position"}).find("a", {"class":"preventLink"}).find("h2").string.strip()
    apply_link = item.find("td", {"class":"position"}).find("a", {"class":"preventLink"})["href"]
    
    job = {
      "company": company,
      "title": title,
      "link": "https://remoteok.com" + apply_link
    }
    ro_jobs.append(job)
  return ro_jobs


def get_jobs(word):
  ro_url = f"https://remoteok.io/remote-dev+{word}-jobs"
  so_url = f"https://stackoverflow.com/jobs?r=true&q={word}"
  wwr_url = f"https://weworkremotely.com/remote-jobs/search?term={word}"

  wwr_jobs = extract_wwr_jobs(wwr_url)
  so_jobs = extract_so_jobs(so_url)
  ro_jobs = extract_ro_jobs(ro_url)

  jobs = wwr_jobs + so_jobs + ro_jobs
  return jobs