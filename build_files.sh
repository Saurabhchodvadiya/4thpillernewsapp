echo "Build start"
python -m  pip install -r requirements.txt
python manage.py collectstatic  --noinput --clear
echo "Build End"