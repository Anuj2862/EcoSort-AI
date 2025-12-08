
# Dataset Preparation Instructions

## Current Status
- Directory structure created for 10 categories
- TrashNet dataset downloaded (if available)

## Categories Needing More Images:
- food_waste (organic matter, fruits, vegetables)
- e_waste (electronics, batteries, circuits)
- textiles (clothing, fabrics, shoes)
- hazardous (chemicals, paint, cleaning products)
- medical (masks, syringes, medical supplies)

## How to Add Images:

### Option 1: Manual Collection
1. Download images from Google Images
2. Place in respective category folders
3. Aim for 500+ images per category

### Option 2: Use Kaggle Datasets
1. Search "waste classification" on Kaggle
2. Download relevant datasets
3. Organize into category folders

### Option 3: Web Scraping
1. Use the provided scraper script
2. Run: python scrape_images.py
3. Review and clean scraped images

## Recommended Dataset Sources:
- Kaggle: "Waste Classification Dataset"
- Google Open Images
- TACO Dataset (for specific categories)
- Custom photography

## Quality Guidelines:
- Clear, well-lit images
- Various angles and backgrounds
- Mix of indoor/outdoor shots
- Different lighting conditions
- Avoid duplicates
