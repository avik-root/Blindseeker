"""
Blindseeker v1.0.0 — FuzzyShield Security Module
==================================================
Custom fuzzy logic encryption/decryption for product key licensing.
Implements device fingerprinting, GitHub key verification, and
tamper-resistant local license storage.

Developed by MintFire
"""

import os
import sys
import json
import hashlib
import hmac
import base64
import struct
import time
import uuid
import platform
import getpass
import socket
import secrets
import logging
from pathlib import Path
from datetime import datetime, timezone

logger = logging.getLogger('blindseeker.fuzzyshield')

# ──────────────────────────────────────────────────────────────
# FuzzyShield Encryption Algorithm
# ──────────────────────────────────────────────────────────────

# Custom substitution table (256-byte permutation)
_FUZZY_SBOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]

# Build inverse S-Box
_FUZZY_SBOX_INV = [0] * 256
for _i, _v in enumerate(_FUZZY_SBOX):
    _FUZZY_SBOX_INV[_v] = _i

# Key alphabet for product key generation
_KEY_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # No I,O,0,1 to avoid ambiguity


class FuzzyShield:
    """
    Custom fuzzy logic encryption system for Blindseeker product keys.
    
    Key Format: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX (25 chars, 5 segments)
    
    The "fuzzy" aspect: verification uses Hamming-distance tolerance,
    allowing small variations (e.g. character transposition) while
    still rejecting invalid keys. This prevents brute-force while
    being tolerant of minor input errors.
    """
    
    # Internal cryptographic seed (derived from application identity)
    _MASTER_SEED = b"BlindSeeker::MintFire::FuzzyShield::v1.0.0::ShadowProtocol"
    _LICENSE_FILENAME = ".blindseeker_license"
    _LICENSE_DIR = Path.home()
    
    # GitHub raw URL for key verification (placeholder — user configures)
    GITHUB_KEYS_URL = "https://raw.githubusercontent.com/avik-root/Blindseeker/main/.keys/valid_keys.dat"
    
    def __init__(self):
        self._device_fp = None
        self._round_keys = self._derive_round_keys()
    
    # ──────────────────────────────────────────────
    # Key Generation
    # ──────────────────────────────────────────────
    
    def generate_key(self, user_id: str = "") -> str:
        """Generate a new product key with embedded metadata."""
        # Create entropy from user_id + timestamp + random
        entropy = hashlib.sha256(
            self._MASTER_SEED + 
            user_id.encode('utf-8') + 
            struct.pack('>d', time.time()) +
            secrets.token_bytes(16)
        ).digest()
        
        # Convert to key characters (5 segments of 5 chars)
        segments = []
        for seg_idx in range(5):
            segment = ""
            for char_idx in range(5):
                byte_idx = seg_idx * 5 + char_idx
                # Apply S-Box substitution + positional rotation
                val = entropy[byte_idx % len(entropy)]
                val = _FUZZY_SBOX[val] ^ self._round_keys[seg_idx]
                val = (val + char_idx * 31 + seg_idx * 17) % len(_KEY_ALPHABET)
                segment += _KEY_ALPHABET[val]
            segments.append(segment)
        
        return "-".join(segments)
    
    # ──────────────────────────────────────────────
    # Fuzzy Encryption / Decryption
    # ──────────────────────────────────────────────
    
    def encrypt_key(self, key: str, device_fingerprint: str) -> str:
        """Encrypt a product key with device-specific fuzzy transformation."""
        clean_key = key.replace("-", "").upper()
        
        # Derive device-specific key stream
        device_seed = hashlib.sha256(
            device_fingerprint.encode('utf-8') + self._MASTER_SEED
        ).digest()
        
        # Apply multi-round fuzzy cipher
        encrypted_bytes = bytearray()
        for i, ch in enumerate(clean_key):
            char_val = ord(ch)
            # Round 1: XOR with device stream
            char_val ^= device_seed[i % len(device_seed)]
            # Round 2: S-Box substitution
            char_val = _FUZZY_SBOX[char_val % 256]
            # Round 3: Positional rotation with round key
            char_val = (char_val + self._round_keys[i % 5] + i * 7) % 256
            # Round 4: Secondary XOR with rotated seed
            char_val ^= device_seed[(i + 13) % len(device_seed)]
            encrypted_bytes.append(char_val)
        
        # Add integrity checksum (HMAC-based)
        mac = hmac.new(device_seed[:16], bytes(encrypted_bytes), hashlib.sha256).digest()[:8]
        encrypted_bytes.extend(mac)
        
        return base64.b85encode(bytes(encrypted_bytes)).decode('ascii')
    
    def decrypt_key(self, encrypted: str, device_fingerprint: str) -> str:
        """Decrypt an encrypted product key."""
        try:
            raw = bytearray(base64.b85decode(encrypted.encode('ascii')))
        except Exception:
            return ""
        
        # Split data and MAC
        mac_received = bytes(raw[-8:])
        data = bytearray(raw[:-8])
        
        # Derive device-specific key stream
        device_seed = hashlib.sha256(
            device_fingerprint.encode('utf-8') + self._MASTER_SEED
        ).digest()
        
        # Verify integrity
        mac_computed = hmac.new(device_seed[:16], bytes(data), hashlib.sha256).digest()[:8]
        if not hmac.compare_digest(mac_received, mac_computed):
            return ""
        
        # Reverse the cipher rounds
        decrypted_chars = []
        for i, val in enumerate(data):
            # Reverse Round 4
            val ^= device_seed[(i + 13) % len(device_seed)]
            # Reverse Round 3
            val = (val - self._round_keys[i % 5] - i * 7) % 256
            # Reverse Round 2
            val = _FUZZY_SBOX_INV[val]
            # Reverse Round 1
            val ^= device_seed[i % len(device_seed)]
            decrypted_chars.append(chr(val % 128))
        
        raw_key = "".join(decrypted_chars)
        # Re-format as XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
        if len(raw_key) == 25:
            return "-".join([raw_key[i:i+5] for i in range(0, 25, 5)])
        return raw_key
    
    # ──────────────────────────────────────────────
    # Fuzzy Verification
    # ──────────────────────────────────────────────
    
    def verify_key_fuzzy(self, input_key: str, stored_key: str, threshold: float = 0.88) -> bool:
        """
        Verify a key using fuzzy Hamming-distance matching.
        
        This is the core "fuzzy logic" — instead of exact string match,
        we compute similarity and accept if above threshold. This makes
        the system resistant to brute-force (need to match ~88% of chars)
        while tolerating minor typos.
        """
        clean_input = input_key.replace("-", "").upper().strip()
        clean_stored = stored_key.replace("-", "").upper().strip()
        
        if len(clean_input) != len(clean_stored):
            return False
        
        if len(clean_input) == 0:
            return False
        
        # Hamming distance with weighted positions
        matches = 0
        total_weight = 0
        for i, (c1, c2) in enumerate(zip(clean_input, clean_stored)):
            # Position-based weight: middle segments have higher weight
            segment_idx = i // 5
            weight = 1.0 + (0.2 if segment_idx in [1, 2, 3] else 0.0)
            total_weight += weight
            if c1 == c2:
                matches += weight
            elif abs(ord(c1) - ord(c2)) <= 1:
                # Adjacent character gets partial credit (fuzzy tolerance)
                matches += weight * 0.3
        
        similarity = matches / total_weight if total_weight > 0 else 0
        return similarity >= threshold
    
    def validate_key_format(self, key: str) -> bool:
        """Check if key matches expected format."""
        parts = key.strip().upper().split("-")
        if len(parts) != 5:
            return False
        for part in parts:
            if len(part) != 5:
                return False
            if not all(c in _KEY_ALPHABET for c in part):
                return False
        return True
    
    # ──────────────────────────────────────────────
    # Device Fingerprinting
    # ──────────────────────────────────────────────
    
    def get_device_fingerprint(self) -> str:
        """
        Generate a unique device fingerprint from system information.
        Captures kernel, hostname, username, MAC, CPU to prevent piracy.
        """
        if self._device_fp:
            return self._device_fp
        
        components = []
        
        # Kernel / OS information
        components.append(f"os:{platform.system()}")
        components.append(f"kernel:{platform.release()}")
        components.append(f"arch:{platform.machine()}")
        
        # Hostname
        components.append(f"host:{socket.gethostname()}")
        
        # Username
        try:
            components.append(f"user:{getpass.getuser()}")
        except Exception:
            components.append("user:unknown")
        
        # MAC address
        mac = uuid.getnode()
        mac_str = ':'.join(f'{(mac >> (8 * i)) & 0xFF:02x}' for i in reversed(range(6)))
        components.append(f"mac:{mac_str}")
        
        # CPU identifier
        components.append(f"cpu:{platform.processor()}")
        
        # Python version (minor component)
        components.append(f"py:{platform.python_version()}")
        
        # Create deterministic fingerprint hash
        fp_string = "|".join(sorted(components))
        fp_hash = hashlib.sha256(
            fp_string.encode('utf-8') + self._MASTER_SEED
        ).hexdigest()
        
        self._device_fp = fp_hash
        return fp_hash
    
    # ──────────────────────────────────────────────
    # License Persistence
    # ──────────────────────────────────────────────
    
    def _get_license_path(self) -> Path:
        """Get the hidden license file path."""
        return self._LICENSE_DIR / self._LICENSE_FILENAME
    
    def save_license(self, key: str) -> bool:
        """
        Save activated license to a hidden file with device-bound encryption.
        Uses a secondary unpredictable fuzzy layer so updates don't lose the key.
        """
        try:
            fingerprint = self.get_device_fingerprint()
            
            # Encrypt key with device fingerprint
            encrypted_key = self.encrypt_key(key, fingerprint)
            
            # Build license data with device binding
            license_data = {
                "v": 1,
                "k": encrypted_key,
                "fp": hashlib.sha256(fingerprint.encode()).hexdigest()[:32],
                "ts": datetime.now(timezone.utc).isoformat(),
                "host": socket.gethostname(),
                "user": getpass.getuser(),
                "os": platform.system(),
                "arch": platform.machine(),
            }
            
            # Serialize and apply secondary obfuscation layer
            raw_json = json.dumps(license_data, separators=(',', ':'))
            
            # Secondary fuzzy obfuscation: XOR with rotating seed derived from fingerprint
            obfuscation_seed = hashlib.sha512(
                fingerprint.encode() + b"::secondary::layer"
            ).digest()
            
            obfuscated = bytearray()
            for i, b in enumerate(raw_json.encode('utf-8')):
                obfuscated.append(b ^ obfuscation_seed[i % len(obfuscation_seed)])
            
            # Add a header magic + version byte
            final = b'\x42\x53\x4b\x01' + bytes(obfuscated)  # BSK\x01
            
            # Write to hidden file
            license_path = self._get_license_path()
            with open(license_path, 'wb') as f:
                f.write(base64.b85encode(final))
            
            # Set file permissions (hide on Unix)
            if platform.system() != 'Windows':
                os.chmod(str(license_path), 0o600)
            
            logger.info(f"License saved to {license_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save license: {e}")
            return False
    
    def load_license(self) -> dict:
        """
        Load and validate a saved license.
        Returns dict with 'valid', 'key', 'expired' etc.
        """
        result = {
            "valid": False, 
            "key": "", 
            "error": "",
            "device_match": False,
            "timestamp": ""
        }
        
        license_path = self._get_license_path()
        if not license_path.exists():
            result["error"] = "No license file found"
            return result
        
        try:
            with open(license_path, 'rb') as f:
                encoded = f.read()
            
            raw = base64.b85decode(encoded)
            
            # Check magic header
            if raw[:4] != b'\x42\x53\x4b\x01':
                result["error"] = "Invalid license file format"
                return result
            
            obfuscated = bytearray(raw[4:])
            
            # Reverse secondary obfuscation
            fingerprint = self.get_device_fingerprint()
            obfuscation_seed = hashlib.sha512(
                fingerprint.encode() + b"::secondary::layer"
            ).digest()
            
            decrypted_json = bytearray()
            for i, b in enumerate(obfuscated):
                decrypted_json.append(b ^ obfuscation_seed[i % len(obfuscation_seed)])
            
            license_data = json.loads(bytes(decrypted_json).decode('utf-8'))
            
            # Verify device fingerprint match
            stored_fp_hash = license_data.get("fp", "")
            current_fp_hash = hashlib.sha256(fingerprint.encode()).hexdigest()[:32]
            
            if stored_fp_hash != current_fp_hash:
                result["error"] = "Device fingerprint mismatch — license bound to another device"
                return result
            
            result["device_match"] = True
            
            # Decrypt the key
            encrypted_key = license_data.get("k", "")
            decrypted_key = self.decrypt_key(encrypted_key, fingerprint)
            
            if not decrypted_key or not self.validate_key_format(decrypted_key):
                result["error"] = "License key decryption failed"
                return result
            
            result["valid"] = True
            result["key"] = decrypted_key
            result["timestamp"] = license_data.get("ts", "")
            
            return result
            
        except json.JSONDecodeError:
            result["error"] = "License file corrupted or from different device"
            return result
        except Exception as e:
            result["error"] = f"License validation error: {str(e)}"
            return result
    
    # ──────────────────────────────────────────────
    # GitHub Verification
    # ──────────────────────────────────────────────
    
    def verify_against_github(self, key: str) -> dict:
        """
        Verify product key against GitHub-hosted keyfile.
        Uses fuzzy matching to check if any stored key matches.
        Returns: {'valid': bool, 'matched': bool, 'error': str}
        """
        import urllib.request
        
        result = {"valid": False, "matched": False, "error": ""}
        
        try:
            # Fetch keys from GitHub
            req = urllib.request.Request(
                self.GITHUB_KEYS_URL,
                headers={"User-Agent": "Blindseeker/1.0.0"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8').strip()
            
            if not content:
                result["error"] = "Empty keyfile from server"
                return result
            
            # Parse lines — each line is an encrypted valid key hash
            valid_hashes = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
            
            # Hash the input key for comparison
            clean_key = key.replace("-", "").upper().strip()
            key_hash = hashlib.sha256(
                clean_key.encode('utf-8') + self._MASTER_SEED
            ).hexdigest()
            
            # Check for match (exact hash or fuzzy string match)
            for stored_hash in valid_hashes:
                stored_hash = stored_hash.strip()
                
                # Direct hash match
                if key_hash == stored_hash:
                    result["valid"] = True
                    result["matched"] = True
                    return result
                
                # Fuzzy hash prefix match (first 48 chars of 64-char hash)
                if key_hash[:48] == stored_hash[:48]:
                    result["valid"] = True
                    result["matched"] = True
                    return result
            
            result["error"] = "Key not found in authorized keyfile"
            return result
            
        except urllib.error.URLError as e:
            # If can't reach GitHub, allow offline activation with format validation
            logger.warning(f"Cannot reach GitHub for verification: {e}")
            result["error"] = f"offline"
            # In offline mode, accept keys with valid format 
            if self.validate_key_format(key):
                result["valid"] = True
                result["matched"] = False
            return result
            
        except Exception as e:
            result["error"] = f"Verification error: {str(e)}"
            return result
    
    # ──────────────────────────────────────────────
    # Full Activation Flow
    # ──────────────────────────────────────────────
    
    def activate(self, key: str) -> dict:
        """
        Complete activation flow:
        1. Validate format
        2. Verify against GitHub
        3. Save to device-bound license file
        """
        result = {
            "success": False,
            "message": "",
            "key": key,
            "device_fingerprint": self.get_device_fingerprint()[:16] + "..."
        }
        
        # Step 1: Format validation
        if not self.validate_key_format(key):
            result["message"] = "Invalid key format. Expected: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX"
            return result
        
        # Step 2: GitHub verification
        github_result = self.verify_against_github(key)
        if not github_result["valid"]:
            result["message"] = f"Key verification failed: {github_result['error']}"
            return result
        
        # Step 3: Save license
        if not self.save_license(key):
            result["message"] = "Failed to save license to device"
            return result
        
        result["success"] = True
        if github_result.get("matched"):
            result["message"] = "Product key verified and activated successfully"
        else:
            result["message"] = "Product key activated (offline mode — will verify on next connection)"
        
        return result
    
    def is_activated(self) -> bool:
        """Quick check if a valid license exists."""
        license_info = self.load_license()
        return license_info.get("valid", False)
    
    # ──────────────────────────────────────────────
    # Internal Helpers
    # ──────────────────────────────────────────────
    
    def _derive_round_keys(self) -> list:
        """Derive 5 round keys from master seed for the fuzzy cipher."""
        seed_hash = hashlib.sha256(self._MASTER_SEED).digest()
        return [seed_hash[i * 4] for i in range(5)]
    
    def get_activation_info(self) -> dict:
        """Get current activation status and device info."""
        license_info = self.load_license()
        return {
            "activated": license_info.get("valid", False),
            "activation_date": license_info.get("timestamp", ""),
            "device_fingerprint": self.get_device_fingerprint()[:16] + "...",
            "hostname": socket.gethostname(),
            "username": getpass.getuser(),
            "os": f"{platform.system()} {platform.release()}",
            "arch": platform.machine(),
            "error": license_info.get("error", "")
        }


# ──────────────────────────────────────────────────────────────
# Key Generation Utility (for admin use)
# ──────────────────────────────────────────────────────────────

def generate_keys(count: int = 5) -> list:
    """Generate multiple product keys for distribution."""
    shield = FuzzyShield()
    keys = []
    for i in range(count):
        key = shield.generate_key(f"user_{i}_{secrets.token_hex(4)}")
        # Also compute the hash for storing in GitHub keyfile
        clean_key = key.replace("-", "").upper()
        key_hash = hashlib.sha256(
            clean_key.encode('utf-8') + shield._MASTER_SEED
        ).hexdigest()
        keys.append({"key": key, "hash": key_hash})
    return keys


if __name__ == "__main__":
    # Admin utility: generate keys
    print("=" * 60)
    print("  FuzzyShield Key Generator — Blindseeker v1.0.0")
    print("=" * 60)
    keys = generate_keys(5)
    print("\nGenerated Product Keys:")
    print("-" * 60)
    for i, k in enumerate(keys, 1):
        print(f"  Key {i}: {k['key']}")
        print(f"  Hash:  {k['hash']}")
        print()
    
    print("Add the hashes to your GitHub valid_keys.dat file.")
    print("=" * 60)
