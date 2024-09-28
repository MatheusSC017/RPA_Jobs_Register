import bs4
import requests
import asyncio
from playwright.async_api import async_playwright


URL_JOB_LIST = "https://gruposeb.gupy.io/"
URL_FORM = "https://forms.office.com/r/zfipx2RFsY"


def extract_job_list():
    response = requests.get(URL_JOB_LIST)
    html = bs4.BeautifulSoup(response.text, "html.parser")

    job_list = []
    for job in html.findAll("li", {"data-testid": "job-list__listitem"}):
        job_list.append([field.text for field in job.findAll("div")[1:]])

    return job_list


if __name__ == "__main__":
    job_list = extract_job_list()
    print(job_list)
