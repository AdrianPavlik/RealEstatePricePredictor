FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get update && apt-get install -y --no-install-recommends python3-venv
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
