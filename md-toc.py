#!/usr/bin/env python

import re
import sys


dashes = re.compile(r'[\s\-,]+')
drop = re.compile(r'\'+')
def gentoc(headers):
    out = '# Table of Contents\n\n'
    for header, level in headers:
        header_id = drop.sub('', dashes.sub('-', header.lower()))
        out += ' ' * (level - 1) + '- [{0}](#{1})\n'.format(header, header_id)
    out += '\n'
    return out


def main(argv):
    for fname in argv[1:]:
        active = False
        with open(fname, 'r+') as f:
            active = True
            in_toc = False
            headers = []
            output = []
            lines = f.readlines()
            for l in lines:
                # Ignore TOC
                if '# Table of Contents' in l:
                    active = False
                elif not active and l.startswith('-'):
                    in_toc = True
                elif in_toc and l.strip() == '':
                    in_toc = False
                    active = True
                # actual header parsing
                elif active:
                    output.append(l)
                    l = l.strip()
                    if l.startswith('#') and ' ' in l:
                        marker, header = l.split(' ', 1)
                        headers.append((header, len(marker)))
            f.seek(0)
            f.write(gentoc(headers))
            f.write(''.join(output))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
