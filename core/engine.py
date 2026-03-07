"""
Blindseeker v1.0.0 - Main Enumeration Engine
===============================================
Orchestrates concurrent platform scanning with proxy/Tor support,
real-time progress callbacks, and result aggregation.
"""

import asyncio
import time
import logging
import threading
from datetime import datetime, timezone

import aiohttp

from core.platforms import PLATFORMS, get_platforms, get_platform_count, get_categories
from core.scanner import PlatformScanner
from core.proxy import ProxyManager
from core.tor import TorManager
from core.rate_limiter import RateLimiter

logger = logging.getLogger('blindseeker.engine')


class ScanSession:
    """Represents a single scan session with metadata."""
    
    def __init__(self, username, scan_id=None):
        self.username = username
        self.scan_id = scan_id or f"scan_{int(time.time())}_{username}"
        self.start_time = None
        self.end_time = None
        self.results = []
        self.found = []
        self.not_found = []
        self.errors = []
        self.total_platforms = 0
        self.scanned = 0
        self.status = 'pending'  # pending, running, completed, cancelled
        self.categories_scanned = set()
    
    def to_dict(self):
        duration = 0
        if self.start_time and self.end_time:
            duration = round(self.end_time - self.start_time, 2)
        elif self.start_time:
            duration = round(time.time() - self.start_time, 2)
        
        all_results = [r.to_dict() for r in self.results]
        
        return {
            'scan_id': self.scan_id,
            'username': self.username,
            'status': self.status,
            'start_time': datetime.fromtimestamp(self.start_time, tz=timezone.utc).isoformat() if self.start_time else None,
            'end_time': datetime.fromtimestamp(self.end_time, tz=timezone.utc).isoformat() if self.end_time else None,
            'duration_seconds': duration,
            'total_platforms': self.total_platforms,
            'scanned': self.scanned,
            'found_count': len(self.found),
            'not_found_count': len(self.not_found),
            'error_count': len(self.errors),
            'found': [r.to_dict() for r in self.found],
            'not_found': [r.to_dict() for r in self.not_found],
            'errors': [r.to_dict() for r in self.errors],
            'results': all_results,
            'categories': list(self.categories_scanned),
            'progress_percent': round((self.scanned / self.total_platforms * 100), 1) if self.total_platforms > 0 else 0
        }


