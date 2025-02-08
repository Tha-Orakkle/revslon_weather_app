# SIMPLE WEATHER BACKEND API

## Description

RESTful API service for a weather app.

## Installation

```bash
git clone https://github.com/Tha-Orakkle/revslon-weather-app.git
cd revslon-weather-app/
```

**create and activate a virtual environment**

```bash
virtualenv venv

source ven/bin/activate # On Linux or MacOS
.\venv\Scripts\activate.bat # Windows
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Migrate and run program**

```bash
python manage.py migrate
python manage.py runserver
```

# API Documentation

## Register User

**Endpoint:** `/register/`

**Method:** `POST`

**Description:** Register a new user.

**Request Body:**

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response:**

- **Success:** `200 OK`

```json
{
  "success": "User created successfully",
  "access": "string",
  "refresh": "string",
  "data": {
    "id": "integer",
    "username": "string",
    "email": "string"
  }
}
```

- **Error:** `400 Bad Request`

```json
{
  "error": "Please, provide complete credentials"
}
```

```json
{
  "error": "user with username already exists"
}
```

## Get Weather

**Endpoint:** `/weather/`

**Method:** `GET`

**Description:** Get the current temperature for a specified city.

**Request Parameters:**

- `city`: The name of the city (required).

**Headers:**

- `Authorization`: `Bearer <access_token>`

**Response:**

- **Success:** `200 OK`

```json
{
  "success": "The temperature in <city> is <temp> Celsius"
}
```

- **Error:** `400 Bad Request`

```json
{
  "error": "Invalid city name"
}
```

```json
{
  "error": "API error message"
}
```

## Get Search History

**Endpoint:** `/history/`

**Method:** `GET`

**Description:** Get the search history of the authenticated user.

**Headers:**

- `Authorization`: `Bearer <access_token>`

**Response:**

- **Success:** `200 OK`

```json
{
    "data": [
        {
            "id": "integer",
            "city": "string",
            "searched_at": "datetime"
        },
        ...
    ]
}
```
