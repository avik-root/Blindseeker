#!/usr/bin/env python3
"""
Blindseeker v1.0.0 — Product Key Generator
============================================
Generates product activation keys with SHA-256 hash encryption.
Appends hashes to .keys/valid_keys.dat for GitHub deployment.

Usage:
    python tools/keygen.py                  # Generate 1 key
    python tools/keygen.py --count 5        # Generate 5 keys
    python tools/keygen.py --count 10 --output keys_export.txt

Developed by MintFire
"""

import hashlib
import random
import string
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# ─── Configuration ───
KEY_SEGMENTS = 5
SEGMENT_LENGTH = 5
KEY_CHARSET = string.ascii_uppercase + string.digits
KEYS_FILE = Path(__file__).parent.parent / '.keys' / 'valid_keys.dat'
ACTIVE_JSON = Path(__file__).parent / 'active.json'


def generate_key():
    """Generate a single product key in XXXXX-XXXXX-XXXXX-XXXXX-XXXXX format."""
    segments = []
    for _ in range(KEY_SEGMENTS):
        segment = ''.join(random.choices(KEY_CHARSET, k=SEGMENT_LENGTH))
        segments.append(segment)
    return '-'.join(segments)


def hash_key(key):
    """SHA-256 hash a product key."""
    return hashlib.sha256(key.encode('utf-8')).hexdigest()


def load_existing_hashes():
    """Load existing hashes from valid_keys.dat."""
    hashes = set()
    if KEYS_FILE.exists():
        with open(KEYS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('['):
                    hashes.add(line)
    return hashes


def save_hashes(new_hashes):
    """Append new hashes to valid_keys.dat."""
    KEYS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if not KEYS_FILE.exists():
        with open(KEYS_FILE, 'w') as f:
            f.write("# Blindseeker Product Key Hashes\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write(f"# Format: SHA-256 hashes (one per line)\n")
            f.write(f"# Total keys: {len(new_hashes)}\n\n")
            for h in new_hashes:
                f.write(h + '\n')
    else:
        # Read existing content
        with open(KEYS_FILE, 'r') as f:
            content = f.read()
        
        # Update total count in header
        existing = load_existing_hashes()
        total = len(existing) + len(new_hashes)
        
        # Append new hashes
        with open(KEYS_FILE, 'a') as f:
            f.write(f"\n# Added: {datetime.now().isoformat()}\n")
            for h in new_hashes:
                f.write(h + '\n')
        
        # Update the total count header
        with open(KEYS_FILE, 'r') as f:
            lines = f.readlines()
        with open(KEYS_FILE, 'w') as f:
            for line in lines:
                if line.startswith('# Total keys:'):
                    f.write(f"# Total keys: {total}\n")
                else:
                    f.write(line)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Blindseeker Product Key Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/keygen.py                  Generate 1 key
  python tools/keygen.py --count 5        Generate 5 keys
  python tools/keygen.py --count 10 -o keys.txt  Export to file
  python tools/keygen.py --no-save        Print only, don't save
        """
    )
    parser.add_argument('--count', '-n', type=int, default=1,
                        help='Number of keys to generate (default: 1)')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='Export keys to a text file')
    parser.add_argument('--no-save', action='store_true',
                        help='Don\'t save hashes to valid_keys.dat')
    parser.add_argument('--json', action='store_true',
                        help='Output in JSON format')
    
    args = parser.parse_args()
    
    existing_hashes = load_existing_hashes()
    generated_keys = []
    new_hashes = []
    
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║          BLINDSEEKER — PRODUCT KEY GENERATOR            ║")
    print("║                  Developed by MintFire                  ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    for i in range(args.count):
        # Generate unique key (not already in valid_keys.dat)
        while True:
            key = generate_key()
            key_hash = hash_key(key)
            if key_hash not in existing_hashes:
                break
        
        existing_hashes.add(key_hash)
        generated_keys.append(key)
        new_hashes.append(key_hash)
        
        print(f"  Key #{i+1}:")
        print(f"    Product Key  : \033[92m{key}\033[0m")
        print(f"    SHA-256 Hash : \033[90m{key_hash}\033[0m")
        print()
    
    # Save hashes to valid_keys.dat
    if not args.no_save:
        save_hashes(new_hashes)
        print(f"  ✓ {len(new_hashes)} hash(es) saved to: {KEYS_FILE}")
        print(f"  ✓ Total keys in database: {len(existing_hashes)}")
        
        # Save to tools/active.json
        active_data = []
        if ACTIVE_JSON.exists():
            try:
                with open(ACTIVE_JSON, 'r') as f:
                    active_data = json.load(f)
            except (json.JSONDecodeError, Exception):
                active_data = []
        
        for key in generated_keys:
            active_data.append({
                'key': key,
                'hash': hash_key(key),
                'generated': datetime.now().isoformat(),
                'status': 'active'
            })
        
        with open(ACTIVE_JSON, 'w') as f:
            json.dump(active_data, f, indent=2)
        
        print(f"  ✓ Keys saved to: {ACTIVE_JSON}")
    else:
        print("  ⚠ Hashes NOT saved (--no-save flag)")
    
    # Export to file
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            f.write(f"# Blindseeker Product Keys\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write(f"# Count: {len(generated_keys)}\n\n")
            for i, key in enumerate(generated_keys):
                f.write(f"Key #{i+1}: {key}\n")
                f.write(f"Hash:    {hash_key(key)}\n\n")
        print(f"  ✓ Keys exported to: {output_path}")
    
    # JSON output
    if args.json:
        output = {
            'generated': datetime.now().isoformat(),
            'count': len(generated_keys),
            'keys': [
                {
                    'key': k,
                    'hash': hash_key(k)
                }
                for k in generated_keys
            ]
        }
        print(f"\n  JSON Output:")
        print(json.dumps(output, indent=2))
    
    print(f"\n  ─────────────────────────────────────────────")
    print(f"  Push .keys/valid_keys.dat to GitHub to activate keys.")
    print(f"  Repo: https://github.com/avik-root/Blindseeker")
    print()


if __name__ == '__main__':
    main()
