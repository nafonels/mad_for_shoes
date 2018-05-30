call ./venv/scripts/activate
python instagram_crawl.py --query_file=search_query.txt --next_id=instagram_end_cursor.cfg
call ./venv/scripts/deactivate