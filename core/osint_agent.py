"""
Blindseeker v1.0.0 — OSINT Intelligence Agent
===============================================
Custom rule-based intelligence agent for comprehensive
person-of-interest analysis. No external LLM dependency.

Takes subject data (name, location, phone, address, pin code, photo, etc.)
and auto-generates search vectors, runs scans, and correlates results.

Developed by MintFire
"""

import re
import hashlib
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

from core.name_parser import NameParser

logger = logging.getLogger('blindseeker.osint_agent')


class OSINTAgent:
    """
    Rule-based OSINT intelligence agent.
    
    Accepts structured subject data and orchestrates:
    1. Input parsing and normalization
    2. Search vector generation (usernames, emails, phone patterns)
    3. Scan execution across platforms
    4. Result correlation and relevance scoring
    5. Intelligence report generation
    """
    
    # Common email providers for email generation
    EMAIL_PROVIDERS = [
        'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
        'protonmail.com', 'icloud.com', 'mail.com', 'aol.com',
        'zoho.com', 'yandex.com', 'gmx.com', 'live.com',
    ]
    
    # Country-specific email providers
    REGIONAL_PROVIDERS = {
        'IN': ['rediffmail.com', 'sify.com'],
        'US': ['comcast.net', 'att.net', 'verizon.net'],
        'UK': ['btinternet.com', 'sky.com', 'virginmedia.com'],
        'DE': ['web.de', 't-online.de', 'gmx.de'],
        'FR': ['orange.fr', 'free.fr', 'sfr.fr'],
        'JP': ['yahoo.co.jp', 'docomo.ne.jp'],
    }
    
    # Phone number format patterns by region
    PHONE_PATTERNS = {
        'IN': r'^(\+91|91|0)?[6789]\d{9}$',
        'US': r'^(\+1|1)?[2-9]\d{2}[2-9]\d{6}$',
        'UK': r'^(\+44|44|0)?7\d{9}$',
        'default': r'^\+?\d{7,15}$',
    }
    
    # PIN code to region mapping (India as example — expandable)
    PIN_REGIONS = {
        '1': 'Delhi/North',    '2': 'North',         '3': 'Rajasthan/West',
        '4': 'Maharashtra',    '5': 'South/Andhra',   '6': 'South/Kerala',
        '7': 'East/NE',        '8': 'Bihar/East',     '9': 'Army/APO',
    }
    
    def __init__(self):
        self.name_parser = NameParser()
        self.session_data = {}
        self._conversation_state = "AWAITING_INPUT"
        self._collected_fields = {}
        self._analysis_steps = []
    
    # ──────────────────────────────────────────────
    # Conversation Engine
    # ──────────────────────────────────────────────
    
    def get_greeting(self) -> dict:
        """Return the initial greeting and available input fields."""
        return {
            "message": (
                "I am the Blindseeker OSINT Intelligence Agent. "
                "Provide me with any information about your subject and I will "
                "analyze, correlate, and scan the internet for their digital footprint.\n\n"
                "You can provide any combination of the following data points:"
            ),
            "fields": [
                {"id": "name", "label": "Full Name", "type": "text", "icon": "user", "placeholder": "e.g. John Michael Smith", "required": False},
                {"id": "location", "label": "Location / City", "type": "text", "icon": "map-pin", "placeholder": "e.g. Mumbai, India", "required": False},
                {"id": "phone", "label": "Phone Number", "type": "text", "icon": "phone", "placeholder": "e.g. +91 98765 43210", "required": False},
                {"id": "email", "label": "Known Email", "type": "text", "icon": "mail", "placeholder": "e.g. john@gmail.com", "required": False},
                {"id": "address", "label": "Address", "type": "text", "icon": "home", "placeholder": "e.g. 123 Main St, City", "required": False},
                {"id": "pincode", "label": "PIN / ZIP Code", "type": "text", "icon": "hash", "placeholder": "e.g. 400001", "required": False},
                {"id": "username", "label": "Known Username", "type": "text", "icon": "at-sign", "placeholder": "e.g. johndoe123", "required": False},
                {"id": "dob", "label": "Date of Birth", "type": "text", "icon": "calendar", "placeholder": "e.g. 1990-05-15", "required": False},
                {"id": "organization", "label": "Organization / Company", "type": "text", "icon": "building", "placeholder": "e.g. Google", "required": False},
                {"id": "additional", "label": "Additional Details", "type": "textarea", "icon": "file-text", "placeholder": "Any other info — bio, hobbies, aliases...", "required": False},
            ],
            "state": "AWAITING_INPUT"
        }
    
    def analyze_subject(self, subject_data: Dict[str, str]) -> dict:
        """
        Main analysis entry point. Takes subject data dict and returns
        comprehensive intelligence analysis with search vectors.
        """
        self._collected_fields = {k: v for k, v in subject_data.items() if v and v.strip()}
        self._analysis_steps = []
        
        if not self._collected_fields:
            return {"error": "No data provided. Please enter at least one piece of information."}
        
        # Step 1: Parse and normalize all inputs
        self._step("Parsing and normalizing input data...")
        parsed = self._parse_inputs(self._collected_fields)
        
        # Step 2: Generate search vectors
        self._step("Generating search vectors...")
        search_vectors = self.generate_search_vectors(parsed)
        
        # Step 3: Generate expected email addresses
        self._step("Predicting email addresses...")
        expected_emails = self._generate_expected_emails(parsed)
        
        # Step 4: Geographic intelligence
        self._step("Analyzing geographic data...")
        geo_intel = self._analyze_geography(parsed)
        
        # Step 5: Build identity profile
        self._step("Building identity profile...")
        identity_profile = self._build_identity_profile(parsed, search_vectors, expected_emails, geo_intel)
        
        # Step 6: Generate scan plan
        self._step("Creating scan strategy...")
        scan_plan = self._generate_scan_plan(search_vectors, geo_intel)
        
        return {
            "status": "analysis_complete",
            "subject_data": self._collected_fields,
            "parsed": parsed,
            "search_vectors": search_vectors,
            "expected_emails": expected_emails,
            "geo_intelligence": geo_intel,
            "identity_profile": identity_profile,
            "scan_plan": scan_plan,
            "analysis_steps": self._analysis_steps,
            "total_usernames": len(search_vectors.get("usernames", [])),
            "total_emails": len(expected_emails),
            "confidence_score": self._calculate_confidence(parsed),
        }
    
    # ──────────────────────────────────────────────
    # Input Parsing
    # ──────────────────────────────────────────────
    
    def _parse_inputs(self, fields: dict) -> dict:
        """Parse and normalize all input fields."""
        parsed = {
            "name_components": {},
            "usernames_from_name": [],
            "phone_info": {},
            "email_info": {},
            "location_info": {},
            "pincode_info": {},
            "known_usernames": [],
            "dob_info": {},
            "org_info": {},
            "keywords": [],
        }
        
        # Parse name
        if fields.get("name"):
            name_result = self.name_parser.parse_name(fields["name"])
            parsed["name_components"] = name_result
            parsed["usernames_from_name"] = self.name_parser.generate_usernames(name_result)
        
        # Parse phone
        if fields.get("phone"):
            parsed["phone_info"] = self._parse_phone(fields["phone"])
        
        # Parse email
        if fields.get("email"):
            parsed["email_info"] = self._parse_email(fields["email"])
        
        # Parse location
        if fields.get("location"):
            parsed["location_info"] = self._parse_location(fields["location"])
        
        # Parse PIN code
        if fields.get("pincode"):
            parsed["pincode_info"] = self._parse_pincode(fields["pincode"])
        
        # Known username
        if fields.get("username"):
            parsed["known_usernames"] = [u.strip() for u in fields["username"].split(",") if u.strip()]
        
        # DOB
        if fields.get("dob"):
            parsed["dob_info"] = self._parse_dob(fields["dob"])
        
        # Organization
        if fields.get("organization"):
            parsed["org_info"] = {"name": fields["organization"].strip(), "normalized": fields["organization"].strip().lower().replace(" ", "")}
        
        # Additional details → keyword extraction
        if fields.get("additional"):
            parsed["keywords"] = self._extract_keywords(fields["additional"])
        
        return parsed
    
    def _parse_phone(self, phone: str) -> dict:
        """Parse phone number and detect region."""
        clean = re.sub(r'[\s\-\(\)\.]', '', phone.strip())
        info = {"raw": phone, "cleaned": clean, "valid": False, "region": "unknown"}
        
        for region, pattern in self.PHONE_PATTERNS.items():
            if re.match(pattern, clean):
                info["valid"] = True
                info["region"] = region
                break
        
        if not info["valid"] and re.match(self.PHONE_PATTERNS['default'], clean):
            info["valid"] = True
            info["region"] = "international"
        
        # Extract digits that could be usernames
        digits = re.sub(r'\D', '', clean)
        info["username_patterns"] = []
        if len(digits) >= 10:
            info["username_patterns"].append(digits[-10:])  # Last 10 digits
            info["username_patterns"].append(digits[-4:])    # Last 4 digits
        
        return info
    
    def _parse_email(self, email: str) -> dict:
        """Parse email address and extract components."""
        email = email.strip().lower()
        info = {"raw": email, "valid": False, "local": "", "domain": "", "provider": ""}
        
        match = re.match(r'^([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$', email)
        if match:
            info["valid"] = True
            info["local"] = match.group(1)
            info["domain"] = match.group(2)
            info["provider"] = match.group(2).split('.')[0].capitalize()
            
            # Extract potential usernames from email local part
            info["extracted_usernames"] = self._usernames_from_email_local(info["local"])
        
        return info
    
    def _parse_location(self, location: str) -> dict:
        """Parse location string into components."""
        parts = [p.strip() for p in location.split(',')]
        info = {"raw": location, "city": "", "state": "", "country": "", "region_code": ""}
        
        if len(parts) >= 3:
            info["city"], info["state"], info["country"] = parts[0], parts[1], parts[2]
        elif len(parts) == 2:
            info["city"], info["country"] = parts[0], parts[1]
        else:
            info["city"] = parts[0]
        
        # Detect country code
        country = info.get("country", "").strip().upper()
        country_map = {
            'INDIA': 'IN', 'USA': 'US', 'UNITED STATES': 'US', 'UK': 'UK',
            'ENGLAND': 'UK', 'GERMANY': 'DE', 'FRANCE': 'FR', 'JAPAN': 'JP',
            'CANADA': 'CA', 'AUSTRALIA': 'AU', 'BRAZIL': 'BR', 'CHINA': 'CN',
        }
        info["region_code"] = country_map.get(country, country[:2] if len(country) >= 2 else "")
        
        return info
    
    def _parse_pincode(self, pincode: str) -> dict:
        """Parse PIN/ZIP code and derive region hints."""
        clean = re.sub(r'\s', '', pincode.strip())
        info = {"raw": pincode, "cleaned": clean, "region_hint": ""}
        
        # Indian PIN code (6 digits)
        if re.match(r'^\d{6}$', clean):
            first_digit = clean[0]
            info["region_hint"] = self.PIN_REGIONS.get(first_digit, "Unknown Region")
            info["country"] = "India"
        # US ZIP (5 or 5+4)
        elif re.match(r'^\d{5}(-\d{4})?$', clean):
            info["country"] = "USA"
        # UK postcode
        elif re.match(r'^[A-Z]{1,2}\d', clean.upper()):
            info["country"] = "UK"
        
        return info
    
    def _parse_dob(self, dob: str) -> dict:
        """Parse date of birth."""
        info = {"raw": dob, "year": None, "patterns": []}
        
        # Try common formats
        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
            try:
                dt = datetime.strptime(dob.strip(), fmt)
                info["year"] = dt.year
                info["month"] = dt.month
                info["day"] = dt.day
                # Common DOB-based username patterns
                info["patterns"] = [
                    str(dt.year),
                    f"{dt.day:02d}{dt.month:02d}",
                    f"{dt.month:02d}{dt.day:02d}",
                    str(dt.year)[-2:],
                    f"{dt.day:02d}{dt.month:02d}{str(dt.year)[-2:]}",
                ]
                break
            except ValueError:
                continue
        
        return info
    
    def _extract_keywords(self, text: str) -> list:
        """Extract meaningful keywords from freetext."""
        # Remove common stop words and extract tokens
        stop_words = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'shall', 'to', 'of',
            'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
            'and', 'or', 'but', 'not', 'no', 'nor', 'so', 'yet', 'both',
            'this', 'that', 'these', 'those', 'it', 'its', 'he', 'she',
            'they', 'them', 'their', 'his', 'her', 'him', 'my', 'your',
        }
        tokens = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        return [t for t in tokens if t not in stop_words]
    
    def _usernames_from_email_local(self, local: str) -> list:
        """Generate username variants from an email local part."""
        variants = [local]
        # Split on dots, underscores, numbers
        parts = re.split(r'[._\-+]', local)
        if len(parts) > 1:
            variants.extend(parts)
            variants.append(''.join(parts))
        # Remove trailing numbers
        base = re.sub(r'\d+$', '', local)
        if base and base != local:
            variants.append(base)
        return list(set(variants))
    
    # ──────────────────────────────────────────────
    # Search Vector Generation
    # ──────────────────────────────────────────────
    
    def generate_search_vectors(self, parsed: dict) -> dict:
        """Generate all search vectors from parsed data."""
        usernames = set()
        
        # From name parsing
        usernames.update(parsed.get("usernames_from_name", []))
        
        # Known usernames
        usernames.update(parsed.get("known_usernames", []))
        
        # From email
        email_info = parsed.get("email_info", {})
        if email_info.get("extracted_usernames"):
            usernames.update(email_info["extracted_usernames"])
        
        # From phone digits
        phone_info = parsed.get("phone_info", {})
        name_components = parsed.get("name_components", {})
        first = name_components.get("first", "").lower()
        last = name_components.get("last", "").lower()
        
        if phone_info.get("username_patterns") and first:
            for pattern in phone_info["username_patterns"]:
                usernames.add(f"{first}{pattern}")
                if last:
                    usernames.add(f"{first}{last}{pattern[-4:]}")
        
        # From DOB patterns
        dob_info = parsed.get("dob_info", {})
        if dob_info.get("patterns") and first:
            for pattern in dob_info["patterns"]:
                usernames.add(f"{first}{pattern}")
                if last:
                    usernames.add(f"{first}{last}{pattern}")
                    usernames.add(f"{first}.{last}{pattern}")
        
        # From organization
        org_info = parsed.get("org_info", {})
        if org_info.get("normalized") and first:
            usernames.add(f"{first}_{org_info['normalized']}")
            if last:
                usernames.add(f"{first}.{last}@{org_info['normalized']}")
        
        # From keywords
        keywords = parsed.get("keywords", [])
        if first and keywords:
            for kw in keywords[:5]:
                usernames.add(f"{first}{kw}")
                usernames.add(f"{kw}{first}")
        
        # Clean and deduplicate
        clean_usernames = sorted(set(
            u.lower().strip() for u in usernames 
            if u and len(u) >= 3 and len(u) <= 50 and '@' not in u
        ))
        
        return {
            "usernames": clean_usernames,
            "primary_username": clean_usernames[0] if clean_usernames else "",
            "total": len(clean_usernames),
        }
    
    # ──────────────────────────────────────────────
    # Email Prediction
    # ──────────────────────────────────────────────
    
    def _generate_expected_emails(self, parsed: dict) -> list:
        """Generate expected email addresses from subject data."""
        emails = []
        name = parsed.get("name_components", {})
        first = name.get("first", "").lower()
        last = name.get("last", "").lower()
        middle = name.get("middle", "").lower()
        region_code = ""
        
        # Get region from location or pincode
        loc = parsed.get("location_info", {})
        pin = parsed.get("pincode_info", {})
        region_code = loc.get("region_code", "") or pin.get("country", "")[:2].upper()
        
        if not first:
            # Fallback to known username
            known = parsed.get("known_usernames", [])
            if known:
                for provider in self.EMAIL_PROVIDERS[:6]:
                    emails.append({"email": f"{known[0]}@{provider}", "confidence": 0.5, "source": "username"})
            return emails
        
        # Generate email patterns
        patterns = []
        if first and last:
            patterns = [
                (f"{first}.{last}", 0.85),
                (f"{first}{last}", 0.80),
                (f"{first[0]}{last}", 0.70),
                (f"{first}_{last}", 0.65),
                (f"{last}.{first}", 0.60),
                (f"{first}{last[0]}", 0.55),
                (f"{first[0]}.{last}", 0.65),
            ]
            if middle:
                patterns.extend([
                    (f"{first}.{middle[0]}.{last}", 0.60),
                    (f"{first}{middle[0]}{last}", 0.55),
                ])
        elif first:
            patterns = [(first, 0.50)]
        
        # Apply to providers
        providers = list(self.EMAIL_PROVIDERS)
        if region_code in self.REGIONAL_PROVIDERS:
            providers.extend(self.REGIONAL_PROVIDERS[region_code])
        
        for local, base_confidence in patterns:
            for provider in providers[:8]:  # Top 8 providers
                # Adjust confidence based on provider popularity 
                provider_weight = 1.0 if provider in ['gmail.com', 'yahoo.com', 'outlook.com'] else 0.8
                emails.append({
                    "email": f"{local}@{provider}",
                    "confidence": round(base_confidence * provider_weight, 2),
                    "source": "name_pattern"
                })
        
        # Add known email if provided
        email_info = parsed.get("email_info", {})
        if email_info.get("valid"):
            emails.insert(0, {
                "email": email_info["raw"],
                "confidence": 1.0,
                "source": "provided"
            })
        
        # Sort by confidence
        emails.sort(key=lambda e: e["confidence"], reverse=True)
        return emails[:30]  # Top 30 predictions
    
    # ──────────────────────────────────────────────
    # Geographic Intelligence
    # ──────────────────────────────────────────────
    
    def _analyze_geography(self, parsed: dict) -> dict:
        """Analyze geographic information from all data sources."""
        geo = {
            "primary_location": "",
            "country": "",
            "region_code": "",
            "city": "",
            "confidence": 0,
            "sources": [],
            "regional_platforms": [],
        }
        
        loc = parsed.get("location_info", {})
        pin = parsed.get("pincode_info", {})
        phone = parsed.get("phone_info", {})
        
        # Priority: explicit location > PIN code > phone region
        if loc.get("city"):
            geo["city"] = loc["city"]
            geo["country"] = loc.get("country", "")
            geo["region_code"] = loc.get("region_code", "")
            geo["primary_location"] = loc["raw"]
            geo["confidence"] = 0.9
            geo["sources"].append("explicit_location")
        
        if pin.get("country"):
            if not geo["country"]:
                geo["country"] = pin["country"]
            if pin.get("region_hint"):
                geo["primary_location"] = geo.get("primary_location") or pin["region_hint"]
                geo["sources"].append("pincode")
                geo["confidence"] = max(geo["confidence"], 0.7)
        
        if phone.get("region") and phone["region"] not in ("unknown", "international"):
            if not geo["region_code"]:
                geo["region_code"] = phone["region"]
                geo["sources"].append("phone_region")
                geo["confidence"] = max(geo["confidence"], 0.5)
        
        # Suggest regional platforms based on detected region
        region_platforms = {
            'IN': ['Naukri', 'ShareChat', 'JioSaavn', 'Koo', 'LinkedIn (India)'],
            'US': ['LinkedIn', 'Glassdoor', 'Indeed', 'Nextdoor', 'Venmo'],
            'UK': ['Gumtree', 'Rightmove', 'LinkedIn (UK)', 'Depop'],
            'DE': ['XING', 'StudiVZ', 'LinkedIn (Germany)'],
            'JP': ['Line', 'Mixi', 'Hatena', 'Pixiv'],
            'BR': ['Orkut Archives', 'LinkedIn (Brazil)', 'OLX Brasil'],
        }
        geo["regional_platforms"] = region_platforms.get(geo["region_code"], [])
        
        return geo
    
    # ──────────────────────────────────────────────
    # Identity Profile Builder
    # ──────────────────────────────────────────────
    
    def _build_identity_profile(self, parsed: dict, vectors: dict, emails: list, geo: dict) -> dict:
        """Build a structured identity profile for the subject."""
        name = parsed.get("name_components", {})
        
        profile = {
            "display_name": f"{name.get('first', '')} {name.get('middle', '')} {name.get('last', '')}".strip(),
            "first_name": name.get("first", ""),
            "last_name": name.get("last", ""),
            "primary_username": vectors.get("primary_username", ""),
            "username_count": vectors.get("total", 0),
            "primary_email": emails[0]["email"] if emails else "",
            "email_count": len(emails),
            "location": geo.get("primary_location", ""),
            "country": geo.get("country", ""),
            "phone": parsed.get("phone_info", {}).get("cleaned", ""),
            "organization": parsed.get("org_info", {}).get("name", ""),
            "dob_year": parsed.get("dob_info", {}).get("year"),
            "data_richness": len([v for v in parsed.values() if v]),
            "keywords": parsed.get("keywords", [])[:10],
        }
        
        return profile
    
    # ──────────────────────────────────────────────
    # Scan Planning
    # ──────────────────────────────────────────────
    
    def _generate_scan_plan(self, vectors: dict, geo: dict) -> dict:
        """Generate an optimized scan plan."""
        usernames = vectors.get("usernames", [])
        
        plan = {
            "total_usernames": len(usernames),
            "priority_usernames": usernames[:5],     # Most likely usernames
            "secondary_usernames": usernames[5:15],  # Secondary variants
            "extended_usernames": usernames[15:],     # Extended variants
            "recommended_categories": ["social", "developer", "business", "creative"],
            "regional_focus": geo.get("regional_platforms", []),
            "estimated_scan_time": f"{max(30, len(usernames) * 15)}s",
        }
        
        return plan
    
    # ──────────────────────────────────────────────
    # Result Correlation
    # ──────────────────────────────────────────────
    
    def correlate_results(self, scan_results: list, subject_data: dict) -> list:
        """
        Cross-reference found profiles with subject data for relevance scoring.
        
        Each result gets a score 0-100 based on:
        - Name match in bio/display name
        - Location consistency
        - Cross-platform username reuse
        - Email domain/pattern match
        - Bio keyword overlap
        """
        if not scan_results or not subject_data:
            return scan_results
        
        name = subject_data.get("name", "").lower()
        location = subject_data.get("location", "").lower()
        email = subject_data.get("email", "").lower()
        keywords = [k.lower() for k in subject_data.get("keywords", [])]
        
        scored_results = []
        found_usernames = set()
        
        for result in scan_results:
            score = 0
            reasons = []
            
            # Platform found = base score
            if result.get("found"):
                score += 20
                reasons.append("profile_exists")
                
                url = result.get("url", "").lower()
                platform_name = result.get("platform", "").lower()
                bio = result.get("bio", "").lower()
                
                # Username reuse across platforms
                username = result.get("username", "").lower()
                if username in found_usernames:
                    score += 15
                    reasons.append("cross_platform_reuse")
                found_usernames.add(username)
                
                # Name appears in URL or profile
                if name:
                    name_parts = name.split()
                    for part in name_parts:
                        if len(part) >= 3 and part in url:
                            score += 10
                            reasons.append("name_in_url")
                            break
                
                # Location keyword in profile
                if location:
                    loc_parts = [p.strip() for p in location.split(',')]
                    for lp in loc_parts:
                        if len(lp) >= 3 and lp.lower() in bio:
                            score += 10
                            reasons.append("location_match")
                            break
                
                # Keyword overlap
                if keywords and bio:
                    overlaps = sum(1 for kw in keywords if kw in bio)
                    if overlaps > 0:
                        score += min(15, overlaps * 5)
                        reasons.append(f"keyword_match_{overlaps}")
            
            result["relevance_score"] = min(100, score)
            result["relevance_reasons"] = reasons
            scored_results.append(result)
        
        # Sort by relevance
        scored_results.sort(key=lambda r: r.get("relevance_score", 0), reverse=True)
        return scored_results
    
    # ──────────────────────────────────────────────
    # Intelligence Report
    # ──────────────────────────────────────────────
    
    def build_intelligence_report(self, analysis: dict, scan_results: list = None) -> dict:
        """Build a structured intelligence report."""
        profile = analysis.get("identity_profile", {})
        
        report = {
            "report_id": hashlib.sha256(
                f"{profile.get('display_name', '')}{datetime.now(timezone.utc).isoformat()}".encode()
            ).hexdigest()[:16],
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "subject": profile,
            "data_points_provided": len(analysis.get("subject_data", {})),
            "usernames_generated": analysis.get("total_usernames", 0),
            "emails_predicted": analysis.get("total_emails", 0),
            "confidence_score": analysis.get("confidence_score", 0),
            "geographic_intel": analysis.get("geo_intelligence", {}),
            "scan_plan": analysis.get("scan_plan", {}),
            "analysis_steps": analysis.get("analysis_steps", []),
        }
        
        if scan_results:
            found = [r for r in scan_results if r.get("found")]
            report["scan_results"] = {
                "total_scanned": len(scan_results),
                "profiles_found": len(found),
                "high_relevance": len([r for r in found if r.get("relevance_score", 0) >= 60]),
                "results": scan_results[:50],
            }
        
        return report
    
    # ──────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────
    
    def _step(self, message: str):
        """Record an analysis step."""
        self._analysis_steps.append({
            "step": len(self._analysis_steps) + 1,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    
    def _calculate_confidence(self, parsed: dict) -> int:
        """Calculate overall confidence score (0-100) based on data richness."""
        score = 0
        weights = {
            "name_components": 25,
            "known_usernames": 15,
            "email_info": 15,
            "phone_info": 10,
            "location_info": 15,
            "pincode_info": 5,
            "dob_info": 5,
            "org_info": 5,
            "keywords": 5,
        }
        for field, weight in weights.items():
            val = parsed.get(field)
            if val:
                if isinstance(val, dict) and any(v for v in val.values() if v):
                    score += weight
                elif isinstance(val, list) and len(val) > 0:
                    score += weight
        
        return min(100, score)
