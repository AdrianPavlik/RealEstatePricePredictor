# Real Estate Price Predictor

This project is developed as part of a school diploma initiative and serves as a comprehensive tool for real estate price prediction and market analysis. By scraping data from prominent Slovak real estate websites like nehnutelnosti.sk, reality.sk, and topreality.sk, this application leverages Django’s robust framework to provide insightful analytics through complex charts, graphs, and heatmaps.

## Purpose 

The goal of this project is to offer a real-time analytical tool that assists users—from real estate investors to home buyers—in making informed decisions based on the latest market trends. The dashboard not only predicts prices but also presents a detailed analysis of the real estate market, helping users understand price determinants and market dynamics.


## Features

- Real-Time Price Prediction: Leverages machine learning to forecast real estate prices using data from top Slovak property websites.
- Automated Scraping: Runs scraping operations separately to maintain high performance and responsiveness of the main application.
- Data Visualization: Provides detailed charts, graphs, and heatmaps for in-depth market analysis.
- Independent Scraping Services: Enhances scalability and efficiency by isolating the scraping processes from the main app.
- Responsive Design: Offers a user-friendly interface that works seamlessly across all devices, powered by Django.
- Security and Scalability: Incorporates Django’s robust security frameworks to safeguard data and ensure system reliability.

## Supported websites

| Website           | Supported |
|-------------------|-----------|
| reality.sk        | Yes       |
| nehnutelnosti.sk  | No        |
| topreality.sk     | No        |
| bazos.sk          | No        |

## Install

### Prerequisites

- **Python 3.10 or newer**: [official Python website](https://www.python.org/downloads/)
- **Docker**: [official Docker website](https://www.docker.com/products/docker-desktop/)

### Deploy

```cmd
docker-compose up --build -d
```

App will be run on port http://localhost:8000/

### Development

```cmd
pip install -r requirements.txt
python manage.py runserver
```

App will be run on port http://127.0.0.1:8000/


