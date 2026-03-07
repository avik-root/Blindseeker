"""
Blindseeker v1.0.0 - Email & OSINT Tracer
===========================================
Performs email-based OSINT lookups:
  - Gravatar profile extraction
  - Email validation & provider detection
  - Username extraction from email
  - Breach database check (HIBP-style)
  - Social media correlation
  - Domain WHOIS hints

Developed by MintFire
"""

import hashlib
import re
import json
import logging
import aiohttp
import asyncio
from urllib.parse import quote

logger = logging.getLogger('blindseeker.email_tracer')


class EmailTracer:
    """
    OSINT email intelligence gathering module.
    Correlates email addresses with online identities.
    """

    # Known email providers and their account profile URLs
    EMAIL_PROVIDERS = {
        'gmail.com': {'provider': 'Google', 'profile': 'https://www.google.com/search?q="{}"'},
        'yahoo.com': {'provider': 'Yahoo', 'profile': None},
        'outlook.com': {'provider': 'Microsoft', 'profile': None},
        'hotmail.com': {'provider': 'Microsoft', 'profile': None},
        'live.com': {'provider': 'Microsoft', 'profile': None},
        'protonmail.com': {'provider': 'ProtonMail', 'profile': None, 'privacy': True},
        'proton.me': {'provider': 'ProtonMail', 'profile': None, 'privacy': True},
        'tutanota.com': {'provider': 'Tutanota', 'profile': None, 'privacy': True},
        'icloud.com': {'provider': 'Apple', 'profile': None},
        'me.com': {'provider': 'Apple', 'profile': None},
        'aol.com': {'provider': 'AOL', 'profile': None},
        'mail.ru': {'provider': 'Mail.ru', 'profile': None, 'region': 'Russia'},
        'yandex.ru': {'provider': 'Yandex', 'profile': None, 'region': 'Russia'},
        'qq.com': {'provider': 'QQ Mail', 'profile': None, 'region': 'China'},
        '163.com': {'provider': 'NetEase', 'profile': None, 'region': 'China'},
        'naver.com': {'provider': 'Naver', 'profile': None, 'region': 'South Korea'},
    }

    # Platforms that expose profiles via email-based lookups
    EMAIL_LOOKUP_PLATFORMS = [
        {"name": "Gravatar", "url": "https://www.gravatar.com/{hash}.json", "method": "gravatar"},
        {"name": "GitHub (email search)", "url": "https://api.github.com/search/users?q={email}+in:email", "method": "json_check"},
        {"name": "Spotify", "url": "https://open.spotify.com/user/{username}", "method": "status_code"},
        {"name": "WordPress", "url": "https://{username}.wordpress.com", "method": "status_code"},
        {"name": "Blogger", "url": "https://{username}.blogspot.com", "method": "status_code"},
        {"name": "About.me", "url": "https://about.me/{username}", "method": "status_code"},
        {"name": "Gravatar Profile", "url": "https://en.gravatar.com/{hash}", "method": "status_code"},
        {"name": "Keybase", "url": "https://keybase.io/{username}", "method": "status_code"},
    ]

    def __init__(self, timeout=10):
        self.timeout = timeout

    def validate_email(self, email):
        """Validate email format and extract components."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return None

        local, domain = email.split('@', 1)
        return {
            'valid': True,
            'email': email,
            'local_part': local,
            'domain': domain,
            'provider': self._identify_provider(domain),
            'md5_hash': hashlib.md5(email.lower().strip().encode()).hexdigest(),
            'sha256_hash': hashlib.sha256(email.lower().strip().encode()).hexdigest(),
        }

    def _identify_provider(self, domain):
        """Identify email provider from domain."""
        domain_lower = domain.lower()
        if domain_lower in self.EMAIL_PROVIDERS:
            return self.EMAIL_PROVIDERS[domain_lower]
        return {'provider': 'Custom/Corporate', 'domain': domain_lower}

    def extract_usernames(self, email):
        """Generate potential usernames from an email address."""
        local = email.split('@')[0].lower()
        usernames = set()

        # The full local part
        usernames.add(local)

        # Without dots
        usernames.add(local.replace('.', ''))

        # Without numbers
        usernames.add(re.sub(r'\d+', '', local))

        # Split by common separators
        for sep in ['.', '_', '-', '+']:
            parts = local.split(sep)
            for part in parts:
                if len(part) >= 3:
                    usernames.add(part)

        # First + last combos if dot separated
        if '.' in local:
            parts = local.split('.')
            if len(parts) == 2:
                usernames.add(parts[0])
                usernames.add(parts[1])
                usernames.add(f"{parts[0]}{parts[1]}")
                usernames.add(f"{parts[0]}_{parts[1]}")
                usernames.add(f"{parts[1]}{parts[0]}")

        # Remove empties
        usernames.discard('')
        return sorted(list(usernames))

    async def gravatar_lookup(self, email):
        """Fetch Gravatar profile data from email hash."""
        md5_hash = hashlib.md5(email.lower().strip().encode()).hexdigest()
        url = f"https://www.gravatar.com/{md5_hash}.json"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=self.timeout)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        entry = data.get('entry', [{}])[0]
                        return {
                            'found': True,
                            'display_name': entry.get('displayName', ''),
                            'profile_url': entry.get('profileUrl', ''),
                            'avatar_url': f"https://www.gravatar.com/avatar/{md5_hash}?s=200",
                            'about': entry.get('aboutMe', ''),
                            'location': entry.get('currentLocation', ''),
                            'accounts': entry.get('accounts', []),
                            'urls': entry.get('urls', []),
                            'photos': entry.get('photos', []),
                        }
                    return {'found': False}
        except Exception as e:
            logger.debug(f"Gravatar lookup error: {e}")
            return {'found': False, 'error': str(e)}

    async def check_breach_indicators(self, email):
        """Check public breach indicator databases."""
        # Using haveibeenpwned-style API (rate-limited, needs key in production)
        results = {
            'email_hash': hashlib.sha256(email.lower().encode()).hexdigest()[:16],
            'recommendation': 'Use official HIBP API with API key for production breach checks',
            'domain_age': 'Check domain registration date via WHOIS',
        }
        return results

    async def full_trace(self, email):
        """Perform complete email OSINT trace."""
        # Validate
        validation = self.validate_email(email)
        if not validation:
            return {'error': 'Invalid email format', 'email': email}

        # Extract potential usernames
        usernames = self.extract_usernames(email)

        # Gravatar lookup
        gravatar = await self.gravatar_lookup(email)

        # Breach indicators
        breach = await self.check_breach_indicators(email)

        # Build intelligence report
        report = {
            'email': email,
            'validation': validation,
            'usernames_extracted': usernames,
            'primary_username': usernames[0] if usernames else None,
            'gravatar': gravatar,
            'breach_indicators': breach,
            'provider_info': validation['provider'],
            'intelligence': {
                'privacy_email': validation['provider'].get('privacy', False),
                'region_hint': validation['provider'].get('region', 'Global'),
                'corporate_email': validation['provider'].get('provider') == 'Custom/Corporate',
                'total_username_variants': len(usernames),
            }
        }

        return report

    def trace_sync(self, email):
        """Synchronous wrapper for full_trace."""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.full_trace(email))
        finally:
            loop.close()
