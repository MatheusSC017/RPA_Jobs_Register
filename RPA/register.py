import asyncio
import json
import typer
from playwright.async_api import async_playwright
from typing_extensions import Annotated


def register_jobs(
    url_form: Annotated[str, typer.Argument(help="url to the company website on gupy")],
    filepath: Annotated[
        str,
        typer.Option(help="Path to the file where the extracted jobs will be saved"),
    ] = "joblist.json",
):
    # Load job list
    with open(filepath, "r") as file:
        job_list = json.load(file)

    asyncio.run(rpa_register_jobs(url_form, job_list))


async def rpa_register_jobs(url_form, job_list):
    try:
        async with async_playwright() as context_manager:
            browser = await context_manager.chromium.launch(headless=False)
            page = await browser.new_page()

            for job in job_list:
                await fill_form(page, job, url_form)
                print(
                    f"{job['Cargo']}({job['Efetivo?']}) in {job['Cidade']} registered"
                )

            await browser.close()
    except Exception as e:
        print(f"An error occurred: {e}")


async def fill_form(page, job, url_form):
    response = await page.goto(url_form)
    if response and response.status == 200:
        await page.wait_for_timeout(500)

        form_fields = await page.locator('[data-automation-id="questionItem"]').all()
        for field in form_fields:
            title = await field.locator(
                '[data-automation-id="questionTitle"] .text-format-content'
            ).text_content()

            # Identify the field and fill in the entry
            if title == "Efetivo?":
                if job[title] == "Efetivo":
                    await field.locator("input").first.check()
                else:
                    await field.locator("input").last.check()
            else:
                await field.locator("input").fill(job[title])
            await page.wait_for_timeout(500)

        await page.locator('[data-automation-id="submitButton"]').click()
        await page.wait_for_timeout(250)
    else:
        raise Exception(f"Error loading {url_form}")
