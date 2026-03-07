"""
Blindseeker v1.0.0 - Flask Application
========================================
Main web application with SocketIO real-time updates.
Provides dashboard, search, results, history, settings, and export API.
Developed by MintFire
"""

import os
import sys
import json
import re
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path

from flask import (
    Flask, render_template, request, jsonify, send_file,
    redirect, url_for, flash, session, Response
)
from flask_socketio import SocketIO, emit

from config import get_config, Config
from core.engine import BlindSeekerEngine
from core.exporter import Exporter
from core.platforms import get_platform_count, get_categories

# ──────────────────────────────────────────────────────────────
# App Initialization
# ──────────────────────────────────────────────────────────────

app = Flask(__name__)
config = get_config()
app.config.from_object(config)
app.secret_key = config.SECRET_KEY

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize engine and exporter
engine = BlindSeekerEngine(config)
exporter = Exporter(config.EXPORT_DIR)

# Scan persistence directory
SCANS_DIR = Path('scans')
SCANS_DIR.mkdir(exist_ok=True)

# Logging setup
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(config.LOG_FILE, encoding='utf-8')
    ]
)
logger = logging.getLogger('blindseeker.app')

# In-memory store for scan results (accessible to routes)
scan_store = {}


def save_scan_json(scan_data):
    """Persist scan results to a JSON file in scans/ directory."""
    try:
        scan_id = scan_data.get('scan_id', 'unknown')
        filename = SCANS_DIR / f"{scan_id}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(scan_data, f, indent=2, default=str)
        logger.info(f"Scan saved to {filename}")
        return str(filename)
    except Exception as e:
        logger.error(f"Failed to save scan: {e}")
        return None


def load_scan_json(scan_id):
    """Load scan data from JSON file."""
    try:
        filename = SCANS_DIR / f"{scan_id}.json"
        if filename.exists():
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load scan {scan_id}: {e}")
    return None

# ──────────────────────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────────────────────

BANNER = r"""
    ____  ___           __               __
   / __ )/ (_)___  ____/ /_______  ___  / /_____  _____
  / __  / / / __ \/ __  / ___/ _ \/ _ \/ //_/ _ \/ ___/
 / /_/ / / / / / / /_/ (__  )  __/  __/ ,< /  __/ /
/_____/_/_/_/ /_/\__,_/____/\___/\___/_/|_|\___/_/
                                           v1.0.0
"""

# ──────────────────────────────────────────────────────────────
# Routes - Pages
# ──────────────────────────────────────────────────────────────

@app.route('/')
def dashboard():
    """Main dashboard page."""
    stats = engine.get_stats()
    return render_template('dashboard.html',
                         stats=stats,
                         platform_count=get_platform_count(),
                         categories=get_categories())


@app.route('/search')
def search_page():
    """Search/scan page."""
    categories = get_categories()
    return render_template('search.html', categories=categories)


@app.route('/results/<scan_id>')
def results_page(scan_id):
    """View scan results."""
    scan_data = scan_store.get(scan_id) or load_scan_json(scan_id) or engine.get_scan_status(scan_id)
    if not scan_data:
        flash('Scan not found', 'error')
        return redirect(url_for('dashboard'))
    return render_template('results.html', scan=scan_data)


@app.route('/history')
def history_page():
    """Scan history page — loads from memory, engine, and persisted JSON files."""
    scans = engine.get_history(limit=100)
    scan_ids = {s.get('scan_id') for s in scans}
    
    # Add scans from in-memory store
    for sid, sdata in scan_store.items():
        if sid not in scan_ids:
            scans.append(sdata)
            scan_ids.add(sid)
    
    # Add persisted scans from JSON files
    if SCANS_DIR.exists():
        for f in SCANS_DIR.glob('*.json'):
            try:
                sid = f.stem
                if sid not in scan_ids:
                    with open(f, 'r', encoding='utf-8') as fp:
                        data = json.load(fp)
                        scans.append(data)
                        scan_ids.add(sid)
            except Exception:
                pass
    
    # Sort by start_time descending
    scans.sort(key=lambda s: s.get('start_time', '') or '', reverse=True)
    return render_template('history.html', scans=scans)


