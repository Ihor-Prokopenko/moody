# The app to analyze comments

![Work flow diagram](MOODY-Work-flow-diagram.png)

---

### Poetry

- To add package:

  ```poetry add --dev package-name```

- To update poetry.lock:

   ```poetry lock --no-update```

---

### Docker

- To create superuser via docker-compose:

  ```docker-compose run --rm api bash -c "python manage.py createsuperuser"```

### Youtube API

- To install google-api-python-client

  ```pip install charset-normalizer```

  ```poetry add google-api-python-client```


