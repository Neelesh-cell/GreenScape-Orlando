const https = require('https');
const fs = require('fs');

const pexelsImages = {
    // Landscape Design Orlando (3D/elegant native plants) -> front yard landscaping design
    'images/landscaping/landscape-design.jpg': 'https://images.pexels.com/photos/5998131/pexels-photo-5998131.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', // formal garden beds / native plants design
    
    // Tree & Shrub Care (professional trimming pruning) -> arborist/pruning
    'images/landscaping/tree-care.jpg': 'https://images.pexels.com/photos/4503269/pexels-photo-4503269.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', // professional landscaper pruning shrub
    
    // Premium Sod Installation (laying new sod grass) -> new pristine lawn installation
    'images/landscaping/sod-installation.jpg': 'https://images.pexels.com/photos/6157144/pexels-photo-6157144.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', // perfect new green grass/lawn laying
    
    // Complete Backyard Makeover (full overhaul modern oasis)
    'images/landscaping/portfolio-1.jpg': 'https://images.pexels.com/photos/32870/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', // luxury backyard makeover pool/decking
    
    // Paver Walkways & Retaining Walls (structured hardscaping) 
    'images/landscaping/portfolio-3.jpg': 'https://images.pexels.com/photos/1080721/pexels-photo-1080721.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', // elegant stone paver walkway
    
    // Tropical Garden Styling (vibrant drought-tolerant plants)
    'images/landscaping/tropical-garden.jpg': 'https://images.pexels.com/photos/2088204/pexels-photo-2088204.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', // lush vibrant tropical garden
    
    // Seasonal Floral Borders (curated seasonal flowers)
    'images/landscaping/portfolio-4.jpg': 'https://images.pexels.com/photos/1054432/pexels-photo-1054432.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2' // colorful bright floral borders/flowers
};

async function downloadDirect() {
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

downloadDirect();
