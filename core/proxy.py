"""
Blindseeker v1.0.0 - Proxy Manager
====================================
Supports HTTP/HTTPS/SOCKS4/SOCKS5 proxies with rotation and health checking.
"""

import random
import threading
import time
import requests
import logging

logger = logging.getLogger('blindseeker.proxy')


class ProxyManager:
    """Manages proxy rotation, health checking, and load balancing."""
    
    def __init__(self):
        self.proxies = []
        self.healthy_proxies = []
        self.dead_proxies = []
        self.current_index = 0
        self.lock = threading.Lock()
        self.enabled = False
        self.rotation_mode = 'round_robin'  # 'round_robin' or 'random'
        self._health_check_interval = 300  # 5 minutes
    
    def load_from_file(self, filepath):
        """
        Load proxies from a file.
        Format per line: protocol://host:port or host:port
        """
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            count = 0
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                proxy = self._parse_proxy(line)
                if proxy:
                    self.proxies.append(proxy)
                    self.healthy_proxies.append(proxy)
                    count += 1
            
            if count > 0:
                self.enabled = True
                logger.info(f"Loaded {count} proxies from {filepath}")
            
            return count
        except FileNotFoundError:
            logger.warning(f"Proxy file not found: {filepath}")
            return 0
        except Exception as e:
            logger.error(f"Error loading proxies: {e}")
            return 0
    
    def load_from_list(self, proxy_list):
        """Load proxies from a list of strings."""
        count = 0
        for proxy_str in proxy_list:
            proxy = self._parse_proxy(proxy_str.strip())
            if proxy:
                self.proxies.append(proxy)
                self.healthy_proxies.append(proxy)
                count += 1
        
        if count > 0:
            self.enabled = True
        
        return count
    
    def _parse_proxy(self, proxy_str):
        """Parse a proxy string into a proxy dict."""
        if not proxy_str:
            return None
        
        # Detect protocol
        if '://' in proxy_str:
            protocol, address = proxy_str.split('://', 1)
        else:
            protocol = 'http'
            address = proxy_str
        
        protocol = protocol.lower()
        
        # Build proxy dict for requests
        if protocol in ('socks4', 'socks5', 'socks5h'):
            proxy_url = f"{protocol}://{address}"
        else:
            proxy_url = f"{protocol}://{address}"
        
        return {
            'url': proxy_url,
            'protocol': protocol,
            'address': address,
            'http': proxy_url,
            'https': proxy_url,
            'failures': 0,
            'last_check': 0
        }
    
    def get_proxy(self):
        """Get the next proxy for use."""
        if not self.enabled or not self.healthy_proxies:
            return None
        
        with self.lock:
            if self.rotation_mode == 'random':
                proxy = random.choice(self.healthy_proxies)
            else:
                # Round robin
                self.current_index = self.current_index % len(self.healthy_proxies)
                proxy = self.healthy_proxies[self.current_index]
                self.current_index += 1
            
            return {
                'http': proxy['http'],
                'https': proxy['https']
            }
    
    def get_proxy_url(self):
        """Get proxy URL string for aiohttp."""
        if not self.enabled or not self.healthy_proxies:
            return None
        
        with self.lock:
            if self.rotation_mode == 'random':
                proxy = random.choice(self.healthy_proxies)
            else:
                self.current_index = self.current_index % len(self.healthy_proxies)
                proxy = self.healthy_proxies[self.current_index]
                self.current_index += 1
            
            return proxy['url']
    
    def report_failure(self, proxy_url):
        """Report a proxy failure."""
        with self.lock:
            for proxy in self.healthy_proxies:
                if proxy['url'] == proxy_url or proxy['http'] == proxy_url:
                    proxy['failures'] += 1
                    if proxy['failures'] >= 3:
                        self.healthy_proxies.remove(proxy)
                        self.dead_proxies.append(proxy)
                        logger.warning(f"Proxy marked dead: {proxy['url']}")
                    break
    
    def report_success(self, proxy_url):
        """Report a proxy success (resets failure count)."""
        with self.lock:
            for proxy in self.healthy_proxies:
                if proxy['url'] == proxy_url or proxy['http'] == proxy_url:
                    proxy['failures'] = 0
                    break
    
    def check_health(self, proxy):
        """Check if a proxy is healthy."""
        try:
            test_url = 'https://httpbin.org/ip'
            proxies = {'http': proxy['http'], 'https': proxy['https']}
            resp = requests.get(test_url, proxies=proxies, timeout=10)
            return resp.status_code == 200
        except Exception:
            return False
    
    def get_status(self):
        """Get proxy manager status."""
        return {
            'enabled': self.enabled,
            'total': len(self.proxies),
            'healthy': len(self.healthy_proxies),
            'dead': len(self.dead_proxies),
            'rotation_mode': self.rotation_mode
        }
    
    def reset(self):
        """Reset all proxies to healthy state."""
        with self.lock:
            for proxy in self.dead_proxies:
                proxy['failures'] = 0
                self.healthy_proxies.append(proxy)
            self.dead_proxies.clear()
            self.current_index = 0
