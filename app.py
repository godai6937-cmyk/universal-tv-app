import os

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Live TV Player</title>
    <!-- Include HLS.js for cross-browser live streaming support -->
    <script src="https://cdn.jsdelivr.net/npm/hls.js@1"></script>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #121212;
            color: #ffffff;
            padding: 20px;
        }
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1400px;
            margin: 0 auto 30px auto;
            flex-wrap: wrap;
            gap: 20px;
        }
        h1 {
            color: #ff4757;
            font-size: 2.2rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin: 0;
            flex: 1;
        }
        .controls-row {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        .filter-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .filter-label {
            font-size: 0.85rem;
            color: #aaa;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }
        .viewer-count {
            font-size: 0.95rem;
            font-weight: bold;
            color: #ff4757;
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 71, 87, 0.1);
            padding: 8px 15px;
            border-radius: 20px;
            border: 1px solid rgba(255, 71, 87, 0.3);
            margin: 0 auto;
        }
        .viewer-count::before {
            content: '';
            display: inline-block;
            width: 10px;
            height: 10px;
            background-color: #ff4757;
            border-radius: 50%;
            box-shadow: 0 0 5px #ff4757;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 71, 87, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(255, 71, 87, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 71, 87, 0); }
        }
        .search-box {
            padding: 12px 20px;
            border-radius: 25px;
            border: 1px solid #333;
            background: #1e1e1e;
            color: #fff;
            font-size: 1rem;
            width: 300px;
            outline: none;
            transition: border-color 0.3s;
        }
        .search-box:focus {
            border-color: #ff4757;
        }
        select.search-box {
            width: 220px;
            cursor: pointer;
            appearance: auto;
        }
        
        .contact-info {
            width: 100%;
            text-align: right;
            font-size: 0.9rem;
            color: #aaa;
            margin-top: 5px;
        }
        .contact-info a {
            color: #ff4757;
            text-decoration: none;
            font-weight: bold;
            transition: color 0.2s;
        }
        .contact-info a:hover {
            color: #ff6b81;
            text-decoration: underline;
        }
        
        /* Loading Overlay */
        #loadingOverlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(18, 18, 18, 0.95);
            z-index: 5000;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 20px;
            transition: opacity 0.5s, visibility 0.5s;
        }
        #loadingOverlay.hidden {
            opacity: 0;
            visibility: hidden;
        }
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid #333;
            border-top: 5px solid #ff4757;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        .progress-bar-container {
            width: 300px;
            height: 10px;
            background: #333;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 10px;
        }
        #progressBar {
            height: 100%;
            width: 0%;
            background: #ff4757;
            transition: width 0.2s;
        }

        .grid-wrapper {
            max-width: 1400px;
            margin: 0 auto;
            padding-bottom: 40px;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 20px;
        }
        .category-header {
            width: 100%;
            margin-top: 40px;
            margin-bottom: 20px;
            color: #ff4757;
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
            font-size: 1.8rem;
        }
        .channel-card {
            background-color: #1e1e1e;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid #2d2d2d;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            height: 200px;
        }
        .channel-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(255, 71, 87, 0.3);
            border-color: #ff4757;
        }
        .channel-logo {
            width: 90px;
            height: 90px;
            object-fit: contain;
            background-color: #2a2a2a;
            border-radius: 8px;
            padding: 5px;
            margin-bottom: 10px;
        }
        .channel-logo-text {
            width: 90px;
            height: 90px;
            background-color: #2a2a2a;
            border-radius: 8px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.2rem;
            font-weight: bold;
            color: #ff4757;
            text-shadow: 0px 2px 4px rgba(0,0,0,0.5);
            border: 1px solid #333;
            letter-spacing: 1px;
        }
        .channel-name {
            font-size: 0.95rem;
            font-weight: 600;
            color: #e0e0e0;
            word-break: break-word;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        /* Hidden video container designed for strict fullscreen presentation */
        #video-container {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #000;
            z-index: 9999;
        }
        video {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        .booster-container {
            position: absolute;
            top: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(30, 30, 30, 0.85);
            padding: 10px 20px;
            border-radius: 50px;
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 15px;
            color: #fff;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s, visibility 0.3s;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .booster-container.show, .booster-container:hover {
            opacity: 1;
            visibility: visible;
        }
        
        /* Ad Container */
        #ad-container {
            position: absolute;
            bottom: 110px;
            left: 0;
            width: 100%;
            z-index: 10001;
            height: 120px;
            box-shadow: 0 -4px 15px rgba(0,0,0,0.5);
            transition: opacity 0.5s, visibility 0.5s;
            background: #000;
        }
        #ad-container.hidden {
            opacity: 0;
            visibility: hidden;
        }
        #ad-image {
            width: 100%;
            height: 120px;
            object-fit: fill;
            display: block;
        }
        .booster-container input[type=range] {
            -webkit-appearance: none;
            width: 120px;
            height: 6px;
            background: #555;
            border-radius: 3px;
            outline: none;
        }
        .booster-container input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #fff;
            cursor: pointer;
        }
        .booster-icon {
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            min-width: 70px;
        }
        #player-viewer-count {
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 10001;
            background: rgba(0,0,0,0.6);
            transition: opacity 0.5s;
        }
        
        /* Mobile & Tablet Responsiveness */
        @media (max-width: 768px) {
            .header-container { flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 15px; }
            h1 { font-size: 1.8rem; width: 100%; }
            .viewer-count { position: static; transform: none; margin: 0 auto; width: fit-content; font-size: 0.85rem;}
            .controls-row { flex-direction: column; width: 100%; gap: 10px; }
            .filter-group { width: 100%; justify-content: center; flex-wrap: wrap; }
            .contact-info { text-align: center; font-size: 0.85rem; margin-top: 0; }
            .search-box { width: 100%; }
            select.search-box { width: 100%; }
            .grid-container { grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 10px; }
            .channel-card { padding: 10px; }
            .channel-logo { width: 70px; height: 70px; }
            .channel-logo-text { width: 70px; height: 70px; font-size: 1.8rem; }
            .category-header { font-size: 1.4rem; text-align: center; }
            #player-viewer-count { top: 60px; right: 10px; font-size: 0.75rem; padding: 4px 8px;}
            .booster-container { top: 10px; padding: 5px 10px; transform: translateX(-50%) scale(0.8); }
            #ad-container { height: 90px; bottom: 80px; }
            #ad-image { height: 90px; }
            .close-btn { top: 10px; right: 10px; width: 35px; height: 35px; font-size: 1.2rem; }
        }
    </style>
