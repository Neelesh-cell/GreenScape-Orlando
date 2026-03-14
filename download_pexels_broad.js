const https = require('https');
const fs = require('fs');

const apiKey = "1o070DORB01I1L1W3VvAOkYFv79D7T3IuI8o4F2Qz23jN5bLStAms7qE";

const queries = {
    'images/landscaping/tree-care.jpg': 'tree pruning',
    'images/landscaping/landscaper.jpg': 'landscaper'
};

// Also verify what downloaded previously for 'landscape-design.jpg' and 'portfolio-3.jpg'
// Because user said images don't match text. Let's force re-download these two with better terms just in case.
const forceQueries = {
    'images/landscaping/landscape-design.jpg': 'front yard landscaping garden',
    'images/landscaping/portfolio-3.jpg': 'backyard stone patio'
};

async function downloadPexels() {
    const allQueries = { ...queries, ...forceQueries };
    
    for (const [filename, query] of Object.entries(allQueries)) {
        if (queries[filename] && fs.existsSync(filename) && fs.statSync(filename).size > 10000) {
            console.log(`Skipping ${filename}`);
            continue;
        }

        console.log(`Searching Pexels for "${query}" -> ${filename}`);
        const searchUrl = `https://api.pexels.com/v1/search?query=${encodeURIComponent(query)}&per_page=1&orientation=landscape`;

        try {
            const data = await new Promise((resolve, reject) => {
                https.get(searchUrl, { headers: { 'Authorization': apiKey } }, (res) => {
                    let d = '';
                    res.on('data', chunk => d += chunk);
                    res.on('end', () => resolve(JSON.parse(d)));
                }).on('error', reject);
            });

            if (data.photos && data.photos.length > 0) {
                const imgUrl = Object.values(forceQueries).includes(query) 
                    ? (data.photos[0].src.large2x || data.photos[0].src.large)
                    : (data.photos[0].src.large || data.photos[0].src.original);
                
                console.log(`Downloading ${filename}...`);
                await new Promise((resolve, reject) => {
                    const file = fs.createWriteStream(filename);
                    https.get(imgUrl, (res) => {
                        res.pipe(file);
                        file.on('finish', () => { file.close(); resolve(); });
                    }).on('error', reject);
                });
            } else {
                console.log(`No images found for ${query}`);
            }
        } catch (e) {
            console.error(e.message);
        }
        await new Promise(r => setTimeout(r, 1500));
    }
}

downloadPexels();
