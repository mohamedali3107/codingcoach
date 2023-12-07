
rm -rf dashboard/migrations/
rm -rf llmcoach/migrations/

python3 manage.py makemigrations dashboard 
python3 manage.py makemigrations 
python3 manage.py makemigrations llmcoach


python3 manage.py migrate 