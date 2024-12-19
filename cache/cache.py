# utils/cache.py

import hashlib
import os
import json

CACHE_DIR = 'cache/'

os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_key(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def get_cached_summary(text):
    key = get_cache_key(text)
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)['summary']
    return None

def set_cached_summary(text, summary):
    key = get_cache_key(text)
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    with open(cache_file, 'w') as f:
        json.dump({'summary': summary}, f)
