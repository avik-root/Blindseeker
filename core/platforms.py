"""
Blindseeker v1.0.0 - Platform Definitions
==========================================
Comprehensive database of 200+ platforms for username enumeration.
Each platform defines URL pattern, detection method, and category.

Detection types:
  - status_code: Check HTTP status (200=found, 404=not found)
  - message: Check response body for "not found" indicators
  - redirect: Profile exists if no redirect occurs
  - json: Check JSON response for existence field

Categories:
  social, developer, gaming, creative, business, finance,
  dating, forum, media, education, music, news, other
"""


PLATFORMS = [
    # ═══════════════════════════════════════════════════════════════
    # SOCIAL MEDIA
    # ═══════════════════════════════════════════════════════════════
    {"name": "Instagram", "url": "https://www.instagram.com/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Twitter/X", "url": "https://x.com/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Facebook", "url": "https://www.facebook.com/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "TikTok", "url": "https://www.tiktok.com/@{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Reddit", "url": "https://www.reddit.com/user/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Pinterest", "url": "https://www.pinterest.com/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Tumblr", "url": "https://{}.tumblr.com", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Snapchat", "url": "https://www.snapchat.com/add/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "LinkedIn", "url": "https://www.linkedin.com/in/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "VK", "url": "https://vk.com/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Mastodon (mastodon.social)", "url": "https://mastodon.social/@{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Threads", "url": "https://www.threads.net/@{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Bluesky", "url": "https://bsky.app/profile/{}.bsky.social", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Quora", "url": "https://www.quora.com/profile/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Medium", "url": "https://medium.com/@{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Telegram", "url": "https://t.me/{}", "detection": "message", "category": "social", "error_msg": "If you have <strong>Telegram</strong>"},
    {"name": "Clubhouse", "url": "https://www.clubhouse.com/@{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Rumble", "url": "https://rumble.com/user/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Minds", "url": "https://www.minds.com/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Gab", "url": "https://gab.com/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Parler", "url": "https://parler.com/user/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Truth Social", "url": "https://truthsocial.com/@{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # DEVELOPER / TECH
    # ═══════════════════════════════════════════════════════════════
    {"name": "GitHub", "url": "https://github.com/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "GitLab", "url": "https://gitlab.com/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Bitbucket", "url": "https://bitbucket.org/{}/", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Stack Overflow", "url": "https://stackoverflow.com/users/?tab=accounts&SearchTerm={}", "detection": "message", "category": "developer", "error_msg": "No users matched your search"},
    {"name": "Dev.to", "url": "https://dev.to/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "HackerRank", "url": "https://www.hackerrank.com/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "LeetCode", "url": "https://leetcode.com/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "CodePen", "url": "https://codepen.io/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Replit", "url": "https://replit.com/@{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Kaggle", "url": "https://www.kaggle.com/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "npm", "url": "https://www.npmjs.com/~{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "PyPI", "url": "https://pypi.org/user/{}/", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Docker Hub", "url": "https://hub.docker.com/u/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Codewars", "url": "https://www.codewars.com/users/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "HackerOne", "url": "https://hackerone.com/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Bugcrowd", "url": "https://bugcrowd.com/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Hashnode", "url": "https://hashnode.com/@{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Glitch", "url": "https://glitch.com/@{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "SourceForge", "url": "https://sourceforge.net/u/{}/profile", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Launchpad", "url": "https://launchpad.net/~{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "About.me", "url": "https://about.me/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Keybase", "url": "https://keybase.io/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Trello", "url": "https://trello.com/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # GAMING
    # ═══════════════════════════════════════════════════════════════
    {"name": "Steam Community", "url": "https://steamcommunity.com/id/{}", "detection": "message", "category": "gaming", "error_msg": "The specified profile could not be found"},
    {"name": "Xbox Gamertag", "url": "https://xboxgamertag.com/search/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "Chess.com", "url": "https://www.chess.com/member/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "Lichess", "url": "https://lichess.org/@/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "Roblox", "url": "https://www.roblox.com/user.aspx?username={}", "detection": "redirect", "category": "gaming"},
    {"name": "Minecraft (NameMC)", "url": "https://namemc.com/profile/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "Epic Games", "url": "https://www.epicgames.com/id/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "Twitch", "url": "https://www.twitch.tv/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "Speedrun.com", "url": "https://www.speedrun.com/users/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "Fortnite Tracker", "url": "https://fortnitetracker.com/profile/all/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "Osu!", "url": "https://osu.ppy.sh/users/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # CREATIVE / DESIGN
    # ═══════════════════════════════════════════════════════════════
    {"name": "Behance", "url": "https://www.behance.net/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Dribbble", "url": "https://dribbble.com/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "DeviantArt", "url": "https://www.deviantart.com/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "ArtStation", "url": "https://www.artstation.com/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Flickr", "url": "https://www.flickr.com/people/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "500px", "url": "https://500px.com/p/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Unsplash", "url": "https://unsplash.com/@{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Pexels", "url": "https://www.pexels.com/@{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Figma", "url": "https://www.figma.com/@{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Canva", "url": "https://www.canva.com/p/{}/", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Pixiv", "url": "https://www.pixiv.net/users/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Wattpad", "url": "https://www.wattpad.com/user/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Archive of Our Own", "url": "https://archiveofourown.org/users/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Redbubble", "url": "https://www.redbubble.com/people/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # MEDIA / VIDEO / STREAMING
    # ═══════════════════════════════════════════════════════════════
    {"name": "YouTube", "url": "https://www.youtube.com/@{}", "detection": "status_code", "category": "media", "expected_code": 200, "not_found_code": 404},
    {"name": "Vimeo", "url": "https://vimeo.com/{}", "detection": "status_code", "category": "media", "expected_code": 200, "not_found_code": 404},
    {"name": "Dailymotion", "url": "https://www.dailymotion.com/{}", "detection": "status_code", "category": "media", "expected_code": 200, "not_found_code": 404},
    {"name": "Bitchute", "url": "https://www.bitchute.com/channel/{}/", "detection": "status_code", "category": "media", "expected_code": 200, "not_found_code": 404},
    {"name": "Odysee", "url": "https://odysee.com/@{}", "detection": "status_code", "category": "media", "expected_code": 200, "not_found_code": 404},
    {"name": "Kick", "url": "https://kick.com/{}", "detection": "status_code", "category": "media", "expected_code": 200, "not_found_code": 404},
    {"name": "Imgur", "url": "https://imgur.com/user/{}", "detection": "status_code", "category": "media", "expected_code": 200, "not_found_code": 404},
    {"name": "Giphy", "url": "https://giphy.com/{}", "detection": "status_code", "category": "media", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # MUSIC
    # ═══════════════════════════════════════════════════════════════
    {"name": "Spotify", "url": "https://open.spotify.com/user/{}", "detection": "status_code", "category": "music", "expected_code": 200, "not_found_code": 404},
    {"name": "SoundCloud", "url": "https://soundcloud.com/{}", "detection": "status_code", "category": "music", "expected_code": 200, "not_found_code": 404},
    {"name": "Bandcamp", "url": "https://{}.bandcamp.com", "detection": "status_code", "category": "music", "expected_code": 200, "not_found_code": 404},
    {"name": "Last.fm", "url": "https://www.last.fm/user/{}", "detection": "status_code", "category": "music", "expected_code": 200, "not_found_code": 404},
    {"name": "Deezer", "url": "https://www.deezer.com/profile/{}", "detection": "status_code", "category": "music", "expected_code": 200, "not_found_code": 404},
    {"name": "Genius", "url": "https://genius.com/{}", "detection": "status_code", "category": "music", "expected_code": 200, "not_found_code": 404},
    {"name": "Mixcloud", "url": "https://www.mixcloud.com/{}/", "detection": "status_code", "category": "music", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # BUSINESS / PROFESSIONAL
    # ═══════════════════════════════════════════════════════════════
    {"name": "Gravatar", "url": "https://en.gravatar.com/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Crunchbase", "url": "https://www.crunchbase.com/person/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "AngelList", "url": "https://angel.co/u/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "ProductHunt", "url": "https://www.producthunt.com/@{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Slideshare", "url": "https://www.slideshare.net/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "HubPages", "url": "https://hubpages.com/@{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Linktree", "url": "https://linktr.ee/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Patreon", "url": "https://www.patreon.com/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Ko-fi", "url": "https://ko-fi.com/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Buy Me a Coffee", "url": "https://buymeacoffee.com/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Fiverr", "url": "https://www.fiverr.com/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Upwork", "url": "https://www.upwork.com/freelancers/~{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # FORUMS / COMMUNITY
    # ═══════════════════════════════════════════════════════════════
    {"name": "Hacker News", "url": "https://news.ycombinator.com/user?id={}", "detection": "message", "category": "forum", "error_msg": "No such user"},
    {"name": "Disqus", "url": "https://disqus.com/by/{}/", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "Discourse (Meta)", "url": "https://meta.discourse.org/u/{}", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "XDA Developers", "url": "https://xdaforums.com/m/{}.0/", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "Instructables", "url": "https://www.instructables.com/member/{}/", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "Hackaday", "url": "https://hackaday.io/{}", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "Itch.io", "url": "https://{}.itch.io", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "Newgrounds", "url": "https://{}.newgrounds.com", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "Wikipedia", "url": "https://en.wikipedia.org/wiki/User:{}", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "Fandom", "url": "https://community.fandom.com/wiki/User:{}", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # FINANCE / CRYPTO
    # ═══════════════════════════════════════════════════════════════
    {"name": "CoinMarketCap", "url": "https://coinmarketcap.com/community/profile/{}/", "detection": "status_code", "category": "finance", "expected_code": 200, "not_found_code": 404},
    {"name": "TradingView", "url": "https://www.tradingview.com/u/{}/", "detection": "status_code", "category": "finance", "expected_code": 200, "not_found_code": 404},
    {"name": "Investing.com", "url": "https://www.investing.com/members/{}", "detection": "status_code", "category": "finance", "expected_code": 200, "not_found_code": 404},
    {"name": "CryptoCompare", "url": "https://www.cryptocompare.com/profile/#{}", "detection": "status_code", "category": "finance", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # DATING
    # ═══════════════════════════════════════════════════════════════
    {"name": "OkCupid", "url": "https://www.okcupid.com/profile/{}", "detection": "status_code", "category": "dating", "expected_code": 200, "not_found_code": 404},
    {"name": "PlentyOfFish", "url": "https://www.pof.com/viewprofile.aspx?profile_id={}", "detection": "status_code", "category": "dating", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # EDUCATION / LEARNING
    # ═══════════════════════════════════════════════════════════════
    {"name": "Duolingo", "url": "https://www.duolingo.com/profile/{}", "detection": "status_code", "category": "education", "expected_code": 200, "not_found_code": 404},
    {"name": "Khan Academy", "url": "https://www.khanacademy.org/profile/{}", "detection": "status_code", "category": "education", "expected_code": 200, "not_found_code": 404},
    {"name": "Coursera", "url": "https://www.coursera.org/user/{}", "detection": "status_code", "category": "education", "expected_code": 200, "not_found_code": 404},
    {"name": "Codecademy", "url": "https://www.codecademy.com/profiles/{}", "detection": "status_code", "category": "education", "expected_code": 200, "not_found_code": 404},
    {"name": "Udemy", "url": "https://www.udemy.com/user/{}/", "detection": "status_code", "category": "education", "expected_code": 200, "not_found_code": 404},
    {"name": "Skillshare", "url": "https://www.skillshare.com/profile/{}", "detection": "status_code", "category": "education", "expected_code": 200, "not_found_code": 404},
    {"name": "ResearchGate", "url": "https://www.researchgate.net/profile/{}", "detection": "status_code", "category": "education", "expected_code": 200, "not_found_code": 404},
    {"name": "Academia.edu", "url": "https://independent.academia.edu/{}", "detection": "status_code", "category": "education", "expected_code": 200, "not_found_code": 404},
    {"name": "Google Scholar", "url": "https://scholar.google.com/citations?user={}", "detection": "status_code", "category": "education", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # NEWS / JOURNALISM
    # ═══════════════════════════════════════════════════════════════
    {"name": "Substack", "url": "https://{}.substack.com", "detection": "status_code", "category": "news", "expected_code": 200, "not_found_code": 404},
    {"name": "Blogger", "url": "https://{}.blogspot.com", "detection": "status_code", "category": "news", "expected_code": 200, "not_found_code": 404},
    {"name": "WordPress", "url": "https://{}.wordpress.com", "detection": "status_code", "category": "news", "expected_code": 200, "not_found_code": 404},
    {"name": "Ghost", "url": "https://{}.ghost.io", "detection": "status_code", "category": "news", "expected_code": 200, "not_found_code": 404},
    {"name": "Blogger (Profile)", "url": "https://www.blogger.com/profile/{}", "detection": "status_code", "category": "news", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # MESSAGING / COMMUNICATION
    # ═══════════════════════════════════════════════════════════════
    {"name": "Skype", "url": "https://web.skype.com/search/users/{}", "detection": "status_code", "category": "messaging", "expected_code": 200, "not_found_code": 404},
    {"name": "Slack (Community)", "url": "https://{}.slack.com", "detection": "status_code", "category": "messaging", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # MISC / OTHER
    # ═══════════════════════════════════════════════════════════════
    {"name": "Gravatar (Global)", "url": "https://gravatar.com/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Foursquare", "url": "https://foursquare.com/user/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "MyAnimeList", "url": "https://myanimelist.net/profile/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "AniList", "url": "https://anilist.co/user/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Letterboxd", "url": "https://letterboxd.com/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Goodreads", "url": "https://www.goodreads.com/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Trakt", "url": "https://trakt.tv/users/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Flipboard", "url": "https://flipboard.com/@{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Internet Archive", "url": "https://archive.org/search?query=uploader:{}", "detection": "message", "category": "other", "error_msg": "0 results"},
    {"name": "Gravatar (JSON)", "url": "https://en.gravatar.com/{}.json", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Strava", "url": "https://www.strava.com/athletes/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Sporcle", "url": "https://www.sporcle.com/user/{}/", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Kongregate", "url": "https://www.kongregate.com/accounts/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "PlayStore Dev", "url": "https://play.google.com/store/apps/developer?id={}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Eyeem", "url": "https://www.eyeem.com/u/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "VSCO", "url": "https://vsco.co/{}/gallery", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Thingiverse", "url": "https://www.thingiverse.com/{}/designs", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Exercism", "url": "https://exercism.org/profiles/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Scratch", "url": "https://scratch.mit.edu/users/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Roblox (Dev Forum)", "url": "https://devforum.roblox.com/u/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "OpenSea", "url": "https://opensea.io/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Rarible", "url": "https://rarible.com/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Foundation", "url": "https://foundation.app/@{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Tenor", "url": "https://tenor.com/users/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Coil", "url": "https://coil.com/u/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Cent", "url": "https://beta.cent.co/@{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Known", "url": "https://{}.known.co", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "GrabCAD", "url": "https://grabcad.com/community/members/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Houzz", "url": "https://www.houzz.com/user/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Periscope", "url": "https://www.periscope.tv/{}/", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Smule", "url": "https://www.smule.com/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "IFTTT", "url": "https://ifttt.com/p/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Cults3D", "url": "https://cults3d.com/en/users/{}/3d-models", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "MyMiniFactory", "url": "https://www.myminifactory.com/users/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Thangs", "url": "https://thangs.com/designer/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "VirusTotal", "url": "https://www.virustotal.com/gui/user/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "CyberDefenders", "url": "https://cyberdefenders.org/p/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "TryHackMe", "url": "https://tryhackme.com/p/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Hack The Box", "url": "https://app.hackthebox.com/profile/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "PentesterLab", "url": "https://pentesterlab.com/profile/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Codeforces", "url": "https://codeforces.com/profile/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "AtCoder", "url": "https://atcoder.jp/users/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "TopCoder", "url": "https://profiles.topcoder.com/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Codesignal", "url": "https://app.codesignal.com/profile/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # SHOPPING / E-COMMERCE
    # ═══════════════════════════════════════════════════════════════
    {"name": "Etsy", "url": "https://www.etsy.com/shop/{}", "detection": "status_code", "category": "shopping", "expected_code": 200, "not_found_code": 404},
    {"name": "eBay", "url": "https://www.ebay.com/usr/{}", "detection": "status_code", "category": "shopping", "expected_code": 200, "not_found_code": 404},
    {"name": "Amazon (Wishlist)", "url": "https://www.amazon.com/hz/wishlist/ls/{}", "detection": "status_code", "category": "shopping", "expected_code": 200, "not_found_code": 404},
    {"name": "Depop", "url": "https://www.depop.com/{}", "detection": "status_code", "category": "shopping", "expected_code": 200, "not_found_code": 404},
    {"name": "Poshmark", "url": "https://poshmark.com/closet/{}", "detection": "status_code", "category": "shopping", "expected_code": 200, "not_found_code": 404},
    {"name": "Mercari", "url": "https://www.mercari.com/u/{}/", "detection": "status_code", "category": "shopping", "expected_code": 200, "not_found_code": 404},
    {"name": "Shopify (Community)", "url": "https://community.shopify.com/c/user/viewprofilepage/user-id/{}", "detection": "status_code", "category": "shopping", "expected_code": 200, "not_found_code": 404},
    {"name": "Gumroad", "url": "https://{}.gumroad.com", "detection": "status_code", "category": "shopping", "expected_code": 200, "not_found_code": 404},
    {"name": "Storenvy", "url": "https://www.storenvy.com/{}", "detection": "status_code", "category": "shopping", "expected_code": 200, "not_found_code": 404},
    {"name": "Teespring", "url": "https://teespring.com/stores/{}", "detection": "status_code", "category": "shopping", "expected_code": 200, "not_found_code": 404},
    {"name": "Zazzle", "url": "https://www.zazzle.com/store/{}", "detection": "status_code", "category": "shopping", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # TRAVEL / MAPS
    # ═══════════════════════════════════════════════════════════════
    {"name": "TripAdvisor", "url": "https://www.tripadvisor.com/Profile/{}", "detection": "status_code", "category": "travel", "expected_code": 200, "not_found_code": 404},
    {"name": "Couchsurfing", "url": "https://www.couchsurfing.com/people/{}", "detection": "status_code", "category": "travel", "expected_code": 200, "not_found_code": 404},
    {"name": "Airbnb", "url": "https://www.airbnb.com/users/show/{}", "detection": "status_code", "category": "travel", "expected_code": 200, "not_found_code": 404},
    {"name": "Geocaching", "url": "https://www.geocaching.com/p/default.aspx?u={}", "detection": "status_code", "category": "travel", "expected_code": 200, "not_found_code": 404},
    {"name": "AllTrails", "url": "https://www.alltrails.com/members/{}", "detection": "status_code", "category": "travel", "expected_code": 200, "not_found_code": 404},
    {"name": "Komoot", "url": "https://www.komoot.com/user/{}", "detection": "status_code", "category": "travel", "expected_code": 200, "not_found_code": 404},
    {"name": "Polarsteps", "url": "https://www.polarsteps.com/{}", "detection": "status_code", "category": "travel", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # FITNESS / HEALTH
    # ═══════════════════════════════════════════════════════════════
    {"name": "Fitbit", "url": "https://www.fitbit.com/user/{}", "detection": "status_code", "category": "fitness", "expected_code": 200, "not_found_code": 404},
    {"name": "MapMyRun", "url": "https://www.mapmyrun.com/profile/{}", "detection": "status_code", "category": "fitness", "expected_code": 200, "not_found_code": 404},
    {"name": "Garmin Connect", "url": "https://connect.garmin.com/modern/profile/{}", "detection": "status_code", "category": "fitness", "expected_code": 200, "not_found_code": 404},
    {"name": "Nike Run Club", "url": "https://www.nike.com/member/profile/{}", "detection": "status_code", "category": "fitness", "expected_code": 200, "not_found_code": 404},
    {"name": "Bodybuilding.com", "url": "https://bodyspace.bodybuilding.com/{}", "detection": "status_code", "category": "fitness", "expected_code": 200, "not_found_code": 404},
    {"name": "Peloton", "url": "https://members.onepeloton.com/members/{}", "detection": "status_code", "category": "fitness", "expected_code": 200, "not_found_code": 404},
    {"name": "Zwift", "url": "https://www.zwift.com/athlete/{}", "detection": "status_code", "category": "fitness", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # FOOD / DRINK
    # ═══════════════════════════════════════════════════════════════
    {"name": "Untappd", "url": "https://untappd.com/user/{}", "detection": "status_code", "category": "food", "expected_code": 200, "not_found_code": 404},
    {"name": "Vivino", "url": "https://www.vivino.com/users/{}", "detection": "status_code", "category": "food", "expected_code": 200, "not_found_code": 404},
    {"name": "Yelp", "url": "https://www.yelp.com/user_details?userid={}", "detection": "status_code", "category": "food", "expected_code": 200, "not_found_code": 404},
    {"name": "Allrecipes", "url": "https://www.allrecipes.com/cook/{}/", "detection": "status_code", "category": "food", "expected_code": 200, "not_found_code": 404},
    {"name": "CookPad", "url": "https://cookpad.com/us/users/{}", "detection": "status_code", "category": "food", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # PODCAST / AUDIO
    # ═══════════════════════════════════════════════════════════════
    {"name": "Anchor.fm", "url": "https://anchor.fm/{}", "detection": "status_code", "category": "podcast", "expected_code": 200, "not_found_code": 404},
    {"name": "Podbean", "url": "https://{}.podbean.com", "detection": "status_code", "category": "podcast", "expected_code": 200, "not_found_code": 404},
    {"name": "Spreaker", "url": "https://www.spreaker.com/user/{}", "detection": "status_code", "category": "podcast", "expected_code": 200, "not_found_code": 404},
    {"name": "Buzzsprout", "url": "https://www.buzzsprout.com/{}", "detection": "status_code", "category": "podcast", "expected_code": 200, "not_found_code": 404},
    {"name": "Castbox", "url": "https://castbox.fm/channel/{}", "detection": "status_code", "category": "podcast", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # CYBERSECURITY / INFOSEC
    # ═══════════════════════════════════════════════════════════════
    {"name": "CrackStation", "url": "https://crackstation.net/profile/{}", "detection": "status_code", "category": "cybersecurity", "expected_code": 200, "not_found_code": 404},
    {"name": "Exploit-DB", "url": "https://www.exploit-db.com/author/?a={}", "detection": "status_code", "category": "cybersecurity", "expected_code": 200, "not_found_code": 404},
    {"name": "CTFtime", "url": "https://ctftime.org/user/{}", "detection": "status_code", "category": "cybersecurity", "expected_code": 200, "not_found_code": 404},
    {"name": "Root Me", "url": "https://www.root-me.org/{}", "detection": "status_code", "category": "cybersecurity", "expected_code": 200, "not_found_code": 404},
    {"name": "OverTheWire", "url": "https://overthewire.org/wargames/community/{}", "detection": "status_code", "category": "cybersecurity", "expected_code": 200, "not_found_code": 404},
    {"name": "Vulnhub", "url": "https://www.vulnhub.com/author/{}/", "detection": "status_code", "category": "cybersecurity", "expected_code": 200, "not_found_code": 404},
    {"name": "Offensive Security", "url": "https://www.offsec.com/community/profile/{}", "detection": "status_code", "category": "cybersecurity", "expected_code": 200, "not_found_code": 404},
    {"name": "Securitytrails", "url": "https://securitytrails.com/community/profile/{}", "detection": "status_code", "category": "cybersecurity", "expected_code": 200, "not_found_code": 404},
    {"name": "Shodan", "url": "https://www.shodan.io/user/{}", "detection": "status_code", "category": "cybersecurity", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # BLOCKCHAIN / WEB3 / CRYPTO
    # ═══════════════════════════════════════════════════════════════
    {"name": "Etherscan", "url": "https://etherscan.io/address/{}", "detection": "status_code", "category": "blockchain", "expected_code": 200, "not_found_code": 404},
    {"name": "Mirror.xyz", "url": "https://mirror.xyz/{}", "detection": "status_code", "category": "blockchain", "expected_code": 200, "not_found_code": 404},
    {"name": "ENS Domains", "url": "https://app.ens.domains/name/{}.eth", "detection": "status_code", "category": "blockchain", "expected_code": 200, "not_found_code": 404},
    {"name": "Zora", "url": "https://zora.co/{}", "detection": "status_code", "category": "blockchain", "expected_code": 200, "not_found_code": 404},
    {"name": "SuperRare", "url": "https://superrare.com/{}", "detection": "status_code", "category": "blockchain", "expected_code": 200, "not_found_code": 404},
    {"name": "LooksRare", "url": "https://looksrare.org/accounts/{}", "detection": "status_code", "category": "blockchain", "expected_code": 200, "not_found_code": 404},
    {"name": "Magic Eden", "url": "https://magiceden.io/u/{}", "detection": "status_code", "category": "blockchain", "expected_code": 200, "not_found_code": 404},
    {"name": "Solscan", "url": "https://solscan.io/account/{}", "detection": "status_code", "category": "blockchain", "expected_code": 200, "not_found_code": 404},
    {"name": "DeFi Pulse", "url": "https://www.defipulse.com/profile/{}", "detection": "status_code", "category": "blockchain", "expected_code": 200, "not_found_code": 404},
    {"name": "Gitcoin", "url": "https://gitcoin.co/{}", "detection": "status_code", "category": "blockchain", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # REGIONAL / INTERNATIONAL SOCIAL
    # ═══════════════════════════════════════════════════════════════
    {"name": "Weibo", "url": "https://weibo.com/u/{}", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "Zhihu", "url": "https://www.zhihu.com/people/{}", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "Douban", "url": "https://www.douban.com/people/{}/", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "Baidu Tieba", "url": "https://tieba.baidu.com/home/main?un={}", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "Bilibili", "url": "https://space.bilibili.com/{}", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "Naver", "url": "https://blog.naver.com/{}", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "LINE (Timeline)", "url": "https://timeline.line.me/user/{}", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "Mixi", "url": "https://mixi.jp/show_profile.pl?id={}", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "OK.ru", "url": "https://ok.ru/profile/{}", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "Taringa", "url": "https://www.taringa.net/{}", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "NicoNico", "url": "https://www.nicovideo.jp/user/{}", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "Pixnet", "url": "https://{}.pixnet.net", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "Ameba", "url": "https://ameblo.jp/{}", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "Hatena", "url": "https://profile.hatena.ne.jp/{}/", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},
    {"name": "FC2", "url": "https://{}.blog.fc2.com", "detection": "status_code", "category": "regional", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # JOB / CAREER
    # ═══════════════════════════════════════════════════════════════
    {"name": "Glassdoor", "url": "https://www.glassdoor.com/member/profile/{}", "detection": "status_code", "category": "career", "expected_code": 200, "not_found_code": 404},
    {"name": "Indeed", "url": "https://my.indeed.com/p/{}", "detection": "status_code", "category": "career", "expected_code": 200, "not_found_code": 404},
    {"name": "Hired", "url": "https://hired.com/talent/{}", "detection": "status_code", "category": "career", "expected_code": 200, "not_found_code": 404},
    {"name": "Wellfound", "url": "https://wellfound.com/u/{}", "detection": "status_code", "category": "career", "expected_code": 200, "not_found_code": 404},
    {"name": "Remote OK", "url": "https://remoteok.com/@{}", "detection": "status_code", "category": "career", "expected_code": 200, "not_found_code": 404},
    {"name": "We Work Remotely", "url": "https://weworkremotely.com/users/{}", "detection": "status_code", "category": "career", "expected_code": 200, "not_found_code": 404},
    {"name": "Toptal", "url": "https://www.toptal.com/resume/{}", "detection": "status_code", "category": "career", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # PHOTOGRAPHY
    # ═══════════════════════════════════════════════════════════════
    {"name": "SmugMug", "url": "https://{}.smugmug.com", "detection": "status_code", "category": "photography", "expected_code": 200, "not_found_code": 404},
    {"name": "ViewBug", "url": "https://www.viewbug.com/member/{}", "detection": "status_code", "category": "photography", "expected_code": 200, "not_found_code": 404},
    {"name": "Fotolog", "url": "https://fotolog.com/{}/", "detection": "status_code", "category": "photography", "expected_code": 200, "not_found_code": 404},
    {"name": "Lomography", "url": "https://www.lomography.com/homes/{}", "detection": "status_code", "category": "photography", "expected_code": 200, "not_found_code": 404},
    {"name": "Photobucket", "url": "https://photobucket.com/user/{}/library", "detection": "status_code", "category": "photography", "expected_code": 200, "not_found_code": 404},
    {"name": "35photo", "url": "https://35photo.pro/{}/", "detection": "status_code", "category": "photography", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # ADDITIONAL SOCIAL / MISC
    # ═══════════════════════════════════════════════════════════════
    {"name": "Signal Guru", "url": "https://signal.guru/user/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Credly", "url": "https://www.credly.com/users/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Notion", "url": "https://notion.so/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Typeracer", "url": "https://data.typeracer.com/pit/profile?user={}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Monkeytype", "url": "https://monkeytype.com/profile/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "WakaTime", "url": "https://wakatime.com/@{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Observable", "url": "https://observablehq.com/@{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Hugging Face", "url": "https://huggingface.co/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Colab (Google)", "url": "https://colab.research.google.com/drive/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Vercel", "url": "https://vercel.com/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Netlify", "url": "https://app.netlify.com/teams/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Render", "url": "https://render.com/u/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Railway", "url": "https://railway.app/@{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Carrd", "url": "https://{}.carrd.co", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Bio.link", "url": "https://bio.link/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Campsite.bio", "url": "https://campsite.bio/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Beacons.ai", "url": "https://beacons.ai/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Stan.store", "url": "https://stan.store/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Snipfeed", "url": "https://snipfeed.co/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Taplink", "url": "https://taplink.cc/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Shorby", "url": "https://shor.by/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "Later (Link in Bio)", "url": "https://linkin.bio/{}", "detection": "status_code", "category": "other", "expected_code": 200, "not_found_code": 404},
    {"name": "GitBook", "url": "https://{}.gitbook.io", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "ReadTheDocs", "url": "https://{}.readthedocs.io", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "Notion.so Blog", "url": "https://notion.so/@{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},
    {"name": "GitConnected", "url": "https://gitconnected.com/{}", "detection": "status_code", "category": "developer", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # ADDITIONAL GAMING
    # ═══════════════════════════════════════════════════════════════
    {"name": "Discord.bio", "url": "https://discord.bio/p/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "RetroAchievements", "url": "https://retroachievements.org/user/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "FACEIT", "url": "https://www.faceit.com/en/players/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "ESEA", "url": "https://play.esea.net/users/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "Battle.net", "url": "https://starcraft2.blizzard.com/en-us/profile/1/1/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "Tracker.gg", "url": "https://tracker.gg/valorant/profile/riot/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "GameJolt", "url": "https://gamejolt.com/@{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "Tabletop Simulator", "url": "https://steamcommunity.com/workshop/browse/?appid=286160&searchtext={}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},
    {"name": "PSNProfiles", "url": "https://psnprofiles.com/{}", "detection": "status_code", "category": "gaming", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # ADDITIONAL SOCIAL / LINKS
    # ═══════════════════════════════════════════════════════════════
    {"name": "Mastodon.world", "url": "https://mastodon.world/@{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Mastodon.online", "url": "https://mastodon.online/@{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Fosstodon", "url": "https://fosstodon.org/@{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Infosec.exchange", "url": "https://infosec.exchange/@{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Lemmy", "url": "https://lemmy.world/u/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Pixelfed", "url": "https://pixelfed.social/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "PeerTube", "url": "https://tilvids.com/a/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Diaspora", "url": "https://diasp.org/u/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Hubzilla", "url": "https://hubzilla.org/channel/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Cohost", "url": "https://cohost.org/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Hive Social", "url": "https://hivesocial.app/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Spoutible", "url": "https://spoutible.com/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "Post.news", "url": "https://post.news/@{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},
    {"name": "T2 Social", "url": "https://t2.social/{}", "detection": "status_code", "category": "social", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # ADDITIONAL FORUMS / COMMUNITY
    # ═══════════════════════════════════════════════════════════════
    {"name": "Reddit (submitted)", "url": "https://www.reddit.com/user/{}/submitted/", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "StackExchange", "url": "https://stackexchange.com/users/?q={}", "detection": "message", "category": "forum", "error_msg": "No users matched"},
    {"name": "Ask Ubuntu", "url": "https://askubuntu.com/users/?q={}", "detection": "message", "category": "forum", "error_msg": "No users matched"},
    {"name": "Super User", "url": "https://superuser.com/users/?q={}", "detection": "message", "category": "forum", "error_msg": "No users matched"},
    {"name": "Server Fault", "url": "https://serverfault.com/users/?q={}", "detection": "message", "category": "forum", "error_msg": "No users matched"},
    {"name": "MathOverflow", "url": "https://mathoverflow.net/users/?q={}", "detection": "message", "category": "forum", "error_msg": "No users matched"},
    {"name": "Physics Forums", "url": "https://www.physicsforums.com/members/{}.0/", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "LessWrong", "url": "https://www.lesswrong.com/users/{}", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "Quillette", "url": "https://quillette.com/author/{}/", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "Lobsters", "url": "https://lobste.rs/u/{}", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},
    {"name": "Tildes", "url": "https://tildes.net/user/{}", "detection": "status_code", "category": "forum", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # ADDITIONAL CREATIVE / WRITING
    # ═══════════════════════════════════════════════════════════════
    {"name": "AO3 (Works)", "url": "https://archiveofourown.org/users/{}/works", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "FanFiction.net", "url": "https://www.fanfiction.net/u/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Royal Road", "url": "https://www.royalroad.com/profile/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Tapas", "url": "https://tapas.io/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Webtoon", "url": "https://www.webtoons.com/creator/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Society6", "url": "https://society6.com/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "Threadless", "url": "https://www.threadless.com/@{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},
    {"name": "TeePublic", "url": "https://www.teepublic.com/user/{}", "detection": "status_code", "category": "creative", "expected_code": 200, "not_found_code": 404},

    # ═══════════════════════════════════════════════════════════════
    # ADDITIONAL BUSINESS / LINKS
    # ═══════════════════════════════════════════════════════════════
    {"name": "Calendly", "url": "https://calendly.com/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Typeform", "url": "https://{}.typeform.com", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "500 Startups", "url": "https://500.co/people/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Dribbble (Teams)", "url": "https://dribbble.com/teams/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Contra", "url": "https://contra.com/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
    {"name": "Guru", "url": "https://www.guru.com/freelancers/{}", "detection": "status_code", "category": "business", "expected_code": 200, "not_found_code": 404},
]


def get_platforms(categories=None):
    """Get platforms filtered by categories."""
    if categories is None:
        return PLATFORMS
    return [p for p in PLATFORMS if p.get('category') in categories]


def get_categories():
    """Get all unique platform categories with counts."""
    cats = {}
    for p in PLATFORMS:
        cat = p.get('category', 'other')
        cats[cat] = cats.get(cat, 0) + 1
    return cats


def get_platform_count():
    """Get total number of platforms."""
    return len(PLATFORMS)
