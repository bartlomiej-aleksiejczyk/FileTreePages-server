# Django Simple Project Template

## Overview

This app was created using django simple project template

## Template Content

This template includes:

- Django
- PostgreSQL
- Docker Compose integration
- Working Auth without registration
- Fail2Ban integration
- Precoinfigured templates and static files
- Huey configured as message queue

## How to run

**Local development version:**

```
docker-compose -f docker-compose-dev.yml up
```

**Production version:**

```
docker compose -f docker-compose-prod.yml up
```

## Command Passthrough

```
docker compose -f <your-docker-compose-name> exec django <your-command-content>
```

examples:

```
docker compose -f docker-compose-dev.yml exec django pip freeze > requirements.txt
docker compose -f docker-compose-dev.yml exec django pip install requests==2.32.3
```
## Template URL
https://github.com/bartlomiej-aleksiejczyk/django-template-copier