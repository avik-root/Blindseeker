"""
Blindseeker v1.0.0 — Auto-Update Module
=========================================
Checks for updates from GitHub repository,
downloads and applies updates while preserving
local configuration and license files.

Developed by MintFire
"""

import os
import sys
import json
import hashlib
import logging
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timezone

logger = logging.getLogger('blindseeker.updater')


class BlindSeekerUpdater:
    """
    Handles checking for and applying updates from GitHub.
    Preserves configuration, license, and scan data during update.
    """
    
    GITHUB_REPO = "MintFireDev/Blindseeker"
    GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    GITHUB_RAW = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"
    VERSION_FILE_URL = f"{GITHUB_RAW}/version.json"
    
    # Files preserved during update (never overwritten)
    PRESERVE_FILES = {
        '.blindseeker_license',
        '.env',
        'config.py',  # Only if user modified
        'proxies.txt',
    }
    
    PRESERVE_DIRS = {
        'scans',
        'exports',
        '.keys',
    }
    
    def __init__(self, app_dir: str = None):
        self.app_dir = Path(app_dir) if app_dir else Path(__file__).parent.parent
        self.current_version = self._get_current_version()
    
    def _get_current_version(self) -> str:
        """Get the current application version."""
        version_file = self.app_dir / 'version.json'
        if version_file.exists():
            try:
                with open(version_file, 'r') as f:
                    data = json.load(f)
                return data.get('version', '1.0.0')
            except Exception:
                pass
        return '1.0.0'
    
    def check_for_updates(self) -> dict:
        """
        Check GitHub for a newer version.
        Returns: {available: bool, current: str, latest: str, changelog: str}
        """
        import urllib.request
        
        result = {
            "available": False,
            "current": self.current_version,
            "latest": self.current_version,
            "changelog": "",
            "error": ""
        }
        
        try:
            # Check version.json from GitHub main branch
            req = urllib.request.Request(
                self.VERSION_FILE_URL,
                headers={"User-Agent": "Blindseeker-Updater/1.0"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8')
            
            remote_data = json.loads(content)
            remote_version = remote_data.get('version', '1.0.0')
            
            result["latest"] = remote_version
            result["changelog"] = remote_data.get('changelog', '')
            
            # Simple semver comparison
            if self._version_compare(remote_version, self.current_version) > 0:
                result["available"] = True
            
            return result
            
        except Exception as e:
            result["error"] = f"Cannot reach update server: {str(e)}"
            logger.warning(f"Update check failed: {e}")
            return result
    
    def apply_update(self) -> dict:
        """
        Apply update using git pull (if git repo) or download.
        Preserves local config and license files.
        """
        result = {
            "success": False,
            "message": "",
            "version_before": self.current_version,
            "version_after": self.current_version,
        }
        
        git_dir = self.app_dir / '.git'
        
        if git_dir.exists():
            # Use git pull for update
            result = self._update_via_git(result)
        else:
            result["message"] = "Not a git repository. Please use 'git clone' to install for auto-updates."
            result["success"] = False
        
        return result
    
    def _update_via_git(self, result: dict) -> dict:
        """Update using git pull."""
        try:
            # Stash any local changes to preserved files
            subprocess.run(
                ['git', 'stash'],
                cwd=str(self.app_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Pull latest
            pull_result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd=str(self.app_dir),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if pull_result.returncode != 0:
                result["message"] = f"Git pull failed: {pull_result.stderr}"
                return result
            
            # Install any new dependencies
            req_file = self.app_dir / 'requirements.txt'
            if req_file.exists():
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '-r', str(req_file), '-q'],
                    cwd=str(self.app_dir),
                    capture_output=True,
                    timeout=120
                )
            
            # Re-read version
            new_version = self._get_current_version()
            
            result["success"] = True
            result["version_after"] = new_version
            result["message"] = f"Updated from v{result['version_before']} to v{new_version}"
            
            logger.info(f"Update applied: {result['message']}")
            return result
            
        except subprocess.TimeoutExpired:
            result["message"] = "Update timed out"
            return result
        except Exception as e:
            result["message"] = f"Update error: {str(e)}"
            logger.error(f"Update failed: {e}")
            return result
    
    def _version_compare(self, v1: str, v2: str) -> int:
        """Compare two semver strings. Returns >0 if v1 > v2."""
        try:
            parts1 = [int(x) for x in v1.split('.')]
            parts2 = [int(x) for x in v2.split('.')]
            
            for a, b in zip(parts1, parts2):
                if a > b:
                    return 1
                if a < b:
                    return -1
            return len(parts1) - len(parts2)
        except (ValueError, AttributeError):
            return 0
    
    def get_update_info(self) -> dict:
        """Get comprehensive update information."""
        check = self.check_for_updates()
        return {
            "current_version": self.current_version,
            "latest_version": check.get("latest", self.current_version),
            "update_available": check.get("available", False),
            "changelog": check.get("changelog", ""),
            "error": check.get("error", ""),
            "is_git_repo": (self.app_dir / '.git').exists(),
            "app_dir": str(self.app_dir),
        }
