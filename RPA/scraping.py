import bs4
import requests
import typer
import pickle
from typing_extensions import Annotated


def extract_job_list(
    url_job_list: Annotated[str, typer.Argument(help="URL to the company website on gupy")] = "https://gruposeb.gupy.io/",
    filepath: Annotated[str, typer.Option(help="Path to the file where the extracted jobs will be saved")] = "joblist.pkl"
):
    response = requests.get(url_job_list)
    html = bs4.BeautifulSoup(response.text, "html.parser")

    job_list = []
    for job in html.findAll("li", {"data-testid": "job-list__listitem"}):
        job_list.append([field.text for field in job.findAll("div")[1:]])

    with open(filepath, "wb") as file:
        pickle.dump(job_list, file)
