"""
Blindseeker v1.0.0 - Tor Integration
======================================
SOCKS5 proxy integration via Tor for anonymous scanning.
Supports circuit renewal via stem controller.
"""

import logging
import requests

logger = logging.getLogger('blindseeker.tor')


class TorManager:
    """Manages Tor SOCKS5 proxy connections and circuit renewal."""
    
    def __init__(self, socks_host='127.0.0.1', socks_port=9050,
                 control_port=9051, control_password=''):
        self.socks_host = socks_host
        self.socks_port = socks_port
        self.control_port = control_port
        self.control_password = control_password
        self.enabled = False
        self.connected = False
        self._current_ip = None
    
    def get_proxy(self):
        """Get Tor SOCKS5 proxy dict for requests."""
        proxy_url = f"socks5h://{self.socks_host}:{self.socks_port}"
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def get_proxy_url(self):
        """Get Tor proxy URL string for aiohttp-socks."""
        return f"socks5://{self.socks_host}:{self.socks_port}"
    
    def check_connection(self):
        """Verify Tor connection is working."""
        try:
            proxies = self.get_proxy()
            resp = requests.get(
                'https://check.torproject.org/api/ip',
                proxies=proxies,
                timeout=15
            )
            
            if resp.status_code == 200:
                data = resp.json()
                self.connected = data.get('IsTor', False)
                self._current_ip = data.get('IP', 'Unknown')
                
                if self.connected:
                    logger.info(f"Tor connected. Exit IP: {self._current_ip}")
                else:
                    logger.warning("Connected but not through Tor network")
                
                return self.connected
            
            return False
        except Exception as e:
            logger.error(f"Tor connection check failed: {e}")
            self.connected = False
            return False
    
    def renew_circuit(self):
        """Request a new Tor circuit for a new exit IP."""
        try:
            from stem import Signal
            from stem.control import Controller
            
            with Controller.from_port(port=self.control_port) as controller:
                if self.control_password:
                    controller.authenticate(password=self.control_password)
                else:
                    controller.authenticate()
                
                controller.signal(Signal.NEWNYM)
                logger.info("Tor circuit renewed successfully")
                
                # Update current IP
                import time
                time.sleep(3)  # Wait for new circuit
                self.check_connection()
                
                return True
        except ImportError:
            logger.warning("stem library not available. Cannot renew Tor circuit.")
            return False
        except Exception as e:
            logger.error(f"Failed to renew Tor circuit: {e}")
            return False
    
    def enable(self):
        """Enable Tor and verify connection."""
        self.enabled = True
        connected = self.check_connection()
        if not connected:
            logger.warning("Tor enabled but connection verification failed. "
                         "Ensure Tor service is running on "
                         f"{self.socks_host}:{self.socks_port}")
        return connected
    
    def disable(self):
        """Disable Tor."""
        self.enabled = False
        self.connected = False
        self._current_ip = None
        logger.info("Tor disabled")
    
    def get_status(self):
        """Get Tor connection status."""
        return {
            'enabled': self.enabled,
            'connected': self.connected,
            'exit_ip': self._current_ip,
            'socks_host': self.socks_host,
            'socks_port': self.socks_port
        }
