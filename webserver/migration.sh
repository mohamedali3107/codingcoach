
rm -rf dashboard/migrations/
rm -rf llmcoach/migrations/

python3 manage.py makemigrations dashboard 
python3 manage.py makemigrations 
python3 manage.py makemigrations llmcoach


python3 manage.py migrate 


export DJANGO_SUPERUSER_USERNAME=root
export DJANGO_SUPERUSER_EMAIL=myadmin@example.com
export DJANGO_SUPERUSER_PASSWORD=root

python3 manage.py createsuperuser --noinput