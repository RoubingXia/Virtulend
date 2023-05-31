FROM python:3

COPY *.py /app/
COPY ../requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app
CMD ["python", "SteamGamesScraper.py"]


