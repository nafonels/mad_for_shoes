call ./venv/scripts/activate
python twitter_crawl.py --query_file=search_query.txt --next_id=twitter_next_id.cfg
call ./venv/scripts/deactivate