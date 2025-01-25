# URLTesting

This is a service to transfer long address to short address with Python, Flask, MongoDB Cloud, Docker and RESTful API.


## Features
- Generate short URL by long URL
- Redirect to long URL by generated URL
- URL generation supports custom alias

## Demo in local
``` bash
curl -X POST http://127.0.0.1:5000/shorten -H "Content-Type: application/json" -d '{"original_url": "https://stackoverflow.com/questions/77653645/preparing-metadata-setup-py-error-error-subprocess-exited-with-error"}'

```
## How to run in Local 
- Python 3.8
- Flask
- Docker
- DynamoDB Cloud


## Tech Stack
- RESTful API
- Python
- Flask
- MongoDB
- Docker

