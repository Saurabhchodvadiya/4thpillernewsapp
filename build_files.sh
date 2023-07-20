echo "Build start"
python 3.9 -m  pip install -r requirements.txt
python 3.9 manage.py collectstatic  --noinput --clear
echo "Build End"