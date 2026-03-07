/**
 * Blindseeker v1.0.0 — Main JavaScript
 * SocketIO client, scan management, real-time UI updates.
 */

// ─── SocketIO Connection ───
const socket = io();
let currentScanId = null;
let scanStats = { scanned: 0, found: 0, notFound: 0, errors: 0, total: 0 };

// ─── Connection Status ───
socket.on('connect', () => {
    const dot = document.getElementById('ws-status');
    const text = document.getElementById('ws-status-text');
    if (dot) { dot.className = 'status-dot connected'; }
    if (text) { text.textContent = 'Connected'; }
});

socket.on('disconnect', () => {
    const dot = document.getElementById('ws-status');
    const text = document.getElementById('ws-status-text');
    if (dot) { dot.className = 'status-dot disconnected'; }
    if (text) { text.textContent = 'Disconnected'; }
});

socket.on('connected', (data) => {
    const counter = document.getElementById('platform-counter');
    if (counter) { counter.textContent = `${data.platform_count} Platforms`; }
});

// ─── Dashboard Quick Scan ───
const quickForm = document.getElementById('quick-scan-form');
if (quickForm) {
    quickForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const username = document.getElementById('quick-username').value.trim();
        if (!username) return;
        startScan(username);
    });
}

// ─── Search Page Scan ───
const scanForm = document.getElementById('scan-form');
if (scanForm) {
    scanForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const username = document.getElementById('scan-username').value.trim();
        if (!username) return;
        
        // Get categories
        const chips = document.querySelectorAll('.filter-chip input[name="categories"]:checked');
        let categories = [];
        chips.forEach(c => {
            if (c.value !== 'all') categories.push(c.value);
        });
        
        const timeout = parseInt(document.getElementById('scan-timeout')?.value || 15);
        const workers = parseInt(document.getElementById('scan-workers')?.value || 50);
        
        startScan(username, categories.length > 0 ? categories : null, timeout, workers);
    });
    
    // Advanced options toggle
    const toggleAdv = document.getElementById('toggle-advanced');
    if (toggleAdv) {
        toggleAdv.addEventListener('click', () => {
            const opts = document.getElementById('advanced-options');
            if (opts.style.display === 'none') {
                opts.style.display = 'block';
                toggleAdv.querySelector('span').textContent = '▾ Advanced Options';
            } else {
                opts.style.display = 'none';
                toggleAdv.querySelector('span').textContent = '▸ Advanced Options';
            }
        });
    }

    // Category filter chips
    document.querySelectorAll('.filter-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const input = chip.querySelector('input');
            if (input.value === 'all') {
                // Uncheck all others
                document.querySelectorAll('.filter-chip').forEach(c => {
                    c.classList.remove('active');
                    const ci = c.querySelector('input');
                    if (ci) ci.checked = false;
                });
                chip.classList.add('active');
                input.checked = true;
            } else {
                // Uncheck "all"
                document.querySelectorAll('.filter-chip').forEach(c => {
                    if (c.querySelector('input')?.value === 'all') {
                        c.classList.remove('active');
                        c.querySelector('input').checked = false;
                    }
                });
                chip.classList.toggle('active');
                input.checked = chip.classList.contains('active');
                
                // If none selected, re-select "all"
                const anySelected = document.querySelectorAll('.filter-chip.active').length > 0;
                if (!anySelected) {
                    const allChip = document.querySelector('.filter-chip input[value="all"]')?.parentElement;
                    if (allChip) {
                        allChip.classList.add('active');
                        allChip.querySelector('input').checked = true;
                    }
                }
            }
        });
    });
}

// ─── Start Scan ───
function startScan(username, categories = null, timeout = 15, maxWorkers = 50) {
    // Reset stats
    scanStats = { scanned: 0, found: 0, notFound: 0, errors: 0, total: 0 };
    
    // Update UI - show progress
    showScanProgress(username);
    
    // Make API call
    fetch('/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: username,
            categories: categories,
            timeout: timeout,
            max_workers: maxWorkers
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        }
    })
    .catch(err => {
        console.error('Scan start error:', err);
    });
}

function showScanProgress(username) {
    // Dashboard
    const qp = document.getElementById('quick-progress');
    const lr = document.getElementById('live-results');
    if (qp) {
        qp.style.display = 'block';
        document.getElementById('progress-username').textContent = username;
        document.getElementById('progress-bar').style.width = '0%';
        document.getElementById('progress-scanned').textContent = '0';
        document.getElementById('progress-found').textContent = '0';
        document.getElementById('progress-errors').textContent = '0';
    }
    if (lr) { lr.style.display = 'block'; }
    
    // Search page
    const spp = document.getElementById('scan-progress-panel');
    if (spp) {
        spp.style.display = 'block';
        document.getElementById('sp-username').textContent = username;
        document.getElementById('sp-bar').style.width = '0%';
        document.getElementById('sp-scanned').textContent = '0';
        document.getElementById('sp-found').textContent = '0';
        document.getElementById('sp-errors').textContent = '0';
        document.getElementById('sp-not-found').textContent = '0';
    }
    
    // Disable submit buttons
    const btns = document.querySelectorAll('#quick-scan-btn, #scan-submit-btn');
    btns.forEach(btn => {
        btn.disabled = true;
        const text = btn.querySelector('.btn-text');
        const loader = btn.querySelector('.btn-loader');
        if (text) text.textContent = 'SCANNING...';
        if (loader) loader.style.display = 'inline-block';
    });

    // Clear previous feed
    const feeds = document.querySelectorAll('.results-feed');
    feeds.forEach(f => f.innerHTML = '');
}

