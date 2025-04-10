FROM python:3.11-slim

ENV TZ=Asia/Seoul

WORKDIR /app


RUN apt-get update && \
	apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libxcursor1 libnss3 lsb-release xdg-utils wget && \
	rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.4.2
RUN poetry config virtualenvs.create false && poetry config virtualenvs.in-project false

COPY pyproject.toml             ./
COPY poetry.lock                ./
COPY hyundai_driving_experience ./hyundai_driving_experience/

RUN poetry install --no-dev
RUN python ./hyundai_driving_experience/preload.py


ENTRYPOINT ["python", "./hyundai_driving_experience/scrape.py" ]
