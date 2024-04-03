## Создать файл .env

    # DJANGO
    SECRET_KEY='kipzc*9@f%^a0!7h_%23lyh!4trkmz=(!dpdo32noy4axm=izt'
    
    # SITE
    SITE_HOST=localhost
    
    # DOCS
    API_DOCS_ENABLE=true
    
    # POSTGRES
    POSTGRES_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=12345
    POSTGRES_PORT=5432
    
    # TELEGRAM
    TELEGRAM_URL=https://api.telegram.org/
    BOT_TOKEN=...

## Запуск бэкенда
```shell
docker-compose -f docker-compose.prod.yml up -d --build 
```