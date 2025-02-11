import subprocess as subproc
import sys
import os
import shutil
import re
import requests
from pathlib import Path
import platform

# Cross-platform home directory
home = str(Path.home())
cicd_cache = os.path.join(home, '.cicd_cache')
xiph_downloads = 'https://xiph.org/downloads'
pattern_ogg = re.compile(
    r'href=["\'](https?://[^\s"\'<>]+/(libogg)-(?:\d+\.){3}zip)["\']',
    re.IGNORECASE
)
pattern_theora = re.compile(
    r'href=["\'](https?://[^\s"\'<>]+/(libtheora)-(?:\d+\.){3}zip)["\']',
    re.IGNORECASE
)
git_clone = ['git', 'clone']
github = 'https://github.com'
c0de = github + '/c0des1ayr'
rems = github + '/RSDKModding'
sources = os.path.join(home, 'Sources')
mania_decomp = 'Sonic-Mania-Decompilation'
base_dir = os.path.join(sources, mania_decomp)
os.makedirs(sources, exist_ok=True)

# Determine OS-specific tar command
tar = ['tar', 'xvf'] if platform.system() != 'Windows' else ['tar.exe', '-xf']

def is_downloadable(url):
    """
    Check if URL contains a downloadable resource
    """
    try:
        h = requests.head(url, allow_redirects=True)
        content_type = h.headers.get('content-type', '').lower()
        return not any(x in content_type for x in ['text', 'html'])
    except requests.exceptions.RequestException:
        return False


def get_filename_from_url(url):
    """
    Get filename from content-disposition (or url, failsafe only)
    """
    r = requests.get(url, allow_redirects=True)
    cd = r.headers.get('content-disposition')
    if cd:
        fname = re.findall('filename=(.+)', cd)
        if len(fname) != 0:
            return fname[0]
    if url.find('/'):
        return url.rsplit('/', 1)[1]
    return None


# Remove directory if exists
if Path(base_dir).is_dir():
    shutil.rmtree(base_dir)

os.makedirs(sources, exist_ok=True)
os.chdir(sources)
subproc.call(git_clone + ['--recursive', rems + '/' + mania_decomp])

os.makedirs(cicd_cache, exist_ok=True)
try:
    page = requests.get(xiph_downloads).text
except requests.exceptions.RequestException as e:
    sys.exit(e)

ogg_matches = pattern_ogg.findall(page)
theora_matches = pattern_theora.findall(page)
if not ogg_matches:
    sys.exit('libogg not found, exiting')
if not theora_matches:
    sys.exit('libtheora not found, exiting')

libogg_url = ogg_matches[0][0]
libtheora_url = theora_matches[0][0]

# Download and extract libraries
for lib_url, lib_name in [(libogg_url, 'libogg'), (libtheora_url, 'libtheora')]:
    if not is_downloadable(lib_url):
        sys.exit(f'{lib_name} download invalid: {lib_url}')
    lib_path = os.path.join(cicd_cache, get_filename_from_url(lib_url))
    if not Path(lib_path).exists():
        with open(lib_path, 'wb') as f:
            f.write(requests.get(lib_url, allow_redirects=True).content)
    extract_path = os.path.join(os.getcwd(), lib_name)
    os.makedirs(extract_path, exist_ok=True)
    subproc.call(tar + [lib_path, '--strip-components=1', '-C', extract_path])

# Handle symbolic link or copy for Windows
link_target = os.path.join(os.getcwd(), 'Game')
link_source = base_dir
if platform.system() == 'Windows':
    shutil.copytree(link_source, link_target, dirs_exist_ok=True)
else:
    os.symlink(link_source, link_target)

sys.exit('Done!')
