import os
import sys
import urllib.request
import datetime
import time
import json
from config import *

def get_request_url(url):
    
    req = urllib.request.Request(url)
    req.add_header("key", val)