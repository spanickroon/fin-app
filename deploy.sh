grep -v '^#' src/variables/prod.env
export $(grep -v '^#' .env | xargs)

cd src/ && gunicorn config.wsgi:application
