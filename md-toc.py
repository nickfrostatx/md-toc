#!/usr/bin/env python

import re
import sys


pattern = re.compile(r'[\s\-,\']+')
def gentoc(headers):
    print('# Table of Contents\n')
    for header, level in headers:
        header_id = pattern.sub('-', header.lower())
        print(' ' * (level - 1) + '- [{0}](#{1})'.format(header, header_id))


def main(argv):
    for fname in argv[1:]:
        active = False
        with open(fname, 'r+') as f:
            active = True
            in_toc = False
            headers = []
            for l in f:
                l = l.strip()
                # Ignore TOC
                if '# Table of Contents' in l:
                    active = False
                elif not active and l.startswith('-'):
                    in_toc = True
                elif in_toc and l == '':
                    in_toc = False
                    active = True
                # actual header parsing
                elif active and l.startswith('#') and ' ' in l:
                    marker, header = l.split(' ', 1)
                    headers.append((header, len(marker)))
            gentoc(headers)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
