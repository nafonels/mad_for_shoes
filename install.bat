virtualenv venv
call ./venv/scripts/activate
echo python venv activated

pip install -r requirements.txt
python driver_setup.py
echo selenium driver installed