"""
Blindseeker v1.0.0 - Name Parser & Username Generator
=======================================================
Parses full names into first/middle/last and generates
all plausible username variants for enumeration.

Developed by MintFire
"""

import re
import itertools


class NameParser:
    """
    Parse full names and generate username variants.
    Supports "First Last", "First Middle Last", "Last, First",
    and batch multi-name input.
    """

    # Common separators between names in a batch
    BATCH_SEPARATORS = ['\n', ';', '|']

    # Common suffixes to strip
    SUFFIXES = {'jr', 'sr', 'ii', 'iii', 'iv', 'v', 'phd', 'md', 'esq', 'dds'}

    def parse_name(self, full_name):
        """
        Parse a full name string into components.
        Returns dict with first, middle, last, and the original.
        """
        name = full_name.strip()
        if not name:
            return None

        # Remove extra whitespace
        name = re.sub(r'\s+', ' ', name)

        # Handle "Last, First Middle" format
        if ',' in name:
            parts = [p.strip() for p in name.split(',', 1)]
            last = parts[0]
            rest = parts[1].split() if len(parts) > 1 else []
            first = rest[0] if rest else ''
            middle = ' '.join(rest[1:]) if len(rest) > 1 else ''
        else:
            parts = name.split()
            # Filter out suffixes
            parts = [p for p in parts if p.lower().rstrip('.') not in self.SUFFIXES]

            if len(parts) == 1:
                first = parts[0]
                middle = ''
                last = ''
            elif len(parts) == 2:
                first = parts[0]
                middle = ''
                last = parts[1]
            else:
                first = parts[0]
                last = parts[-1]
                middle = ' '.join(parts[1:-1])

        return {
            'original': full_name.strip(),
            'first': first,
            'middle': middle,
            'last': last,
            'has_middle': bool(middle),
        }

    def generate_usernames(self, parsed):
        """
        Generate all plausible username variants from a parsed name.
        Returns a sorted list of unique usernames.
        """
        if not parsed:
            return []

        f = parsed['first'].lower()
        l = parsed['last'].lower()
        m = parsed['middle'].lower().split()[0] if parsed['middle'] else ''
        mi = m[0] if m else ''  # middle initial

        usernames = set()

        if f:
            usernames.add(f)
        if l:
            usernames.add(l)

        if f and l:
            # Common patterns
            usernames.add(f'{f}{l}')           # johnsmith
            usernames.add(f'{f}.{l}')          # john.smith
            usernames.add(f'{f}_{l}')          # john_smith
            usernames.add(f'{f}-{l}')          # john-smith
            usernames.add(f'{l}{f}')           # smithjohn
            usernames.add(f'{f[0]}{l}')        # jsmith
            usernames.add(f'{f}{l[0]}')        # johns
            usernames.add(f'{l}{f[0]}')        # smithj
            usernames.add(f'{f[0]}.{l}')       # j.smith
            usernames.add(f'{f[0]}_{l}')       # j_smith

            if mi:
                usernames.add(f'{f}{mi}{l}')       # johnmsmith
                usernames.add(f'{f}.{mi}.{l}')     # john.m.smith
                usernames.add(f'{f}_{mi}_{l}')     # john_m_smith
                usernames.add(f'{f[0]}{mi}{l}')    # jmsmith
                usernames.add(f'{f}{m}{l}')        # johnmichaelsmith
                usernames.add(f'{f}.{m}.{l}')      # john.michael.smith
                usernames.add(f'{f}_{m}_{l}')      # john_michael_smith
                usernames.add(f'{f}{m}')            # johnmichael

        # Remove empties and single-char
        usernames = {u for u in usernames if len(u) >= 2}
        return sorted(list(usernames))

    def parse_batch(self, text):
        """
        Parse a batch of names from a text block.
        Auto-detects names separated by newlines, semicolons, or pipes.
        Returns a list of parsed name dicts with generated usernames.
        """
        if not text or not text.strip():
            return []

        # Split by any separator
        lines = re.split(r'[\n;|]+', text)
        results = []

        for line in lines:
            line = line.strip()
            if not line or len(line) < 2:
                continue

            parsed = self.parse_name(line)
            if parsed:
                parsed['usernames'] = self.generate_usernames(parsed)
                results.append(parsed)

        return results

    def get_all_usernames(self, text):
        """
        Parse batch text and return a flat unique list of all usernames.
        """
        batch = self.parse_batch(text)
        all_usernames = set()
        for entry in batch:
            all_usernames.update(entry.get('usernames', []))
        return sorted(list(all_usernames))