</head>
<body>

    <div class="header-container">
        <h1>🌍 Universal Live TV</h1>
        <div id="main-viewer-count" class="viewer-count">110014 Live Watching Worldwide</div>
        <div class="controls-row">
            <div class="filter-group">
                <span class="filter-label">Select Country:</span>
                <select id="countrySelect" class="search-box"></select>
            </div>
            <input type="text" id="searchInput" class="search-box" placeholder="Search for a channel...">
        </div>
        <div class="contact-info">
            For advertisement contact <a href="mailto:godai6937@gmail.com" onclick="navigator.clipboard.writeText('godai6937@gmail.com'); alert('Email address copied to clipboard!');">godai6937@gmail.com</a>
        </div>
    </div>
    
    <div id="loadingOverlay">
        <div class="spinner"></div>
        <p id="loadingText" style="font-size: 1.2rem; margin-top: 15px;">Connecting to Global Database...</p>
        <div class="progress-bar-container">
            <div id="progressBar"></div>
        </div>
    </div>

    <div class="grid-wrapper" id="grid-wrapper"></div>

    <div id="video-container">
        <div id="player-viewer-count" class="viewer-count">110014 Live Watching Worldwide</div>
        <div class="booster-container" title="Audio Booster">
            <span class="booster-icon" id="boostValue">🔊 100%</span>
            <input type="range" id="volumeBooster" min="1" max="5" step="0.1" value="1">
        </div>
        <div id="ad-container" class="hidden">
            <a id="ad-link" href="#" target="_blank">
                <img id="ad-image" src="" alt="Advertisement">
            </a>
        </div>
        <video id="videoPlayer" crossorigin="anonymous" controls autoplay playsinline webkit-playsinline></video>
    </div>

    <script>
        let allChannels = [];
        let activeData = [];
        let deadStreams = new Set();
        let currentLoadId = 0;

        const grid = document.getElementById('grid-wrapper');
        const countrySelect = document.getElementById('countrySelect');
        const searchInput = document.getElementById('searchInput');
        const loadingOverlay = document.getElementById('loadingOverlay');
        const loadingText = document.getElementById('loadingText');
        const progressBar = document.getElementById('progressBar');
        
        const videoContainer = document.getElementById('video-container');
        const video = document.getElementById('videoPlayer');
        let hls = null;

        // Clean Channel Names
        function cleanName(rawName, countryCode) {
            let name = rawName.replace(/\s*\(\s*[a-zA-Z]{2}\s*\)/gi, '')
                              .replace(/\s*\[\s*[a-zA-Z]{2}\s*\]/gi, '');
            const upperCode = countryCode.toUpperCase();
            if (name.endsWith(" " + upperCode)) name = name.slice(0, -(upperCode.length + 1));
            if (name.startsWith(upperCode + " ")) name = name.substring(upperCode.length + 1);
            return name.trim();
        }

        // Indian Sorting Logic
        function applyIndianSorting(channels) {
            const getCategoryAndRank = (name) => {
                const n = name.toLowerCase();
                
                // Combines Premium TRP leaders + Top Free TRP leaders
                const topFamous = [
                    "star plus", "sony entertainment", "zee tv", "colors tv", "sun tv", "star maa", "star jalsha", "asianet", "zee kannada", "star vijay", "sony sab", "zee marathi", "star pravah", "dangal",
                    "aaj tak", "india tv", "abp news", "republic bharat", "ndtv india", "zee news", "news18 india", "tv9 bharatvarsh", "shemaroo", "goldmines", "dd national", "dd sports", "b4u"
                ];
                
                if (topFamous.some(t => n.includes(t))) return { cat: "Top 14 / Popular", rank: 0.5 };
                
                const main_ent = ["zee", "star", "sony", "colors", "sab", "set", "and tv", "&tv", "utsav"];
                const movies = ["movie", "cinema", "picture", "max", "gold", "action", "pix", "hbo", "star movies"];
                const music = ["music", "mtv", "zing", "vh1", "9xm", "b4u", "jalsha movies", "mastiii"];
                const news = ["news", "aaj tak", "abp", "ndtv", "republic", "times now", "cnn", "bbc", "wion", "india tv", "news18"];
                const kids = ["cartoon", "pogo", "nick", "disney", "hungama", "animax", "discovery kids"];
                const sports = ["sport", "star sports", "ten", "espn", "sony six", "dd sports"];
                
                if (news.some(x => n.includes(x))) return { cat: "News", rank: 5 };
                if (sports.some(x => n.includes(x))) return { cat: "Sports", rank: 6 };
                if (kids.some(x => n.includes(x))) return { cat: "Kids", rank: 4 };
                if (movies.some(x => n.includes(x))) return { cat: "Movies", rank: 2 };
                if (music.some(x => n.includes(x))) return { cat: "Music", rank: 3 };
                if (main_ent.some(x => n.includes(x))) return { cat: "Entertainment", rank: 1 };
                return { cat: "Other", rank: 99 };
            };

            const getLanguageRank = (name) => {
                const n = name.toLowerCase();
                const regional = ["tamil", "telugu", "kannada", "malayalam", "marathi", "bengali", "odia", "punjabi", "gujarati", "bhojpuri", "assamese", "sun tv", "asianet", "star maa", "star jalsha"];
                const english = ["english", "star world", "comedy central", "hbo", "romedy", "movies now", "mnx", "bbc", "cnn", "wion", "times now"];
                if (regional.some(x => n.includes(x))) return 3;
                if (english.some(x => n.includes(x))) return 2;
                return 1;
            };

            channels.forEach(c => {
                if (c.url.startsWith("premium:")) {
                    c.category = "Top";
                    c.rank = 0.5;
                    c.lang_rank = 1;
                } else {
                    const info = getCategoryAndRank(c.name);
                    c.category = info.cat;
                    c.rank = info.rank;
                    c.lang_rank = getLanguageRank(c.name);
                }
            });

            channels.sort((a, b) => {
                if (a.rank !== b.rank) return a.rank - b.rank;
                if (a.lang_rank !== b.lang_rank) return a.lang_rank - b.lang_rank;
                return a.name.localeCompare(b.name);
            });
        }

        async function initApp() {
            try {
                const res = await fetch('https://iptv-org.github.io/api/countries.json');
                const countries = await res.json();
                
                countries.sort((a, b) => a.name.localeCompare(b.name));
                countries.forEach(c => {
                    const opt = document.createElement('option');
                    opt.value = c.code.toLowerCase();
                    opt.textContent = c.name;
                    countrySelect.appendChild(opt);
                });

                let userCountry = "in";
                try {
                    const geoRes = await fetch('https://get.geojs.io/v1/ip/country.json');
                    if (geoRes.ok) {
                        const geoData = await geoRes.json();
                        if (geoData && geoData.country) {
                            const detectedCode = geoData.country.toLowerCase();
                            if (countries.some(c => c.code.toLowerCase() === detectedCode)) {
                                userCountry = detectedCode;
                            }
                        }
                    }
                } catch (e) {
                    console.log("Geo location fallback to IN");
                }

                countrySelect.value = userCountry;
                countrySelect.addEventListener('change', (e) => loadCountry(e.target.value));
                loadCountry(userCountry);
            } catch (err) {
                loadingText.textContent = "Error connecting to database.";
            }
        }

        async function checkStream(url) {
            try {
                const controller = new AbortController();
                const id = setTimeout(() => controller.abort(), 2500);
                const res = await fetch(url, { method: 'GET', signal: controller.signal });
                clearTimeout(id);
                
                if (!res.ok && res.status !== 206) {
                    controller.abort();
                    return false;
                }
                
                // Read just the first chunk to prevent downloading the whole video/playlist
                const reader = res.body.getReader();
                const { value } = await reader.read();
                reader.cancel();
                controller.abort(); 
                
                if (!value) return false;
                
                const text = new TextDecoder().decode(value);
                if (text.includes("#EXTM3U")) return true;
                
                const cType = res.headers.get('content-type');
                if (cType && (cType.includes('video') || cType.includes('mpegurl') || cType.includes('stream'))) return true;
                
                return false;
            } catch {
                return false;
            }
        }

        async function loadCountry(code) {
            currentLoadId++;
            const myLoadId = currentLoadId;
            
            loadingOverlay.classList.remove('hidden');
            progressBar.style.width = "0%";
            loadingText.textContent = `Fetching channel manifest for ${countrySelect.options[countrySelect.selectedIndex].text}...`;
            grid.innerHTML = "";
            allChannels = [];
            activeData = [];
            deadStreams.clear();
            searchInput.value = "";

            try {
                const url = `https://iptv-org.github.io/iptv/countries/${code}.m3u`;
                const res = await fetch(url);
                if (!res.ok) throw new Error("No channels available for this region.");
                const text = await res.text();
                
                const lines = text.split('\\n');
                let rawChannels = [];
                let currentLogo = "";
                let currentCategory = "Other";
                let currentName = "Live Channel";

                lines.forEach(line => {
                    line = line.trim();
                    if (line.startsWith("#EXTINF")) {
                        const lgMatch = line.match(/tvg-logo="([^"]+)"/);
                        currentLogo = lgMatch ? lgMatch[1] : "";
                        const catMatch = line.match(/group-title="([^"]+)"/);
                        currentCategory = catMatch && catMatch[1].trim() !== "" ? catMatch[1] : "Other";
                        const rawName = line.split(',').pop() || "Live Channel";
                        currentName = cleanName(rawName, code);
                    } else if (line.startsWith("http")) {
                        rawChannels.push({
                            name: currentName, logo: currentLogo,
                            category: currentCategory, url: line
                        });
                    }
                });

                // Pre-sort raw channels to prioritize the most important ones for the first 100 checks
                if (code === "in") {
                    applyIndianSorting(rawChannels);
                } else {
                    rawChannels.sort((a, b) => {
                        if (a.category === b.category) return a.name.localeCompare(b.name);
                        if (a.category === "Other") return 1;
                        if (b.category === "Other") return -1;
                        return a.category.localeCompare(b.category);
                    });
                }

                const initialBatchSize = Math.min(100, rawChannels.length);
                const validChannels = [];

                // Synchronously test first 100 for the initial UI
                loadingText.textContent = `Verifying top channels (0/${initialBatchSize})...`;
                for (let i = 0; i < initialBatchSize; i += 40) {
                    if (myLoadId !== currentLoadId) return; // User switched country, abort
                    const batch = rawChannels.slice(i, Math.min(i + 40, initialBatchSize));
                    const results = await Promise.all(batch.map(c => checkStream(c.url)));
                    batch.forEach((c, idx) => { if (results[idx]) validChannels.push(c); });
                    
                    const progress = Math.min(i + 40, initialBatchSize);
                    loadingText.textContent = `Verifying top channels (${progress}/${initialBatchSize})...`;
                    progressBar.style.width = `${(progress / initialBatchSize) * 100}%`;
                }

                if (myLoadId !== currentLoadId) return; // User switched country during batch, abort

                // Render the first batch and hide loader immediately
                allChannels = [...validChannels];
                activeData = [...allChannels];
                renderGrid(activeData);
                loadingOverlay.classList.add('hidden');

                // Process remaining streams in the background silently
                if (rawChannels.length > initialBatchSize) {
                    (async function processBackground() {
                        for (let i = initialBatchSize; i < rawChannels.length; i += 40) {
                            if (myLoadId !== currentLoadId) return; // User switched country, abort background loop
                            const batch = rawChannels.slice(i, Math.min(i + 40, rawChannels.length));
                            const results = await Promise.all(batch.map(c => checkStream(c.url)));
                            
                            if (myLoadId !== currentLoadId) return; // Double check after await
                            
                            let added = false;
                            
                            batch.forEach((c, idx) => {
                                if (results[idx] && !deadStreams.has(c.url)) {
                                    validChannels.push(c);
                                    added = true;
                                }
                            });

                            if (added) {
                                // Filter out any streams that died while we were processing
                                const currentValid = validChannels.filter(c => !deadStreams.has(c.url));
                                
                                // Re-sort array
                                if (code === "in") {
                                    applyIndianSorting(currentValid);
                                } else {
                                    currentValid.sort((a, b) => {
                                        if (a.category === b.category) return a.name.localeCompare(b.name);
                                        if (a.category === "Other") return 1;
                                        if (b.category === "Other") return -1;
                                        return a.category.localeCompare(b.category);
                                    });
                                }
                                allChannels = [...currentValid];
                                
                                // Re-render gracefully without breaking search
                                const query = searchInput.value.toLowerCase();
                                activeData = query ? allChannels.filter(c => c.name.toLowerCase().includes(query)) : allChannels;
                                renderGrid(activeData);
                            }
                        }
                    })();
                }

            } catch (err) {
                grid.innerHTML = `<p style='text-align:center; color:#ff4757; font-size:1.2rem; margin-top:50px;'>${err.message}</p>`;
                loadingOverlay.classList.add('hidden');
            }
        }

        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            activeData = allChannels.filter(c => c.name.toLowerCase().includes(query));
            renderGrid(activeData);
        });

        function renderGrid(data) {
            grid.innerHTML = "";
            if(data.length === 0) {
                grid.innerHTML = "<p style='text-align:center;'>No verified channels found.</p>";
                return;
            }
            let currentCategory = "";
            let currentGrid = null;
            data.forEach(chan => {
                if (chan.category && chan.category !== currentCategory) {
                    currentCategory = chan.category;
                    const header = document.createElement('h2');
                    header.className = 'category-header';
                    header.innerText = currentCategory;
                    grid.appendChild(header);
                    currentGrid = document.createElement('div');
                    currentGrid.className = 'grid-container';
                    grid.appendChild(currentGrid);
                }
                const card = document.createElement('div');
                card.className = 'channel-card';
                card.onclick = () => playStream(chan.url);
                
                // Generate a 1-2 letter acronym for the logo fallback
                const words = chan.name.replace(/[^a-zA-Z0-9 ]/g, '').split(' ').filter(w => w.length > 0);
                let acronym = "TV";
                if (words.length >= 2) acronym = (words[0][0] + words[1][0]).toUpperCase();
                else if (words.length === 1) acronym = words[0].substring(0, 2).toUpperCase();
                
                let logoHtml = '';
                if (chan.logo && chan.logo.trim() !== "") {
                    logoHtml = `<img class="channel-logo" src="${chan.logo}" onerror="this.outerHTML='<div class=\\'channel-logo-text\\'>${acronym}</div>'" alt="logo">`;
                } else {
                    logoHtml = `<div class="channel-logo-text">${acronym}</div>`;
                }

                card.innerHTML = `
                    ${logoHtml}
                    <div class="channel-name">${chan.name}</div>
                `;
                currentGrid.appendChild(card);
            });
        }

        function handleDeadStream(url) {
            closePlayer();
            
            // Mark stream as dead globally so background processes don't add it back
            deadStreams.add(url);
            
            // Remove the dead channel from our arrays
            allChannels = allChannels.filter(c => c.url !== url);
            activeData = activeData.filter(c => c.url !== url);
            renderGrid(activeData);
            
            // Show a temporary red toast notification instead of an alert
            const toast = document.createElement('div');
            toast.textContent = "Stream is currently offline. Channel has been temporarily removed from your grid.";
            toast.style.cssText = "position:fixed; bottom:30px; left:50%; transform:translateX(-50%); background:#ff4757; color:#fff; padding:12px 24px; border-radius:30px; z-index:99999; font-weight:bold; box-shadow: 0 4px 15px rgba(0,0,0,0.5); text-align:center;";
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 3500);
        }

        function playStream(url) {
            // ... existing function implementation ...
            if (hls) { hls.destroy(); hls = null; }
            if (videoContainer.requestFullscreen) videoContainer.requestFullscreen().catch(err => console.log(err));
            else if (videoContainer.webkitRequestFullscreen) videoContainer.webkitRequestFullscreen();
            if (video.webkitEnterFullscreen) video.webkitEnterFullscreen();

            videoContainer.style.display = "block";
            showBooster();
            loadAd();

            if (typeof Hls !== 'undefined' && Hls.isSupported()) {
                hls = new Hls({ abrEwmaDefaultEstimate: 5000000 });
                hls.loadSource(url);
                hls.attachMedia(video);
                hls.on(Hls.Events.MANIFEST_PARSED, function() {
                    video.play().catch(e => console.error("Autoplay prevented:", e));
                });
                hls.on(Hls.Events.ERROR, function(event, data) {
                    if (data.fatal) {
                        console.error("Stream error:", data);
                        handleDeadStream(url);
                    }
                });
            } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = url;
                video.addEventListener('loadedmetadata', function() {
                    video.play().catch(e => console.error("Autoplay prevented:", e));
                });
                video.onerror = () => {
                    handleDeadStream(url);
                };
            }
        }

        function closePlayer() {
            if (document.fullscreenElement) document.exitFullscreen().catch(e => console.log(e));
            videoContainer.style.display = "none";
            document.getElementById('ad-container').classList.add('hidden');
            video.pause();
            video.removeAttribute('src');
            video.load();
            if (hls) { hls.destroy(); hls = null; }
        }

        function monitorFullScreenChange() {
            if (!document.fullscreenElement && !document.webkitIsFullScreen && !document.mozFullScreen && !document.msFullscreenElement) {
                closePlayer();
            }
        }

        document.addEventListener('fullscreenchange', monitorFullScreenChange);
        document.addEventListener('webkitfullscreenchange', monitorFullScreenChange);
        document.addEventListener('mozfullscreenchange', monitorFullScreenChange);
        document.addEventListener('MSFullscreenChange', monitorFullScreenChange);
        video.addEventListener('webkitendfullscreen', closePlayer);

        let audioCtx, gainNode, sourceNode;
        const boosterInput = document.getElementById('volumeBooster');
        const boostValue = document.getElementById('boostValue');
        const boosterContainer = document.querySelector('.booster-container');
        let hideTimeout;

        function showBooster() {
            boosterContainer.classList.add('show');
            clearTimeout(hideTimeout);
            hideTimeout = setTimeout(() => { boosterContainer.classList.remove('show'); }, 3000);
        }

        videoContainer.addEventListener('mousemove', showBooster);
        videoContainer.addEventListener('touchstart', showBooster);
        videoContainer.addEventListener('click', showBooster);

        function initAudioBooster() {
            if (audioCtx) return;
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            audioCtx = new AudioContext();
            sourceNode = audioCtx.createMediaElementSource(video);
            gainNode = audioCtx.createGain();
            sourceNode.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            boosterInput.addEventListener('input', function(e) {
                const val = parseFloat(e.target.value);
                gainNode.gain.value = val;
                boostValue.innerText = `🔊 ${Math.round(val * 100)}%`;
            });
        }

        video.addEventListener('play', () => {
            initAudioBooster();
            if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
        });
        
        let adShowTimer = null;
        let adHideTimer = null;
        async function loadAd() {
            try {
                const res = await fetch('/api/ad');
                const adData = await res.json();
                if (adData.ad_enabled && adData.ad_image_url) {
                    const adContainer = document.getElementById('ad-container');
                    const adImage = document.getElementById('ad-image');
                    const adLink = document.getElementById('ad-link');
                    
                    adImage.src = adData.ad_image_url;
                    if (adData.ad_target_link) {
                        adLink.onclick = (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            let target = adData.ad_target_link;
                            if (!target.startsWith('http://') && !target.startsWith('https://')) {
                                target = 'https://' + target;
                            }
                            window.open(target, '_blank');
                        };
                        adLink.style.cursor = "pointer";
                    } else {
                        adLink.onclick = (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                        };
                        adLink.style.cursor = "default";
                    }
                    
                    clearTimeout(adShowTimer);
                    clearTimeout(adHideTimer);
                    
                    const showDelay = (adData.ad_start_delay_seconds || 0) * 1000;
                    
                    adShowTimer = setTimeout(() => {
                        adContainer.classList.remove('hidden');
                        
                        if (adData.ad_auto_hide_seconds > 0) {
                            adHideTimer = setTimeout(() => {
                                adContainer.classList.add('hidden');
                            }, adData.ad_auto_hide_seconds * 1000);
                        }
                    }, showDelay);
                }
            } catch (e) {
                console.error("No ad server found or ad failed to load:", e);
            }
        }

        let playerIdleTimer;
        videoContainer.addEventListener('mousemove', () => {
            const pvc = document.getElementById('player-viewer-count');
            pvc.style.opacity = '1';
            clearTimeout(playerIdleTimer);
            playerIdleTimer = setTimeout(() => {
                pvc.style.opacity = '0';
            }, 3000);
        });
        
        let viewerId = localStorage.getItem('tv_viewer_id');
        if (!viewerId) {
            viewerId = Math.random().toString(36).substring(2, 15);
            localStorage.setItem('tv_viewer_id', viewerId);
        }

        async function pingViewers() {
            try {
                const res = await fetch('/api/ping', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ viewer_id: viewerId })
                });
                const data = await res.json();
                const text = `${data.viewers} Live Watching Worldwide`;
                document.getElementById('main-viewer-count').innerText = text;
                document.getElementById('player-viewer-count').innerText = text;
            } catch (e) { }
        }
        setInterval(pingViewers, 10000);
        pingViewers();

        initApp();
    </script>
