import subprocess as subproc
import sys
import os
import pwd
import shutil
import re
import requests
from pathlib import Path


dir_stack = []


def pushd(new_dir):
    """
    Pushes the current directory to a stack, then switches to the new directory.
    """
    global dir_stack
    dir_stack.append(os.getcwd())
    os.chdir(new_dir)


def popd():
    """
    Pops the last previous directory off the stack and switches to it.
    """
    global dir_stack
    os.chdir(dir_stack.pop(0))


home = pwd.getpwuid(os.getuid()).pw_dir
cicd_cache = home + '/.cicd_cache'
xiph_downloads = 'https://xiph.org/downloads'
xiph_regex = '(https://downloads.xiph.org/releases/ogg/lib'
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
tar = ['bsdtar', 'xvf']
sources = home + '/Sources'
mania_decomp = '/Sonic-Mania-Decompilation'
start_mods = ['ManiaTouchControls', 'MaxControl', 'UltrawideMania']
base_dir = sources + mania_decomp
os.makedirs(sources, exist_ok=True)


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


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


# should the directory be erased
if Path(base_dir).is_dir():
    # yes
    shutil.rmtree(base_dir)


os.chdir(sources)
subproc.call(git_clone + ['--recursive', rems + mania_decomp])
os.chdir(base_dir + '/dependencies/RSDKv5')
pushd(os.getcwd() + '/dependencies/android')
os.makedirs(cicd_cache, exist_ok=True)
try:
    with requests.get(xiph_downloads) as f:
        page = f.text
except requests.exceptions.RequestException as e:
    raise SystemExit(e)

ogg_matches = pattern_ogg.findall(page)
theora_matches = pattern_theora.findall(page)
if not ogg_matches:
    sys.exit('libogg not found, exiting')
if not theora_matches:
    sys.exit('libtheora not found, exiting')
libogg_url = ogg_matches[0][0]
libtheora_url = theora_matches[0][0]

if not is_downloadable(libogg_url):
    raise SystemExit('libogg download invalid: ' + libogg_url)
libogg_name = cicd_cache + '/' + get_filename_from_url(libogg_url)
if not Path(libogg_name).exists():
    libogg_zip = requests.get(libogg_url, allow_redirects=True)
    with open(libogg_name, 'wb') as f:
        f.write(libogg_zip.content)
os.makedirs(os.getcwd() + '/libogg', exist_ok=True)
subproc.call(tar + [libogg_name, '--strip-components=1', '-C', os.getcwd() + '/libogg'])
if not is_downloadable(libtheora_url):
    raise SystemExit('libtheora download invalid: ' + libtheora_url)
libtheora_name = cicd_cache + '/' + get_filename_from_url(libtheora_url)
if not Path(libtheora_name).exists():
    libtheora_zip = requests.get(libtheora_url, allow_redirects=True)
    with open(libtheora_name, 'wb') as f:
        f.write(libtheora_zip.content)
os.makedirs(os.getcwd() + '/libtheora', exist_ok=True)
subproc.call(tar + [libtheora_name, '--strip-components=1', '-C', os.getcwd() + '/libtheora'])
popd()
pushd(os.getcwd() + '/android/app/jni')
os.symlink(sources + mania_decomp, os.getcwd() + '/Game')
subproc.call(git_clone + ['--recursive', c0de + '/AHyperMania'])
subproc.call(git_clone + [rems + '/RSDKv5-Example-Mods'])
subproc.call(git_clone + ['--recursive', rems + '/RSDKv5-GameAPI', 'GameAPI'])
pushd(os.getcwd() + '/RSDKv5-Example-Mods')
for i in range(3):
    shutil.move(os.getcwd() + '/' + start_mods[i-1], os.getcwd() + '/..')
popd()
pushd(os.getcwd() + '/android/app/jni')
shutil.rmtree(os.getcwd() + '/RSDKv5-Example-Mods')
pushd(os.getcwd() + '/MaxControl/MaxControl')
with open(os.getcwd() + '/dllmain.c', 'r') as dllmain:
    maxcontrol_main = dllmain.readlines()
maxcontrol_main[0] = '#include \"../../GameAPI/C/GameAPI/Game.h\"\n'
with open(os.getcwd() + '/dllmain.c', 'w') as newmain:
    for line in maxcontrol_main:
        newmain.write(str(line))
popd()
print('Done!')
