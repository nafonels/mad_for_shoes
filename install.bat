virtualenv venv
call ./venv/scripts/activate
echo python venv activated

mkdir data
cd data
mkdir raw
cd ..

pip install -r requirements.txt
python driver_setup.py
echo selenium driver installed