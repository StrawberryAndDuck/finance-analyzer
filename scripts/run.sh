DEFAULT_PORT=8080

export $(grep -v '^#' .env | xargs)
gunicorn --workers 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$DEFAULT_PORT -m 007 app.api.main:app --timeout 0 --keep-alive 5
