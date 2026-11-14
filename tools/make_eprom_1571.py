#!/usr/bin/env python3
"""make_eprom_1571.py - EPROM-Vorlage C1571_29F040.BIN fuer die externe 1571.

Schema wie die C128DCR-Vorlage C1571_C128DCR_29F040.BIN (8 Baenke zu 64 KB,
n@RNROM waehlt Bank n, untere Haelfte $FF, DOS ab $x8000):

  Bank 1, 2, 5-8  Commodore DOS V3.0 1571 (310654-05)   $x8000-$xFFFF
  Bank 3          DolphinDOS 3 1571 (Original)           $28000-$2FFFF
  Bank 4          C1571DolphinDos26 (64 KB)              $30000-$3FFFF

Aufruf: tools/make_eprom_1571.py [ausgabe]   (Standard: rom/C1571_29F040.BIN)
Quellen werden ueber das Projektverzeichnis mit Builds/ gefunden.
"""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def root():
    d = REPO
    while d != '/':
        if os.path.isdir(os.path.join(d, 'Builds')) and os.path.isdir(os.path.join(d, 'Referenzen')):
            return d
        d = os.path.dirname(d)
    sys.exit('Projektverzeichnis mit Builds/ nicht gefunden')


R = root()
SRC = {
    'cbm': (os.path.expanduser('~/.local/vice-ms/share/vice/DRIVES/dos1571-310654-05.bin'), 0x8000,
            'dae964d64b7843ff86c008d396dda208'),
    'dd3': (os.path.join(R, 'Referenzen', '1571-DolphinDos3.ROM.BIN'), 0x8000,
            'e39a154877cc3a1a893688bc8cabccf2'),
    'dd26': (os.path.join(R, 'Builds', 'C1571_DOLPHINDOS26.bin'), 0x10000, None),
}
BANKS = ['cbm', 'cbm', 'dd3', 'dd26', 'cbm', 'cbm', 'cbm', 'cbm']


def load(k):
    p, size, md5 = SRC[k]
    d = open(p, 'rb').read()
    if len(d) != size:
        sys.exit('%s: %d Bytes statt %d' % (p, len(d), size))
    if md5 and hashlib.md5(d).hexdigest() != md5:
        sys.exit('%s: falsche Pruefsumme' % p)
    return d


out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'rom', 'C1571_29F040.BIN')
img = bytearray()
for k in BANKS:
    d = load(k)
    img += b'\xff' * (0x10000 - len(d)) + d
assert len(img) == 0x80000
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'wb').write(img)
print('%s  %s' % (hashlib.md5(img).hexdigest(), out))