// ─── Scan Progress Updates ───
socket.on('scan_progress', (data) => {
    const result = data.result;
    scanStats.scanned++;
    
    if (result.found) {
        scanStats.found++;
    } else if (result.error) {
        scanStats.errors++;
    } else {
        scanStats.notFound++;
    }
    
    updateProgressUI();
    addFeedItem(result);
});

function updateProgressUI() {
    const total = parseInt(document.getElementById('progress-total')?.textContent || 
                          document.getElementById('sp-total')?.textContent || 0) || scanStats.scanned;
    const pct = total > 0 ? Math.round((scanStats.scanned / total) * 100) : 0;
    
    // Dashboard progress
    const pb = document.getElementById('progress-bar');
    const ps = document.getElementById('progress-scanned');
    const pf = document.getElementById('progress-found');
    const pe = document.getElementById('progress-errors');
    
    if (pb) pb.style.width = `${pct}%`;
    if (ps) ps.textContent = scanStats.scanned;
    if (pf) pf.textContent = scanStats.found;
    if (pe) pe.textContent = scanStats.errors;
    
    // Search page progress
    const spb = document.getElementById('sp-bar');
    const sps = document.getElementById('sp-scanned');
    const spf = document.getElementById('sp-found');
    const spe = document.getElementById('sp-errors');
    const spnf = document.getElementById('sp-not-found');
    
    if (spb) spb.style.width = `${pct}%`;
    if (sps) sps.textContent = scanStats.scanned;
    if (spf) spf.textContent = scanStats.found;
    if (spe) spe.textContent = scanStats.errors;
    if (spnf) spnf.textContent = scanStats.notFound;
}

function addFeedItem(result) {
    const feedClass = result.found ? 'found' : (result.error ? 'error' : 'not-found');
    const statusIcon = result.found ? '✓' : (result.error ? '⚠' : '✗');
    const url = result.url || '';
    const time = result.response_time ? `${result.response_time}ms` : '—';
    
    const item = document.createElement('div');
    item.className = `feed-item ${feedClass}`;
    item.setAttribute('data-type', feedClass);
    item.innerHTML = `
        <span class="feed-status">${statusIcon}</span>
        <span class="feed-platform">${result.platform}</span>
        <span class="feed-url">${url ? `<a href="${url}" target="_blank">${url}</a>` : (result.error || '—')}</span>
        <span class="feed-time">${time}</span>
    `;
    
    // Add to all feeds
    document.querySelectorAll('.results-feed').forEach(feed => {
        const clone = item.cloneNode(true);
        feed.insertBefore(clone, feed.firstChild);
        
        // Keep feed size manageable
        while (feed.children.length > 200) {
            feed.removeChild(feed.lastChild);
        }
    });
}

// ─── Scan Complete ───
socket.on('scan_complete', (data) => {
    currentScanId = data.scan_id;
    
    // Re-enable buttons
    const btns = document.querySelectorAll('#quick-scan-btn, #scan-submit-btn');
    btns.forEach(btn => {
        btn.disabled = false;
        const text = btn.querySelector('.btn-text');
        const loader = btn.querySelector('.btn-loader');
        if (text) text.textContent = text.dataset.original || 'INITIATE SCAN';
        if (loader) loader.style.display = 'none';
    });
    
    // Update search page completion panel
    const scp = document.getElementById('scan-complete-panel');
    if (scp) {
        scp.style.display = 'block';
        document.getElementById('sc-found').textContent = data.data?.found_count || data.found_count || 0;
        document.getElementById('sc-duration').textContent = `${data.data?.duration_seconds || data.duration || 0}s`;
        document.getElementById('sc-total').textContent = data.data?.total_platforms || data.total || 0;
        document.getElementById('sc-view-results').href = `/results/${data.scan_id}`;
        
        // Update status badge
        const badge = document.getElementById('scan-status-badge');
        if (badge) {
            badge.textContent = 'COMPLETE';
            badge.style.background = 'rgba(0, 255, 136, 0.2)';
        }
    }
    
    // Progress bar to 100%
    const bars = document.querySelectorAll('#progress-bar, #sp-bar');
    bars.forEach(bar => bar.style.width = '100%');
});

socket.on('scan_error', (data) => {
    alert(`Scan error: ${data.error}`);
    
    const btns = document.querySelectorAll('#quick-scan-btn, #scan-submit-btn');
    btns.forEach(btn => {
        btn.disabled = false;
        const text = btn.querySelector('.btn-text');
        const loader = btn.querySelector('.btn-loader');
        if (text) text.textContent = 'INITIATE SCAN';
        if (loader) loader.style.display = 'none';
    });
});

// ─── Scan Started (via Socket) ───
socket.on('scan_started', (data) => {
    const pt = document.getElementById('progress-total');
    const st = document.getElementById('sp-total');
    if (pt) pt.textContent = data.total;
    if (st) st.textContent = data.total;
});

// ─── Feed Filters ───
document.querySelectorAll('.feed-filter').forEach(btn => {
    btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;
        const parent = btn.closest('.live-feed-container') || document;
        
        parent.querySelectorAll('.feed-filter').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        parent.querySelectorAll('.feed-item').forEach(item => {
            if (filter === 'all') {
                item.style.display = 'flex';
            } else {
                item.style.display = item.dataset.type === filter ? 'flex' : 'none';
            }
        });
    });
});

// ─── Mobile Menu Toggle ───
const menuToggle = document.getElementById('menu-toggle');
if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        document.getElementById('sidebar').classList.toggle('open');
    });
}

// ─── Keyboard Shortcut ───
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const input = document.getElementById('quick-username') || document.getElementById('scan-username');
        if (input) input.focus();
    }
});

console.log('%c◉ BLINDSEEKER v1.0.0 — Username Enumeration Engine', 
    'color: #00ff88; font-size: 14px; font-weight: bold;');