@app.route('/settings')
def settings_page():
    """Settings/configuration page."""
    return render_template('settings.html',
                         config=config,
                         proxy_status=engine.proxy_manager.get_status(),
                         tor_status=engine.tor_manager.get_status())


# ──────────────────────────────────────────────────────────────
# Routes - API
# ──────────────────────────────────────────────────────────────

@app.route('/api/scan', methods=['POST'])
def api_start_scan():
    """Start a new scan via API."""
    data = request.get_json() or request.form
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    # Validate username
    if len(username) > 100:
        return jsonify({'error': 'Username too long (max 100 chars)'}), 400
    
    categories = data.get('categories')
    if isinstance(categories, str):
        categories = [c.strip() for c in categories.split(',') if c.strip()]
    
    timeout = int(data.get('timeout', config.REQUEST_TIMEOUT))
    max_workers = int(data.get('max_workers', config.MAX_WORKERS))
    
    # Calculate total platforms for progress tracking
    from core.platforms import get_platforms
    filtered = get_platforms(categories or None)
    total_platforms = len(filtered)
    
    # Emit scan_started with accurate platform count
    socketio.emit('scan_started', {
        'username': username,
        'total': total_platforms
    })
    
    # Progress callback that emits via SocketIO
    def on_progress(result):
        result_dict = result.to_dict()
        socketio.emit('scan_progress', {
            'result': result_dict,
            'username': username
        })
    
    # Run scan in background thread
    def run_scan():
        try:
            scan_session = engine.scan(
                username,
                categories=categories or None,
                timeout=timeout,
                max_workers=max_workers,
                progress_callback=on_progress
            )
            
            scan_data = scan_session.to_dict()
            
            # Auto email trace for found profiles
            try:
                from core.email_tracer import EmailTracer
                tracer = EmailTracer(timeout=5)
                email_variants = [
                    f"{username}@gmail.com",
                    f"{username}@yahoo.com",
                    f"{username}@outlook.com",
                    f"{username}@protonmail.com",
                ]
                email_results = []
                for em in email_variants:
                    trace = tracer.trace_sync(em)
                    if trace and not trace.get('error'):
                        email_results.append(trace)
                scan_data['email_traces'] = email_results
            except Exception as e:
                logger.debug(f"Email auto-trace error: {e}")
                scan_data['email_traces'] = []
            
            scan_store[scan_session.scan_id] = scan_data
            
            # Persist scan to JSON file
            save_scan_json(scan_data)
            
            socketio.emit('scan_complete', {
                'scan_id': scan_session.scan_id,
                'username': username,
                'found_count': len(scan_session.found),
                'total': scan_session.total_platforms,
                'duration': scan_data['duration_seconds']
            })
        except Exception as e:
            logger.error(f"Scan error: {e}")
            socketio.emit('scan_error', {
                'username': username,
                'error': str(e)
            })
    
    thread = threading.Thread(target=run_scan, daemon=True)
    thread.start()
    
    return jsonify({
        'status': 'started',
        'username': username,
        'total_platforms': total_platforms,
        'message': f'Scan initiated for "{username}"'
    })


@app.route('/api/scan/<scan_id>/status')
def api_scan_status(scan_id):
    """Get scan status."""
    data = scan_store.get(scan_id) or engine.get_scan_status(scan_id)
    if not data:
        return jsonify({'error': 'Scan not found'}), 404
    return jsonify(data)


