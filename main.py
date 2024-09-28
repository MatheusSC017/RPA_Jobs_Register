import typer
from RPA.scraping import extract_job_list
from RPA.register import register_jobs


app = typer.Typer()
app.command()(extract_job_list)
app.command()(register_jobs)


if __name__ == "__main__":
    app()