</body>
</html>
"""

import json
import time
import os
from flask import Flask, render_template_string, jsonify, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
DEFAULT_CONFIG = {
    "password": generate_password_hash("admin"),
    "ad_enabled": False,
    "ad_image_url": "",
    "ad_target_link": "",
    "ad_start_delay_seconds": 0,
    "ad_auto_hide_seconds": 10
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        pw = config.get("password", "")
        if not pw.startswith("pbkdf2:") and not pw.startswith("scrypt:"):
            config["password"] = generate_password_hash(pw if pw else "admin")
            save_config(config)
        return config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

active_viewers = {}

@app.route('/api/ping', methods=['POST'])
def ping():
    data = request.json or {}
    viewer_id = data.get('viewer_id')
    if viewer_id:
        active_viewers[viewer_id] = time.time()
        
    current_time = time.time()
    for vid in list(active_viewers.keys()):
        if current_time - active_viewers[vid] > 30:
            del active_viewers[vid]
            
    return jsonify({"viewers": 110013 + len(active_viewers)})

admin_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #121212; color: #fff; padding: 20px; }
        .card { background: #1e1e1e; padding: 30px; border-radius: 12px; max-width: 500px; margin: 50px auto; border: 1px solid #333;}
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="number"], input[type="password"] { width: 100%; padding: 12px; margin: 5px 0 20px 0; border-radius: 5px; border: 1px solid #444; background: #2a2a2a; color: white; box-sizing: border-box; }
        button { background: #ff4757; color: #fff; cursor: pointer; font-weight: bold; width: 100%; padding: 15px; border: none; border-radius: 5px; font-size: 16px;}
        h2 { color: #ff4757; margin-top: 0; }
        .help { font-size: 0.85rem; color: #aaa; margin-top: 0; display: block; margin-bottom: 10px;}
    </style>
</head>
<body>
    <div class="card">
        <h2>Ad Dashboard</h2>
        {% if msg %}<p style="color:#2ecc71; font-weight:bold;">{{ msg }}</p>{% endif %}
        <form method="POST">
            <label style="font-size: 1.1rem; display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
                <input type="checkbox" name="ad_enabled" {% if config.ad_enabled %}checked{% endif %} style="width: 20px; height: 20px;">
                Enable Advertisement
            </label>
            
            <label>Image or GIF URL:</label>
            <input type="text" name="ad_image_url" value="{{ config.ad_image_url }}" placeholder="https://example.com/ad.gif">
            
            <label>Target Click Link (optional):</label>
            <input type="text" name="ad_target_link" value="{{ config.ad_target_link }}" placeholder="https://advertiser.com">
            
            <label>Start Delay (seconds):</label>
            <span class="help">How long to wait before showing the ad (0 = instantly).</span>
            <input type="number" name="ad_start_delay_seconds" value="{{ config.ad_start_delay_seconds }}">
            
            <label>Auto-Hide Timer (seconds):</label>
            <span class="help">Set to 0 if you want the ad to stay permanently until closed.</span>
            <input type="number" name="ad_auto_hide_seconds" value="{{ config.ad_auto_hide_seconds }}">
            
            <label>Change Admin Password:</label>
            <input type="password" name="password" placeholder="Leave empty to keep current">
            
            <button type="submit">Save Advertisement</button>
        </form>
    </div>
</body>
</html>
"""

