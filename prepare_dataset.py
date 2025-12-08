"""
Dataset Download and Preparation Script
Downloads public waste classification datasets and organizes them into 10 categories
"""

import os
import urllib.request
import zipfile
import shutil
from pathlib import Path

# Create dataset directory structure
DATASET_DIR = 'dataset'
CATEGORIES = [
    'metal',
    'glass',
    'plastic',
    'paper',
    'food_waste',
    'e_waste',
    'textiles',
    'hazardous',
    'medical',
    'general_trash'
]

def create_directory_structure():
    """Create organized directory structure for dataset"""
    print("📁 Creating directory structure...")
    
    for category in CATEGORIES:
        category_path = os.path.join(DATASET_DIR, category)
        os.makedirs(category_path, exist_ok=True)
        print(f"  ✅ Created: {category_path}")
    
    print("\n✅ Directory structure created!\n")

def download_trashnet():
    """Download TrashNet dataset"""
    print("📥 Downloading TrashNet dataset...")
    
    url = "https://github.com/garythung/trashnet/archive/master.zip"
    zip_path = "trashnet.zip"
    
    try:
        print("  Downloading from GitHub...")
        urllib.request.urlretrieve(url, zip_path)
        print("  ✅ Downloaded!")
        
        print("  Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("temp_trashnet")
        print("  ✅ Extracted!")
        
        # Map TrashNet categories to our categories
        trashnet_mapping = {
            'metal': 'metal',
            'glass': 'glass',
            'plastic': 'plastic',
            'paper': 'paper',
            'cardboard': 'paper',
            'trash': 'general_trash'
        }
        
        # Move files to our structure
        print("  Organizing files...")
        trashnet_data_path = "temp_trashnet/trashnet-master/data"
        
        for trashnet_cat, our_cat in trashnet_mapping.items():
            src_path = os.path.join(trashnet_data_path, trashnet_cat)
            if os.path.exists(src_path):
                dest_path = os.path.join(DATASET_DIR, our_cat)
                for file in os.listdir(src_path):
                    shutil.copy2(
                        os.path.join(src_path, file),
                        os.path.join(dest_path, f"trashnet_{file}")
                    )
                print(f"    ✅ Copied {trashnet_cat} → {our_cat}")
        
        # Cleanup
        os.remove(zip_path)
        shutil.rmtree("temp_trashnet")
        
        print("\n✅ TrashNet dataset integrated!\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        print("  Skipping TrashNet - will use manual dataset\n")
        return False

def print_dataset_summary():
    """Print summary of collected dataset"""
    print("\n" + "="*50)
    print("📊 DATASET SUMMARY")
    print("="*50 + "\n")
    
    total_images = 0
    for category in CATEGORIES:
        category_path = os.path.join(DATASET_DIR, category)
        if os.path.exists(category_path):
            count = len([f for f in os.listdir(category_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
            total_images += count
            status = "✅" if count >= 100 else "⚠️"
            print(f"{status} {category:20s}: {count:4d} images")
    
    print("\n" + "-"*50)
    print(f"📈 TOTAL IMAGES: {total_images}")
    print("="*50 + "\n")
    
    if total_images < 1000:
        print("⚠️  WARNING: Dataset is small. Consider adding more images.")
        print("   Recommended: 500+ images per category\n")

def create_placeholder_note():
    """Create note about manual dataset addition"""
    note = """
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
"""
    
    with open('DATASET_README.md', 'w') as f:
        f.write(note)
    
    print("📝 Created DATASET_README.md with instructions\n")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 WASTE CLASSIFICATION DATASET PREPARATION")
    print("="*50 + "\n")
    
    # Step 1: Create structure
    create_directory_structure()
    
    # Step 2: Download TrashNet
    download_trashnet()
    
    # Step 3: Create instructions
    create_placeholder_note()
    
    # Step 4: Show summary
    print_dataset_summary()
    
    print("✅ Dataset preparation complete!")
    print("\n📌 Next Steps:")
    print("   1. Review DATASET_README.md")
    print("   2. Add more images to categories with < 500 images")
    print("   3. Run: python train_model.py")
    print()
