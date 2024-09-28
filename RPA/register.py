import asyncio
import pickle
import typer
from playwright.async_api import async_playwright
from typing_extensions import Annotated


def register_jobs(
    url_form: Annotated[str, typer.Argument(help="url to the company website on gupy")] = "https://forms.office.com/r/zfipx2RFsY",
    filepath: Annotated[str, typer.Option(help="Path to the file where the extracted jobs will be saved")] = "joblist.pkl"
):
    # Load job list
    with open(filepath, "rb") as file:
        job_list = pickle.load(file)[:3]

    asyncio.run(rpa_register_jobs(url_form, job_list))


async def rpa_register_jobs(url_form, job_list):
    async with async_playwright() as context_manager:
        browser = await context_manager.chromium.launch(headless=False)
        page = await browser.new_page()

        for job in job_list:
            await fill_form(page, job, url_form)

        await browser.close()


async def fill_form(page, job, url_form):
    await page.goto(url_form)
    await page.wait_for_timeout(1000)

    form_fields = await page.locator('[data-automation-id="questionItem"]').all()
    for field in form_fields:
        title = await field.locator('[data-automation-id="questionTitle"] .text-format-content').text_content()

        # Identify the field and fill in the entry
        field_index = ["Cargo", "Cidade", "Efetivo?"].index(title)
        if title == "Efetivo?":
            if job[field_index] == "Efetivo":
                await field.locator("input").first.check()
            else:
                await field.locator("input").last.check()
        else:
            await field.locator("input").fill(job[field_index])
        await page.wait_for_timeout(500)

    await page.locator('[data-automation-id="submitButton"]').click()

    await page.wait_for_timeout(1000)