class BlindSeekerEngine:
    """Main engine orchestrating username enumeration."""
    
    def __init__(self, config=None):
        from config import Config
        self.config = config or Config()
        
        # Components
        self.proxy_manager = ProxyManager()
        self.tor_manager = TorManager(
            socks_host=self.config.TOR_SOCKS_HOST,
            socks_port=self.config.TOR_SOCKS_PORT,
            control_port=self.config.TOR_CONTROL_PORT,
            control_password=self.config.TOR_CONTROL_PASSWORD
        )
        self.rate_limiter = RateLimiter(
            default_rate=self.config.RATE_LIMIT_PER_SECOND,
            default_burst=self.config.RATE_LIMIT_PER_SECOND * 2
        )
        
        # State
        self.scan_history = []
        self.active_scans = {}
        self._lock = threading.Lock()
    
    def configure_proxy(self, proxy_file=None, proxy_list=None):
        """Configure proxy manager."""
        if proxy_file:
            count = self.proxy_manager.load_from_file(proxy_file)
            logger.info(f"Loaded {count} proxies from file")
        elif proxy_list:
            count = self.proxy_manager.load_from_list(proxy_list)
            logger.info(f"Loaded {count} proxies from list")
    
    def configure_tor(self, enable=True):
        """Enable/disable Tor."""
        if enable:
            connected = self.tor_manager.enable()
            return connected
        else:
            self.tor_manager.disable()
            return True
    
    def _get_proxy_url(self):
        """Get proxy URL (Tor takes priority over regular proxies)."""
        if self.tor_manager.enabled:
            return self.tor_manager.get_proxy_url()
        elif self.proxy_manager.enabled:
            return self.proxy_manager.get_proxy_url()
        return None
    
    async def _scan_worker(self, session, scanner, platform, username,
                           proxy_url, progress_callback=None):
        """Worker coroutine for scanning a single platform."""
        result = await scanner.scan_platform(session, platform, username, proxy_url)
        
        if progress_callback:
            try:
                progress_callback(result)
            except Exception as e:
                logger.debug(f"Progress callback error: {e}")
        
        return result
    
    async def _run_scan(self, username, categories=None, timeout=None,
                        max_workers=None, progress_callback=None):
        """Internal async scan runner."""
        timeout = timeout or self.config.REQUEST_TIMEOUT
        max_workers = max_workers or self.config.MAX_WORKERS
        
        # Get platforms
        platforms = get_platforms(categories)
        
        # Create scan session
        scan_session = ScanSession(username)
        scan_session.total_platforms = len(platforms)
        scan_session.start_time = time.time()
        scan_session.status = 'running'
        
        with self._lock:
            self.active_scans[scan_session.scan_id] = scan_session
        
        # Create scanner
        scanner = PlatformScanner(
            timeout=timeout,
            max_retries=self.config.MAX_RETRIES,
            rate_limiter=self.rate_limiter
        )
        
        proxy_url = self._get_proxy_url()
        
        # Create connector with connection limits
        connector = aiohttp.TCPConnector(
            limit=max_workers,
            limit_per_host=3,
            ttl_dns_cache=300,
            ssl=False
        )
        
        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                # Create semaphore to limit concurrency
                sem = asyncio.Semaphore(max_workers)
                
                async def bounded_scan(platform):
                    async with sem:
                        if scan_session.status == 'cancelled':
                            return None
                        
                        result = await self._scan_worker(
                            session, scanner, platform, username,
                            proxy_url, progress_callback
                        )
                        
                        # Update session
                        scan_session.scanned += 1
                        scan_session.results.append(result)
                        scan_session.categories_scanned.add(
                            platform.get('category', 'other')
                        )
                        
                        if result.found:
                            scan_session.found.append(result)
                        elif result.error:
                            scan_session.errors.append(result)
                        else:
                            scan_session.not_found.append(result)
                        
                        return result
                
                # Launch all tasks
                tasks = [bounded_scan(p) for p in platforms]
                await asyncio.gather(*tasks, return_exceptions=True)
        
        except Exception as e:
            logger.error(f"Scan error: {e}")
        
        finally:
            scan_session.end_time = time.time()
            scan_session.status = 'completed'
            
            with self._lock:
                self.scan_history.append(scan_session)
                if scan_session.scan_id in self.active_scans:
                    del self.active_scans[scan_session.scan_id]
        
        return scan_session
    
    def scan(self, username, categories=None, timeout=None,
             max_workers=None, progress_callback=None):
        """
        Synchronous scan entry point.
        Runs the async scan in a new event loop.
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self._run_scan(username, categories, timeout,
                              max_workers, progress_callback)
            )
            return result
        finally:
            loop.close()
    
    def scan_async(self, username, categories=None, timeout=None,
                   max_workers=None, progress_callback=None):
        """
        Start async scan in background thread.
        Returns scan_id immediately.
        """
        scan_id = f"scan_{int(time.time())}_{username}"
        
        def run_in_thread():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(
                    self._run_scan(username, categories, timeout,
                                  max_workers, progress_callback)
                )
            finally:
                loop.close()
        
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
        
        return scan_id
    
    def cancel_scan(self, scan_id):
        """Cancel an active scan."""
        with self._lock:
            if scan_id in self.active_scans:
                self.active_scans[scan_id].status = 'cancelled'
                return True
        return False
    
    def get_scan_status(self, scan_id):
        """Get status of a scan."""
        with self._lock:
            if scan_id in self.active_scans:
                return self.active_scans[scan_id].to_dict()
        
        for session in reversed(self.scan_history):
            if session.scan_id == scan_id:
                return session.to_dict()
        
        return None
    
    def get_history(self, limit=50):
        """Get scan history."""
        return [s.to_dict() for s in reversed(self.scan_history[-limit:])]
    
    def get_stats(self):
        """Get engine statistics."""
        total_scans = len(self.scan_history)
        total_found = sum(len(s.found) for s in self.scan_history)
        
        return {
            'total_scans': total_scans,
            'total_found': total_found,
            'active_scans': len(self.active_scans),
            'platform_count': get_platform_count(),
            'categories': get_categories(),
            'proxy_status': self.proxy_manager.get_status(),
            'tor_status': self.tor_manager.get_status(),
        }
