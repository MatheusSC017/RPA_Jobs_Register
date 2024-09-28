# RPA_Avaliation

This project consists of an RPA script to automate the collection of job information from the gupy website for the SEB group (https://gruposeb.gupy.io/) and use this data to fill the forms (https://forms.office.com/r/zfipx2RFsY) and send the response

## Requirements

- Python 3.9 or above

  - Playwright;
  - Requests;
  - BeautifulSoup4


## Install

### Local

To install the dependencies run the commands below:

> pip install -r requirements.txt

> playwright install

### Docker

Run the command below to create the image

>  docker build -t rpa_avaliation --rm .

Init the app with the next command, this will start a bash that you will use to execute the commands

> docker run -it --name rpa_app --rm rpa_avaliation

## Use

The form extraction and register jobs method can be used separately or together to allow for reuse and customization of calls

### Scraping Jobs and Register in the Form

The first argument is a link to a company's website on Gupy, and if no data is provided, the SEB Group link will be used. 

The second argument is a link to the form that will be filled with the job information. 

> python main.py rpa-jobs "https://gruposeb.gupy.io/" "https://forms.office.com/r/zfipx2RFsY"

### Scraping Job List

The first argument is a link to a company's website on Gupy, and if no data is provided, the SEB Group link will be used. 

The second argument represents the path to the file where the extracted job list will be written, which is also optional.

> python main.py extract-job-list "https://gruposeb.gupy.io/"  --filepath "joblist.pkl"

### Registering Jobs

The first argument is a link to the form that will be filled with the job information. 

The second argument represents the path to the file where the list of extracted jobs is stored.

> python main.py register-jobs "https://forms.office.com/r/zfipx2RFsY" --filepath "joblist.pkl"
