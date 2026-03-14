const https = require('https');
const fs = require('fs');
const path = require('path');

// Public Pexels API Key
const apiKey = "1o070DORB01I1L1W3VvAOkYFv79D7T3IuI8o4F2Qz23jN5bLStAms7qE";

const queries = {
    'images/landscaping/landscape-design.jpg': 'garden landscape front yard residential',
    'images/landscaping/tree-care.jpg': 'tree pruning worker landscaping arborist',
    'images/landscaping/landscaper.jpg': 'landscaper planting flowers worker',
    'images/landscaping/portfolio-1.jpg': 'elegant walkway front yard landscaping',
    'images/landscaping/portfolio-2.jpg': 'modern outdoor living space patio backyard design',
    'images/landscaping/portfolio-3.jpg': 'stone paver walkway garden installation landscaping',
    'images/landscaping/portfolio-4.jpg': 'colorful floral garden bed landscape residential',
    'images/map.jpg': 'florida map stylized outline graphic green'
};

async function downloadPexels() {
    for (const [filename, query] of Object.entries(queries)) {
        if (fs.existsSync(filename) && fs.statSync(filename).size > 10000) {
            console.log(`Skipping ${filename}, valid file already exists.`);
            continue;
        }

        console.log(`Searching Pexels for "${query}" -> ${filename}`);

        const searchUrl = `https://api.pexels.com/v1/search?query=${encodeURIComponent(query)}&per_page=1&orientation=landscape`;

        try {
            const data = await new Promise((resolve, reject) => {
                https.get(searchUrl, {
                    headers: { 'Authorization': apiKey }
                }, (res) => {
                    let d = '';
                    res.on('data', chunk => d += chunk);
                    res.on('end', () => resolve(JSON.parse(d)));
                }).on('error', reject);
            });

            if (data.photos && data.photos.length > 0) {
                const imgUrl = data.photos[0].src.large2x || data.photos[0].src.large;
                console.log(`Downloading image from ${imgUrl}...`);
                
                await new Promise((resolve, reject) => {
                    const file = fs.createWriteStream(filename);
                    https.get(imgUrl, (res) => {
                        res.pipe(file);
                        file.on('finish', () => {
                            file.close();
                            resolve();
                        });
                    }).on('error', (err) => {
                        fs.unlink(filename, () => {});
                        reject(err);
                    });
                });
                console.log(`Successfully saved ${filename}`);
            } else {
                console.log(`No images found on Pexels for ${query}`);
            }
        } catch (e) {
            console.error(`Error processing ${filename}:`, e.message);
        }
        
        // Respect API rate limits
        await new Promise(r => setTimeout(r, 2000));
    }
}

downloadPexels();
