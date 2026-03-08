"""
Blindseeker v1.0.0 - Name Parser & Username Generator
=======================================================
Parses full names into first/middle/last and generates
ALL plausible username combinations for maximum coverage.

Developed by MintFire
"""

import re
import itertools


class NameParser:
    """
    Parse full names and generate exhaustive username variants.
    Supports "First Last", "First Middle Last", "Last, First",
    and batch multi-name input.
    """

    # Common separators between names in a batch
    BATCH_SEPARATORS = ['\n', ';', '|']

    # Common suffixes to strip
    SUFFIXES = {'jr', 'sr', 'ii', 'iii', 'iv', 'v', 'phd', 'md', 'esq', 'dds'}

    # Separators to use between name parts
    NAME_SEPARATORS = ['', '.', '_', '-']

    # Common number suffixes for variations
    NUM_SUFFIXES = ['', '1', '01', '123', '007', '99', '00']

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
        Generate ALL plausible username combinations from a parsed name.
        Uses every combination of separators (none, '.', '_', '-')
        between first, last, middle, and initials.
        Returns a sorted list of unique usernames.
        """
        if not parsed:
            return []

        f = parsed['first'].lower().strip()
        l = parsed['last'].lower().strip()
        m_full = parsed['middle'].lower().strip()
        m = m_full.split()[0] if m_full else ''  # first middle name word
        fi = f[0] if f else ''                    # first initial
        li = l[0] if l else ''                    # last initial
        mi = m[0] if m else ''                    # middle initial

        usernames = set()

        # ─── Single parts ───
        if f:
            usernames.add(f)
        if l:
            usernames.add(l)

        # ─── Two-part combos: first + last ───
        if f and l:
            for sep in self.NAME_SEPARATORS:
                # first{sep}last
                usernames.add(f'{f}{sep}{l}')
                # last{sep}first
                usernames.add(f'{l}{sep}{f}')
                # first_initial{sep}last
                usernames.add(f'{fi}{sep}{l}')
                # last{sep}first_initial
                usernames.add(f'{l}{sep}{fi}')
                # first{sep}last_initial
                usernames.add(f'{f}{sep}{li}')
                # last_initial{sep}first
                usernames.add(f'{li}{sep}{f}')

            # With number suffixes on the most common combos
            for num in self.NUM_SUFFIXES:
                if num:
                    usernames.add(f'{f}{l}{num}')
                    usernames.add(f'{f}.{l}{num}')
                    usernames.add(f'{f}_{l}{num}')
                    usernames.add(f'{fi}{l}{num}')

        # ─── Three-part combos: first + middle + last ───
        if f and l and mi:
            for sep in self.NAME_SEPARATORS:
                # first{sep}middle_initial{sep}last
                usernames.add(f'{f}{sep}{mi}{sep}{l}')
                # first_initial{sep}middle_initial{sep}last
                usernames.add(f'{fi}{sep}{mi}{sep}{l}')
                # first{sep}middle_full{sep}last
                usernames.add(f'{f}{sep}{m}{sep}{l}')
                # first{sep}middle_initial
                usernames.add(f'{f}{sep}{mi}')
                # middle{sep}last
                usernames.add(f'{m}{sep}{l}')

            # Special combos
            usernames.add(f'{f}{m}{l}')            # firstmiddlelast
            usernames.add(f'{fi}{mi}{l}')           # fml + last
            usernames.add(f'{fi}{mi}{li}')          # initials

        # ─── Edge cases: single name (no last) ───
        if f and not l:
            for num in self.NUM_SUFFIXES:
                if num:
                    usernames.add(f'{f}{num}')

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
