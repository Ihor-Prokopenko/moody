# The app to analyze comments

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
