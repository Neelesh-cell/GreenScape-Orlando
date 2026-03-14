const https = require('https');
const fs = require('fs');
const path = require('path');

// direct image IDs from Pexels that match EXACTLY what the user wants. No search API needed.
const pexelsImages = {
    'images/landscaping/landscape-design.jpg': '287550', // front yard path
    'images/landscaping/tree-care.jpg': '4751996', // tree pruning arborist
    'images/landscaping/landscaper.jpg': '4132400', // landscaper working
    'images/landscaping/portfolio-3.jpg': '7543085', // nice stone walkway / patio
    'images/map.jpg': '3769165' // basic green graphic map representation
};

const apiKey = "1o070DORB01I1L1W3VvAOkYFv79D7T3IuI8o4F2Qz23jN5bLStAms7qE";

async function downloadDirect() {
    for (const [filepath, pexelsId] of Object.entries(pexelsImages)) {
        console.log(`Fetching Pexels Photo ID: ${pexelsId} -> ${filepath}`);
        
        try {
            // Get the photo details directly by ID
            const url = `https://api.pexels.com/v1/photos/${pexelsId}`;
            const photoData = await new Promise((resolve, reject) => {
                https.get(url, { headers: { 'Authorization': apiKey } }, (res) => {
                    let d = '';
                    res.on('data', chunk => d += chunk);
                    res.on('end', () => resolve(JSON.parse(d)));
                }).on('error', reject);
            });

            if (photoData.src) {
                // Use large size for web optimization
                const imgUrl = photoData.src.large2x || photoData.src.large;
                console.log(`Downloading ${imgUrl}`);

                await new Promise((resolve, reject) => {
                    // Ensure the directory exists
                    const dir = path.dirname(filepath);
                    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

                    const file = fs.createWriteStream(filepath);
                    https.get(imgUrl, (res) => {
                        res.pipe(file);
                        file.on('finish', () => { file.close(); resolve(); });
                    }).on('error', reject);
                });
                console.log(`Saved successfully!`);
            } else {
                console.log(`Failed to fetch ID ${pexelsId}`);
            }
        } catch (e) {
            console.error(`Error: ${e.message}`);
        }
        
        // short delay to prevent getting flagged
        await new Promise(r => setTimeout(r, 1000));
    }
}

downloadDirect();
