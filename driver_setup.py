#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import zipfile
from urllib import request

__author__ = 'Teoslard'
__version__ = "$"

chromedriver = "https://chromedriver.storage.googleapis.com/2.38/chromedriver_win32.zip"
os.makedirs('temp')

with request.urlopen(chromedriver) as driver_response:
    with open('./temp/driver.zip', 'wb') as t:
        t.write(driver_response.read())

    with open('./temp/driver.zip', 'rb') as driver_zip:
        zip_cur = zipfile.ZipFile(driver_zip)
        zip_cur.extractall('./driver')

shutil.rmtree('temp')
