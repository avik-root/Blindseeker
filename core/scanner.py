"""
Blindseeker v1.0.0 - Platform Scanner
=======================================
Individual platform scanning with retry logic, response analysis,
and multiple detection methods (status_code, message, redirect, json).
"""

import random
import logging
import asyncio
import aiohttp
from config import Config

logger = logging.getLogger('blindseeker.scanner')


class ScanResult:
    """Represents the result of scanning a single platform."""
    
    def __init__(self, platform, username, found=False, url=None,
                 status_code=None, response_time=None, error=None):
        self.platform = platform
        self.username = username
        self.found = found
        self.url = url
        self.status_code = status_code
        self.response_time = response_time
        self.error = error
        self.category = platform.get('category', 'other')
    
    def to_dict(self):
        return {
            'platform': self.platform.get('name', 'Unknown'),
            'username': self.username,
            'found': self.found,
            'url': self.url,
            'status_code': self.status_code,
            'response_time': self.response_time,
            'error': self.error,
            'category': self.category
        }


class PlatformScanner:
    """Scans individual platforms for username existence."""
    
    def __init__(self, timeout=15, max_retries=2, rate_limiter=None):
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limiter = rate_limiter
    
    def _get_headers(self):
        """Get randomized request headers."""
        ua = random.choice(Config.USER_AGENTS)
        return {
            'User-Agent': ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
    
    async def scan_platform(self, session, platform, username, proxy_url=None):
        """
        Scan a single platform for the given username.
        Returns ScanResult.
        """
        name = platform.get('name', 'Unknown')
        url_template = platform.get('url', '')
        detection = platform.get('detection', 'status_code')
        
        # Build the profile URL
        url = url_template.format(username)
        
        # Rate limit
        if self.rate_limiter:
            self.rate_limiter.acquire(url)
        
        for attempt in range(self.max_retries + 1):
            try:
                start_time = asyncio.get_event_loop().time()
                
                timeout = aiohttp.ClientTimeout(total=self.timeout)
                headers = self._get_headers()
                
                async with session.get(
                    url,
                    headers=headers,
                    timeout=timeout,
                    allow_redirects=True,
                    proxy=proxy_url,
                    ssl=False
                ) as response:
                    end_time = asyncio.get_event_loop().time()
                    response_time = round((end_time - start_time) * 1000)
                    status = response.status
                    
                    # Handle rate limiting
                    if status == 429:
                        if self.rate_limiter:
                            self.rate_limiter.report_throttled(url)
                        if attempt < self.max_retries:
                            await asyncio.sleep(2 ** attempt)
                            continue
                        return ScanResult(
                            platform, username,
                            error='Rate limited (429)',
                            status_code=429,
                            response_time=response_time
                        )
                    
                    body = await response.text(errors='replace')
                    
                    # Detect based on method
                    found = False
                    
                    if detection == 'status_code':
                        expected = platform.get('expected_code', 200)
                        not_found_code = platform.get('not_found_code', 404)
                        found = (status == expected)
                    
                    elif detection == 'message':
                        error_msg = platform.get('error_msg', '')
                        # Found if the error message is NOT in the response
                        found = (error_msg not in body) and (status != 404)
                    
                    elif detection == 'redirect':
                        # Found if there's no redirect (stayed on profile page)
                        found = (str(response.url) == url or username.lower() in str(response.url).lower())
                    
                    elif detection == 'json':
                        try:
                            import json
                            data = json.loads(body)
                            field = platform.get('json_field', 'exists')
                            found = data.get(field, False)
                        except Exception:
                            found = False
                    
                    return ScanResult(
                        platform, username,
                        found=found,
                        url=url if found else None,
                        status_code=status,
                        response_time=response_time
                    )
            
            except asyncio.TimeoutError:
                if attempt < self.max_retries:
                    await asyncio.sleep(1)
                    continue
                return ScanResult(
                    platform, username,
                    error='Timeout',
                    response_time=self.timeout * 1000
                )
            
            except aiohttp.ClientError as e:
                if attempt < self.max_retries:
                    await asyncio.sleep(1)
                    continue
                return ScanResult(
                    platform, username,
                    error=f'Connection error: {str(e)[:50]}'
                )
            
            except Exception as e:
                logger.debug(f"Error scanning {name}: {e}")
                return ScanResult(
                    platform, username,
                    error=f'Error: {str(e)[:50]}'
                )
        
        return ScanResult(platform, username, error='Max retries exceeded')