@app.route('/api/export/<scan_id>/<fmt>')
def api_export(scan_id, fmt):
    """Export scan results."""
    scan_data = scan_store.get(scan_id)
    if not scan_data:
        return jsonify({'error': 'Scan not found'}), 404
    
    fmt = fmt.lower()
    allowed = ['json', 'csv', 'pdf', 'xml', 'html', 'xlsx']
    if fmt not in allowed:
        return jsonify({'error': f'Format must be one of: {", ".join(allowed)}'}), 400
    
    investigator = request.args.get('investigator', '')
    case_id = request.args.get('case_id', '')
    notes = request.args.get('notes', '')
    
    try:
        content, fname = exporter.export_bytes(
            scan_data, fmt,
            investigator=investigator,
            case_id=case_id,
            notes=notes
        )
        
        mime_types = {
            'json': 'application/json',
            'csv': 'text/csv',
            'pdf': 'application/pdf',
            'xml': 'application/xml',
            'html': 'text/html',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        
        return Response(
            content,
            mimetype=mime_types.get(fmt, 'application/octet-stream'),
            headers={'Content-Disposition': f'attachment; filename="{fname}"'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def api_stats():
    """Get engine statistics."""
    return jsonify(engine.get_stats())


@app.route('/api/history')
def api_history():
    """Get scan history."""
    limit = int(request.args.get('limit', 50))
    return jsonify(engine.get_history(limit))


@app.route('/api/platforms')
def api_platforms():
    """Get platform list."""
    from core.platforms import PLATFORMS
    return jsonify({
        'count': len(PLATFORMS),
        'categories': get_categories(),
        'platforms': [{'name': p['name'], 'category': p['category']} for p in PLATFORMS]
    })


@app.route('/api/email-trace', methods=['POST'])
def api_email_trace():
    """OSINT email trace endpoint."""
    from core.email_tracer import EmailTracer

    data = request.get_json() or request.form
    email = data.get('email', '').strip()

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    tracer = EmailTracer(timeout=int(data.get('timeout', 10)))
    result = tracer.trace_sync(email)

    if 'error' in result:
        return jsonify(result), 400

    return jsonify(result)


@app.route('/api/parse-names', methods=['POST'])
def api_parse_names():
    """Parse full names into username variants."""
    from core.name_parser import NameParser

    data = request.get_json() or request.form
    text = data.get('names', '').strip()

    if not text:
        return jsonify({'error': 'Names text is required'}), 400

    parser = NameParser()
    batch = parser.parse_batch(text)
    all_usernames = parser.get_all_usernames(text)

    return jsonify({
        'parsed': batch,
        'total_names': len(batch),
        'total_usernames': len(all_usernames),
        'usernames': all_usernames
    })


@app.route('/api/scan/batch', methods=['POST'])
def api_batch_scan():
    """Batch scan: parse names and scan all generated usernames."""
    from core.name_parser import NameParser

    data = request.get_json() or request.form
    text = data.get('names', '').strip()
    mode = data.get('mode', 'name')  # 'name' or 'username'

    if not text:
        return jsonify({'error': 'Input is required'}), 400

    if mode == 'name':
        parser = NameParser()
        usernames = parser.get_all_usernames(text)
    else:
        # Direct username list
        usernames = [u.strip() for u in re.split(r'[\n;|,]+', text) if u.strip()]

    if not usernames:
        return jsonify({'error': 'No valid usernames generated'}), 400

    # Emit batch started
    socketio.emit('batch_started', {
        'usernames': usernames,
        'total_usernames': len(usernames)
    })

    def run_batch():
        from core.platforms import get_platforms
        batch_results = []

        for idx, username in enumerate(usernames):
            socketio.emit('batch_progress', {
                'current_username': username,
                'index': idx + 1,
                'total': len(usernames)
            })

            try:
                scan_session = engine.scan(
                    username,
                    timeout=int(data.get('timeout', 10)),
                    max_workers=int(data.get('max_workers', 50)),
                    progress_callback=lambda r: socketio.emit('scan_progress', {
                        'result': r.to_dict(), 'username': username
                    })
                )

                scan_data = scan_session.to_dict()
                scan_store[scan_session.scan_id] = scan_data
                save_scan_json(scan_data)
                batch_results.append({
                    'username': username,
                    'scan_id': scan_session.scan_id,
                    'found_count': len(scan_session.found)
                })
            except Exception as e:
                logger.error(f"Batch scan error for {username}: {e}")

        socketio.emit('batch_complete', {
            'results': batch_results,
            'total_scanned': len(batch_results)
        })

    thread = threading.Thread(target=run_batch, daemon=True)
    thread.start()

    return jsonify({
        'status': 'started',
        'usernames': usernames,
        'total': len(usernames)
    })


@app.route('/api/settings', methods=['POST'])
def api_update_settings():
    """Update settings."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Tor settings
    if 'tor_enabled' in data:
        if data['tor_enabled']:
            connected = engine.configure_tor(enable=True)
            if not connected:
                return jsonify({
                    'warning': 'Tor enabled but connection could not be verified. '
                               'Ensure Tor service is running.'
                })
        else:
            engine.configure_tor(enable=False)
    
    # Proxy settings
    if 'proxy_list' in data:
        proxies = data['proxy_list']
        if isinstance(proxies, str):
            proxies = [p.strip() for p in proxies.split('\n') if p.strip()]
        engine.configure_proxy(proxy_list=proxies)
    
    # Rate limit
    if 'rate_limit' in data:
        engine.rate_limiter = __import__('core.rate_limiter', fromlist=['RateLimiter']).RateLimiter(
            default_rate=int(data['rate_limit']),
            default_burst=int(data['rate_limit']) * 2
        )
    
    return jsonify({'status': 'Settings updated'})


# ──────────────────────────────────────────────────────────────
# SocketIO Events
# ──────────────────────────────────────────────────────────────

@socketio.on('connect')
def on_connect():
    logger.debug('Client connected via WebSocket')
    emit('connected', {'status': 'connected', 'platform_count': get_platform_count()})


@socketio.on('disconnect')
def on_disconnect():
    logger.debug('Client disconnected')


@socketio.on('start_scan')
def on_start_scan(data):
    """Handle scan request via WebSocket."""
    username = data.get('username', '').strip()
    if not username:
        emit('scan_error', {'error': 'Username is required'})
        return
    
    categories = data.get('categories')
    timeout = int(data.get('timeout', config.REQUEST_TIMEOUT))
    max_workers = int(data.get('max_workers', config.MAX_WORKERS))
    
    from core.platforms import get_platforms
    filtered = get_platforms(categories or None)
    emit('scan_started', {'username': username, 'total': len(filtered)})
    
    def on_progress(result):
        result_dict = result.to_dict()
        socketio.emit('scan_progress', {
            'result': result_dict,
            'username': username
        })
    
    def run():
        try:
            scan_session = engine.scan(
                username,
                categories=categories or None,
                timeout=timeout,
                max_workers=max_workers,
                progress_callback=on_progress
            )
            
            scan_data = scan_session.to_dict()
            scan_store[scan_session.scan_id] = scan_data
            save_scan_json(scan_data)
            
            socketio.emit('scan_complete', {
                'scan_id': scan_session.scan_id,
                'username': username,
                'data': scan_data
            })
        except Exception as e:
            socketio.emit('scan_error', {'error': str(e), 'username': username})
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()


# ──────────────────────────────────────────────────────────────
# Error Handlers
# ──────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template('base.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('base.html', error='Internal server error'), 500


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print(BANNER)
    print(f"  ► Platforms: {get_platform_count()}")
    print(f"  ► Categories: {len(get_categories())}")
    print(f"  ► Server: http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    print(f"  ► Tor: {'Enabled' if config.TOR_ENABLED else 'Disabled'}")
    print(f"  ► Proxy: {'Enabled' if config.PROXY_ENABLED else 'Disabled'}")
    print()
    
    # Auto-configure from env
    if config.TOR_ENABLED:
        engine.configure_tor(enable=True)
    
    if config.PROXY_ENABLED and os.path.exists(config.PROXY_FILE):
        engine.configure_proxy(proxy_file=config.PROXY_FILE)
    
    socketio.run(
        app,
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG if hasattr(config, 'FLASK_DEBUG') else False,
        allow_unsafe_werkzeug=True
    )
