FROM python:3.9-slim

WORKDIR /home/app_user

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && playwright install --with-deps

COPY . .

CMD ["bash"]