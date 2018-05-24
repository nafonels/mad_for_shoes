#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

LogLevel = logging.DEBUG

# http://docs.python.org/howto/logging.html#configuring-logging
logger = logging.getLogger('defaultLogger')
logger.setLevel(LogLevel)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

# create formatter for sh
# and add_method formatter to sh
sh_formatter = logging.Formatter('%(asctime)s [%(filename)s-%(name)s(%(lineno)s)] (%(levelname)s)\t: %(message)s',
                                 datefmt = '%Y/%m/%d %H:%M:%S')
sh.setFormatter(sh_formatter)

# add_method sh to logger
logger.addHandler(sh)

# logging.basicConfig(filename = "test.log")


fh = logging.FileHandler("crawling.log")
fh.setLevel(logging.NOTSET)
fh.setFormatter(sh_formatter)

logger.addHandler(fh)

# import log_handler

# dh = log_handler.SQLAlchemyHandler()
# dh.setLevel(LogLevel)

# logging test
# logger.warning("")
# logger.info("test logging")
