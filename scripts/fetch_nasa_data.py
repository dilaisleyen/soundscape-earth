#!/usr/bin/env python3
"""Download the NASA pictures listed in data/nasa/SOURCES.json again.

Why the pictures are kept in this project: NASA's server does not send CORS headers, so a web page cannot read the
pixels of a picture loaded straight from it (the page reads the colours to get the temperatures).

What it does, for every entry with "fetch": true:
  - downloads the "url" into data/nasa/<file>,
  - writes the new size ("bytes"), checksum ("sha256"), download date ("downloaded") and the server's
    Last-Modified date ("last_modified") back into SOURCES.json.
If the downloaded picture is not the same as before, "data_date" is set to null: the pictures have no date stamp, so
the date of the new picture has to be found and written in by hand.

Special entries:
  - "latest_day": true (the "Today" picture of the Through the years slider): before downloading, the script asks
    GIBS for the newest day the layer has, puts that day into the url (from "url_template") and into "data_date".
    The page itself never looks for a newer day: it shows the picture that was downloaded, with the date written here.
  - "date_known": true (pictures asked for a fixed day): "data_date" stays even if the picture changes.
  - "kind": "colormap" (an XML file instead of a picture).

Entries with "fetch": false (derived files, converted from NASA's own files) are listed but never touched.

Only the Python standard library is used.

  python scripts/fetch_nasa_data.py --list
  python scripts/fetch_nasa_data.py --dry-run
  python scripts/fetch_nasa_data.py --only sst_colorbar
  python scripts/fetch_nasa_data.py
"""
import argparse
import datetime
import email.utils
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NASA_DIR = os.path.join(ROOT, 'data', 'nasa')
SOURCES = os.path.join(NASA_DIR, 'SOURCES.json')
USER_AGENT = 'soundscape-earth-fetch/1.0 (downloads the NASA pictures listed in SOURCES.json)'


def destination(entry):
    """The place a file is saved. It must stay inside data/nasa/."""
    path = os.path.realpath(os.path.join(NASA_DIR, entry['file']))
    if os.path.commonpath([path, os.path.realpath(NASA_DIR)]) != os.path.realpath(NASA_DIR):
        raise ValueError(f"{entry['file']}: outside data/nasa/")
    return path


def download(url, path, kind='image/'):
    """Downloads url to path (through a temporary file). Returns (bytes, sha256, last_modified)."""
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    handle, temp = tempfile.mkstemp(dir=folder, suffix='.part')
    try:
        digest = hashlib.sha256()
        size = 0
        with urllib.request.urlopen(request, timeout=120) as response, os.fdopen(handle, 'wb') as out:
            kind_header = response.headers.get('Content-Type', '')
            if not kind_header.startswith(kind):
                raise ValueError(f'expected {kind}, the server sent {kind_header or "no type"}')
            modified = response.headers.get('Last-Modified')
            while True:
                chunk = response.read(1 << 16)
                if not chunk:
                    break
                out.write(chunk)
                digest.update(chunk)
                size += len(chunk)
        if size == 0:
            raise ValueError('the server sent an empty file')
        os.replace(temp, path)
    except Exception:
        if os.path.exists(temp):
            os.remove(temp)
        raise
    if modified:
        try:
            modified = email.utils.parsedate_to_datetime(modified).date().isoformat()
        except (TypeError, ValueError):
            pass
    return size, digest.hexdigest(), modified


def newest_day(entry):
    """The newest day GIBS has for the layer of this entry (read from the layer's capabilities)."""
    url = ('https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi?SERVICE=WMTS&request=GetCapabilities&layer='
           + entry['layer'])
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        text = response.read().decode('utf-8', 'replace')
    found = re.search(r'<Default>(\d{4}-\d{2}-\d{2})</Default>', text)
    if not found:
        raise ValueError('could not read the newest day from the capabilities')
    return found.group(1)


def main():
    parser = argparse.ArgumentParser(description='Download the NASA pictures listed in data/nasa/SOURCES.json again.')
    parser.add_argument('--list', action='store_true', help='only list the entries')
    parser.add_argument('--dry-run', action='store_true', help='show what would be downloaded, change nothing')
    parser.add_argument('--only', metavar='TEXT', help='only entries whose file name contains TEXT')
    args = parser.parse_args()

    with open(SOURCES, encoding='utf-8') as f:
        doc = json.load(f)
    entries = [e for e in doc['files'] if not args.only or args.only in e['file']]
    if not entries:
        print('No entry matches.')
        return 1

    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    failed = changed = fetched = 0
    for entry in entries:
        label = f"{entry['file']}  ({entry.get('kind', '?')}, data date {entry.get('data_date')})"
        if args.list:
            print(('fetch ' if entry.get('fetch') else 'skip  ') + label)
            continue
        if not entry.get('fetch'):
            continue          # derived files are never downloaded here
        if args.dry_run:
            print(f"would download {entry['url']}\n           to {entry['file']}")
            continue
        try:
            if entry.get('latest_day'):
                day = newest_day(entry)
                entry['url'] = entry['url_template'].replace('{date}', day)
                entry['data_date'] = day
                print(f"newest day of {entry['layer']}: {day}")
            size, sha, modified = download(entry['url'], destination(entry), 'text/xml' if entry.get('kind') == 'colormap' else 'image/')
        except Exception as error:
            failed += 1
            print(f"FAILED  {entry['file']}: {error}")
            continue
        fetched += 1
        same = sha == entry.get('sha256')
        entry.update({'downloaded': today, 'bytes': size, 'sha256': sha, 'last_modified': modified})
        if not same and not entry.get('date_known'):
            changed += 1
            entry['data_date'] = None
            print(f"CHANGED {entry['file']}: not the same picture as before ({size} bytes). "
                  'Its data date is now null: find the date and write it in. If this is the picture that opens '
                  'with the page, the base64 copy inside index.html has to be rebuilt too.')
        elif not same:
            print(f"ok      {entry['file']}: downloaded ({size} bytes; its date is fixed, so it stays {entry.get('data_date')})")
        else:
            print(f"ok      {entry['file']}: same picture as before ({size} bytes)")

    if args.list:
        derived = sum(1 for e in entries if not e.get('fetch'))
        print(f'{len(entries)} entries, {derived} derived (not downloaded by this script).')
    elif not args.dry_run and fetched:
        with open(SOURCES, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f'SOURCES.json updated: {fetched} downloaded, {changed} changed, {failed} failed.')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
