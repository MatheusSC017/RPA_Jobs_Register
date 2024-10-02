import typer
from typing_extensions import Annotated
from RPA.scraping import extract_job_list
from RPA.register import register_jobs


def rpa_jobs(
    url_job_list: Annotated[str, typer.Argument(help="URL to the company website on gupy")],
    url_form: Annotated[str, typer.Argument(help="Url to the google form")]
):
    extract_job_list(url_job_list)
    register_jobs(url_form)


app = typer.Typer()
app.command()(extract_job_list)
app.command()(register_jobs)
app.command()(rpa_jobs)


if __name__ == "__main__":
    app()
