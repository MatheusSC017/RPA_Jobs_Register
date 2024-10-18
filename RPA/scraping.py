import bs4
import requests
import typer
import json
from typing import List
from typing_extensions import Annotated


def extract_job_list(
    url_job_list: Annotated[
        str, typer.Argument(help="URL to the company website on gupy")
    ],
    filepath: Annotated[
        str,
        typer.Option(help="Path to the file where the extracted jobs will be saved"),
    ] = "joblist.json",
    fields: Annotated[
        List[str], typer.Option(help="Name of the fields that will be used")
    ] = ["Cargo", "Cidade", "Efetivo?"],
):
    try:
        response = requests.get(url_job_list)
        if response.status_code == 200:
            html = bs4.BeautifulSoup(response.text, "html.parser")

            job_list = []
            for job in html.find_all(attrs={"data-testid": "job-list__listitem"}):
                job_title = job.select_one('[class*="sc-f5007364-4"]').text
                job_city = job.select_one('[class*="sc-f5007364-5"]').text
                job_type = job.select_one('[class*="sc-f5007364-6"]').text

                if len(fields) != 3:
                    fields = fields[:2]
                    fields.extend(["Cargo", "Cidade", "Efetivo?"][len(fields) :])

                job_list.append(
                    {fields[0]: job_title, fields[1]: job_city, fields[2]: job_type}
                )

            with open(filepath, "w") as file:
                json.dump(job_list, file, indent=4)
        else:
            print("Error loading the page")
    except Exception as e:
        print(f"An error occurred: {e}")