login_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #121212; color: #fff; padding: 50px; }
        .card { background: #1e1e1e; padding: 30px; border-radius: 12px; max-width: 300px; margin: 0 auto; text-align: center; border: 1px solid #333;}
        input, button { width: 100%; padding: 12px; margin: 10px 0; border-radius: 5px; border: none; box-sizing: border-box; }
        input { background: #2a2a2a; color: white; border: 1px solid #444; }
        button { background: #ff4757; color: #fff; cursor: pointer; font-weight: bold; font-size: 16px;}
        h2 { color: #ff4757; margin-top: 0;}
    </style>
</head>
<body>
    <div class="card">
        <h2>Admin Login</h2>
        <form method="POST">
            <input type="password" name="password" placeholder="Enter Password" required>
            <button type="submit">Login</button>
            {% if error %}<p style="color:#ff4757; font-weight:bold; margin-top: 15px;">{{ error }}</p>{% endif %}
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/api/ad')
def api_ad():
    return jsonify(load_config())

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    config = load_config()
    if 'logged_in' not in session:
        if request.method == 'POST':
            if check_password_hash(config['password'], request.form.get('password', '')):
                session['logged_in'] = True
                return redirect('/admin')
            else:
                return render_template_string(login_template, error="Invalid password!")
        return render_template_string(login_template)
    
    if request.method == 'POST':
        config['ad_enabled'] = 'ad_enabled' in request.form
        config['ad_image_url'] = request.form.get('ad_image_url', '')
        config['ad_target_link'] = request.form.get('ad_target_link', '')
        try:
            config['ad_start_delay_seconds'] = int(request.form.get('ad_start_delay_seconds', 0))
        except:
            config['ad_start_delay_seconds'] = 0
            
        try:
            config['ad_auto_hide_seconds'] = int(request.form.get('ad_auto_hide_seconds', 0))
        except:
            config['ad_auto_hide_seconds'] = 0
            
        new_pass = request.form.get('password', '')
        if new_pass:
            config['password'] = generate_password_hash(new_pass)
            
        save_config(config)
        return render_template_string(admin_template, config=config, msg="Advertisement Settings Saved!")
        
    return render_template_string(admin_template, config=config)

if __name__ == '__main__':
    print("Starting Universal TV Admin & Ad Server...")
    print("Open http://127.0.0.1:5000 in your browser to view the player.")
    print("Open http://127.0.0.1:5000/admin to configure advertisements.")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
