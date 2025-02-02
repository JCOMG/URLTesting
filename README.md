# URLTesting

This is a service to transfer long address to short address with Python, Flask, MongoDB Cloud, Docker, Heroku and RESTful API.


## Features
- Generate short URL by long URL
- Redirect to long URL by generated URL
- URL generation supports custom alias

## Demo in local
``` bash
curl -X POST http://127.0.0.1:5000/shorten -H "Content-Type: application/json" -d '{"original_url": "https://stackoverflow.com/questions/77653645/preparing-metadata-setup-py-error-error-subprocess-exited-with-error"}'

## Demo in Heroku
```  https://urltesting-heroku-87b2c8548b48.herokuapp.com/

## Tech Stack
- RESTful API
- Python
- Flask
- MongoDB
- Docker
- Heroku

