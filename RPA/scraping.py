import bs4
import requests
import typer
import json
from typing_extensions import Annotated


def extract_job_list(
    url_job_list: Annotated[str, typer.Argument(help="URL to the company website on gupy")],
    filepath: Annotated[str, typer.Option(help="Path to the file where the extracted jobs will be saved")] = "joblist.json"
):
    try:
        response = requests.get(url_job_list)
        if response.status_code == 200:
            html = bs4.BeautifulSoup(response.text, "html.parser")

            job_list = []
            for job in html.find_all(attrs={"data-testid": "job-list__listitem"}):
                job_list.append({title: field.text for title, field in zip(["Cargo", "Cidade", "Efetivo?"], job.findAll("div")[1:])})

            with open(filepath, "w") as file:
                json.dump(job_list, file, indent=4)
        else:
            print("Error loading the page")
    except Exception as e:
        print(f"An error occurred: {e}")