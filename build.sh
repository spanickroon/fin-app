pip install -r src/requirements.txt

grep -v '^#' src/variables/prod.env
export $(grep -v '^#' .env | xargs)

python3 src/manage.py migrate --no-input