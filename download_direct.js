const https = require('https');
const fs = require('fs');

const pexelsImages = {
    'images/landscaping/landscape-design.jpg': 'https://images.pexels.com/photos/1080721/pexels-photo-1080721.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', // beautiful garden path
    'images/landscaping/tree-care.jpg': 'https://images.pexels.com/photos/3160469/pexels-photo-3160469.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', // cutting/pruning outdoors
    'images/landscaping/landscaper.jpg': 'https://images.pexels.com/photos/4503273/pexels-photo-4503273.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', // person gardening/planting
    'images/landscaping/portfolio-3.jpg': 'https://images.pexels.com/photos/2253456/pexels-photo-2253456.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', // luxury backyard stone patio
    'images/map.jpg': 'https://images.pexels.com/photos/2088210/pexels-photo-2088210.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2' // green nature background (fallback for map illustration)
};

async function downloadFallback() {
    for (const [filename, url] of Object.entries(pexelsImages)) {
        console.log(`Downloading direct to ${filename}`);
        await new Promise((resolve, reject) => {
            const file = fs.createWriteStream(filename);
            https.get(url, (res) => {
                res.pipe(file);
                file.on('finish', () => { file.close(); resolve(); });
            }).on('error', reject);
        });
        console.log(`Saved ${filename}`);
    }
}

downloadFallback();
