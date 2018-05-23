#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser

from util.logger import logger
from twitter.twitter_search import search_query

if __name__ == '__main__':
    parser = ArgumentParser(
            prog = "(twitter_crawl.py)",

    )

    parser.add_argument('query', nargs = '*')
    parser.add_argument('--next_id', action = 'store', default = 'twitter_next_id.cfg')
    parser.add_argument('--query_file', action = 'store')

    args = parser.parse_args()
    logger.info('twitter crawler executed.')
    logger.debug(f'arguments : {args}')

    querys = args.query
    next_id = {}

    if args.query_file:
        try:
            logger.info(f'using query_file : {args.query_file}')
            with open(args.query_file, 'r', encoding = 'utf-8') as qf:
                querys = [s.strip() for s in qf.readlines()]

        except:
            raise

    print(querys)

    if args.next_id:
        try:
            logger.info('using next_id preservation.')
            with open(args.next_id, 'r', encoding = 'utf-8') as nf:
                next_id = {k.strip(): v.strip() for s in nf.readlines() for k, v in (s.split('='),)}
                print(next_id)

        except:
            raise

    if querys:
        for query in querys:
            next_id[query] = search_query(query, next_id.get(query, None))

        if args.next_id:
            try:
                logger.info('save next_id for session save.')
                with open(args.next_id, 'w', encoding = 'utf-8') as nf:
                    for k, v in next_id.items():
                        nf.write(f'{k}={v}')

            except:
                logger.error('critial error : cannnot save next_id')
