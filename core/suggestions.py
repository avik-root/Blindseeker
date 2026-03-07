"""
Blindseeker v1.0.0 — Profile Suggestion Engine
================================================
Smart suggestion engine that generates expected emails,
locations, and related profile predictions based on 
found usernames and scan results.

Developed by MintFire
"""

import re
import logging
from typing import Dict, List

logger = logging.getLogger('blindseeker.suggestions')


class ProfileSuggestionEngine:
    """
    Generates intelligent suggestions after a scan completes.
    For each found profile, predicts:
    - Expected email addresses
    - Expected location/timezone
    - Related profiles on other platforms
    - Confidence-scored relevance to subject
    """
    
    COMMON_PROVIDERS = [
        'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
        'protonmail.com', 'icloud.com',
    ]
    
    # Platform categories that suggest professional vs personal
    PROFESSIONAL_PLATFORMS = {
        'linkedin', 'github', 'gitlab', 'bitbucket', 'stackoverflow',
        'behance', 'dribbble', 'angellist', 'crunchbase', 'kaggle',
        'medium', 'dev.to', 'hashnode', 'researchgate',
    }
    
    SOCIAL_PLATFORMS = {
        'twitter', 'instagram', 'facebook', 'tiktok', 'snapchat',
        'pinterest', 'reddit', 'tumblr', 'mastodon', 'threads',
    }
    
    def __init__(self):
        pass
    
    def generate_suggestions(self, username: str, found_profiles: list, subject_data: dict = None) -> dict:
        """
        Generate comprehensive suggestions based on scan results.
        
        Args:
            username: The scanned username
            found_profiles: List of found profile dicts from scan
            subject_data: Optional original subject data from agent
            
        Returns:
            Dict with email suggestions, location hints, related profiles, and summary
        """
        suggestions = {
            "username": username,
            "email_suggestions": self._suggest_emails(username, found_profiles, subject_data),
            "location_hints": self._suggest_locations(found_profiles, subject_data),
            "profile_clusters": self._cluster_profiles(found_profiles),
            "identity_indicators": self._extract_identity_signals(found_profiles),
            "risk_assessment": self._assess_digital_risk(found_profiles),
            "platform_summary": self._summarize_platforms(found_profiles),
        }
        
        return suggestions
    
    def _suggest_emails(self, username: str, profiles: list, subject_data: dict = None) -> list:
        """Generate email suggestions based on username patterns and profiles."""
        emails = []
        seen = set()
        
        # Pattern 1: Direct username@provider
        for provider in self.COMMON_PROVIDERS:
            email = f"{username}@{provider}"
            if email not in seen:
                emails.append({
                    "email": email,
                    "confidence": 0.7,
                    "source": "username_direct",
                    "reasoning": f"Common pattern: {username} on {provider}"
                })
                seen.add(email)
        
        # Pattern 2: Parse username for name parts
        # e.g. "johndoe" → "john.doe@gmail.com"
        name_parts = self._extract_name_from_username(username)
        if name_parts:
            first, last = name_parts
            patterns = [
                (f"{first}.{last}", 0.85, "first.last"),
                (f"{first}{last}", 0.75, "firstlast"),
                (f"{first[0]}{last}", 0.65, "flast"),
                (f"{first}_{last}", 0.60, "first_last"),
            ]
            for local, conf, ptype in patterns:
                for provider in self.COMMON_PROVIDERS[:3]:
                    email = f"{local}@{provider}"
                    if email not in seen:
                        emails.append({
                            "email": email,
                            "confidence": conf,
                            "source": f"name_pattern_{ptype}",
                            "reasoning": f"Derived from username decomposition"
                        })
                        seen.add(email)
        
        # Pattern 3: From subject data if available
        if subject_data and subject_data.get("email"):
            known = subject_data["email"].lower()
            if known not in seen:
                emails.insert(0, {
                    "email": known,
                    "confidence": 1.0,
                    "source": "provided",
                    "reasoning": "Explicitly provided by investigator"
                })
                seen.add(known)
        
        # Sort by confidence
        emails.sort(key=lambda e: e["confidence"], reverse=True)
        return emails[:20]
    
    def _suggest_locations(self, profiles: list, subject_data: dict = None) -> list:
        """Infer possible locations from profile data."""
        locations = []
        
        # From explicit subject data
        if subject_data and subject_data.get("location"):
            locations.append({
                "location": subject_data["location"],
                "confidence": 0.95,
                "source": "provided"
            })
        
        # From platform regions — analyze which regional platforms were found
        found_platforms = {p.get("platform", "").lower() for p in profiles if p.get("found")}
        
        region_signals = {
            'IN': ['shareChat', 'koo', 'naukri'],
            'US': ['venmo', 'nextdoor', 'cash.app'],
            'UK': ['gumtree', 'depop'],
            'DE': ['xing'],
            'JP': ['line', 'mixi', 'pixiv'],
        }
        
        for region, platforms in region_signals.items():
            if any(p in found_platforms for p in platforms):
                locations.append({
                    "location": f"Region: {region}",
                    "confidence": 0.6,
                    "source": "platform_signal"
                })
        
        return locations
    
    def _cluster_profiles(self, profiles: list) -> dict:
        """Cluster found profiles by category for analysis."""
        clusters = {"professional": [], "social": [], "creative": [], "other": []}
        
        for p in profiles:
            if not p.get("found"):
                continue
            
            platform = p.get("platform", "").lower()
            category = p.get("category", "other").lower()
            
            entry = {
                "platform": p.get("platform"),
                "url": p.get("url"),
                "category": category,
                "response_time": p.get("response_time"),
            }
            
            if platform in self.PROFESSIONAL_PLATFORMS or category in ['developer', 'business']:
                clusters["professional"].append(entry)
            elif platform in self.SOCIAL_PLATFORMS or category == 'social':
                clusters["social"].append(entry)
            elif category in ['creative', 'photography', 'music']:
                clusters["creative"].append(entry)
            else:
                clusters["other"].append(entry)
        
        return clusters
    
    def _extract_identity_signals(self, profiles: list) -> dict:
        """Extract identity indicators from found profiles."""
        found = [p for p in profiles if p.get("found")]
        
        signals = {
            "total_found": len(found),
            "platform_diversity": len(set(p.get("category", "") for p in found)),
            "is_developer": any(p.get("platform", "").lower() in self.PROFESSIONAL_PLATFORMS for p in found),
            "is_social_active": sum(1 for p in found if p.get("platform", "").lower() in self.SOCIAL_PLATFORMS),
            "username_consistency": "high" if len(found) > 5 else "medium" if len(found) > 2 else "low",
            "digital_footprint": "extensive" if len(found) > 15 else "moderate" if len(found) > 5 else "minimal",
        }
        
        return signals
    
    def _assess_digital_risk(self, profiles: list) -> dict:
        """Assess digital exposure risk level."""
        found = [p for p in profiles if p.get("found")]
        total = len(found)
        
        risk_level = "LOW"
        if total > 20:
            risk_level = "CRITICAL"
        elif total > 10:
            risk_level = "HIGH"
        elif total > 5:
            risk_level = "MEDIUM"
        
        return {
            "level": risk_level,
            "exposure_score": min(100, total * 5),
            "platforms_exposed": total,
            "recommendation": (
                "Subject has minimal digital exposure" if risk_level == "LOW" else
                "Subject has moderate digital exposure — review privacy settings" if risk_level == "MEDIUM" else
                "Subject has significant digital exposure — high OSINT value" if risk_level == "HIGH" else
                "Subject has critical digital exposure — extremely high OSINT value"
            ),
        }
    
    def _summarize_platforms(self, profiles: list) -> dict:
        """Summarize platform findings."""
        found = [p for p in profiles if p.get("found")]
        categories = {}
        for p in found:
            cat = p.get("category", "other")
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        
        return {
            "total_found": len(found),
            "categories": categories,
            "top_category": max(categories, key=categories.get) if categories else "none",
        }
    
    def _extract_name_from_username(self, username: str) -> tuple:
        """Try to extract first/last name from a username string."""
        # Pattern: first.last, first_last, first-last
        match = re.match(r'^([a-z]+)[._\-]([a-z]+)$', username.lower())
        if match:
            return (match.group(1), match.group(2))
        
        # Pattern: firstlast (try common first names)
        common_first = [
            'john', 'james', 'robert', 'michael', 'david', 'william', 'richard',
            'joseph', 'thomas', 'chris', 'daniel', 'matthew', 'andrew', 'mark',
            'steven', 'paul', 'kevin', 'brian', 'jason', 'alex', 'ryan', 'nick',
            'sarah', 'jessica', 'jennifer', 'amanda', 'emily', 'rachel', 'ashley',
            'samantha', 'megan', 'hannah', 'laura', 'kate', 'anna', 'maria',
        ]
        lower = username.lower()
        for name in common_first:
            if lower.startswith(name) and len(lower) > len(name) + 1:
                return (name, lower[len(name):])
        
        return None
