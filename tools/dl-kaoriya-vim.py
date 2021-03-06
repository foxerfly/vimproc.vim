#!/usr/bin/python3

# Download the latest KaoriYa Vim from the GitHub release

import argparse
import calendar
import io
import json
import os
import sys
import time
import urllib.request, urllib.error

# Repository Name
repo_name = 'koron/vim-kaoriya'
gh_release_url = 'https://api.github.com/repos/' + repo_name + '/releases/latest'

# Parse arguments
parser = argparse.ArgumentParser(
        description='Download the latest KaoriYa Vim from the GitHub release')
parser.add_argument('-f', '--force', action='store_true',
        help='overwrite the download file')
parser.add_argument('-n', '--filename', type=str, action='store',
        help='filename to save')
parser.add_argument('-a', '--arch', type=str, action='store',
        choices=['all', 'win32', 'win64'], default='all',
        help='architecture to download')
args = parser.parse_args()

if args.filename and args.arch == 'all':
    parser.error('-a must be specified when you specify -n.')

# Get information of GitHub release
# see: https://developer.github.com/v3/repos/releases/
try:
    response = urllib.request.urlopen(gh_release_url)
except urllib.error.HTTPError:
    print('GitHub release not found.', out=sys.stderr)
    exit(1)

rel_info = json.load(io.StringIO(str(response.read(), 'utf-8')))
print('Last release:', rel_info['name'])
print('Created at:', rel_info['created_at'])

# Download the files
for asset in rel_info['assets']:
    if args.filename:
        name = args.filename
    else:
        name = asset['name']
    if args.arch != 'all' and asset['name'].find(args.arch) < 0:
        continue
    if os.path.isfile(name) and not args.force:
        print('File exists:', name)
        continue
    print('Downloading to:', name)
    urllib.request.urlretrieve(asset['browser_download_url'], name)
    # Set timestamp
    asset_time = time.strptime(asset['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
    os.utime(name, times=(time.time(), calendar.timegm(asset_time)))
