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


async def fill_form(job_list):
    async with async_playwright() as context_manager:
        browser = await context_manager.chromium.launch(headless=False)
        page = await browser.new_page()

        for job in job_list:
            await page.goto(URL_FORM)
            await page.wait_for_timeout(1000)

            form_fields = await page.locator('[data-automation-id="questionItem"]').all()
            for field in form_fields:
                title = await field.locator('[data-automation-id="questionTitle"] .text-format-content').text_content()
                field_index = ["Cargo", "Cidade", "Efetivo?"].index(title)
                if field_index != 2:
                    await field.locator("input").fill(job[field_index])
                else:
                    if job[field_index] == "Efetivo":
                        await field.locator("input").first.check()
                    else:
                        await field.locator("input").last.check()
                await page.wait_for_timeout(500)

            await page.locator('[data-automation-id="submitButton"]').click()

            await page.wait_for_timeout(1000)

        await browser.close()


if __name__ == "__main__":
    job_list = extract_job_list()
    asyncio.run(fill_form(job_list))
