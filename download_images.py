"""
Image Downloader for Model 2 Dataset
Downloads images from Google Images for each category
Requires: google_images_download or manual collection
"""

import os
import requests
from pathlib import Path

# Dataset configuration
DATASET_DIR = 'dataset_model2'
CATEGORIES = {
    'food_waste': [
        'food waste compost',
        'organic waste',
        'fruit vegetable scraps',
        'spoiled food waste',
        'kitchen waste compost'
    ],
    'e_waste': [
        'electronic waste',
        'broken phone waste',
        'old laptop ewaste',
        'circuit board waste',
        'battery waste disposal'
    ],
    'textiles': [
        'textile waste',
        'old clothes waste',
        'fabric scraps waste',
        'torn clothing waste',
        'shoe waste disposal'
    ],
    'hazardous': [
        'hazardous waste container',
        'paint can waste',
        'chemical waste disposal',
        'pesticide container waste',
        'cleaning product waste'
    ],
    'medical': [
        'medical waste',
        'used mask waste',
        'syringe disposal',
        'medical glove waste',
        'biohazard waste'
    ]
}

print("\n" + "="*70)
print("📥 DATASET COLLECTION GUIDE FOR MODEL 2")
print("="*70 + "\n")

print("🎯 Target: 500+ images per category (2,500+ total)\n")
print("📂 Categories and Search Keywords:\n")

for category, keywords in CATEGORIES.items():
    print(f"📁 {category.upper()}")
    print(f"   Directory: {DATASET_DIR}/{category}/")
    print(f"   Keywords:")
    for kw in keywords:
        print(f"      • {kw}")
    print()

print("="*70)
print("🔍 COLLECTION METHODS")
print("="*70 + "\n")

print("METHOD 1: Kaggle Datasets (RECOMMENDED)")
print("-" * 70)
print("1. Visit: https://www.kaggle.com/datasets")
print("2. Search: 'waste classification' or specific category")
print("3. Download datasets:")
print("   • Food Waste Dataset")
print("   • E-Waste Classification")
print("   • Textile Waste")
print("4. Extract and organize into dataset_model2/ folders\n")

print("METHOD 2: Google Images (Manual)")
print("-" * 70)
print("1. Open Google Images")
print("2. Search using keywords above")
print("3. Download 100+ images per keyword")
print("4. Save to dataset_model2/{category}/")
print("5. Remove duplicates and low-quality images\n")

print("METHOD 3: Automated Download (Advanced)")
print("-" * 70)
print("Install: pip install bing-image-downloader")
print("Then run:")
print("""
from bing_image_downloader import downloader

for category, keywords in CATEGORIES.items():
    for keyword in keywords:
        downloader.download(
            keyword, 
            limit=100,
            output_dir=f'dataset_model2/{category}',
            adult_filter_off=True,
            force_replace=False
        )
""")
print()

print("="*70)
print("✅ QUALITY CHECKLIST")
print("="*70 + "\n")
print("Before training, ensure:")
print("  ✓ 500+ images per category")
print("  ✓ Clear, well-lit images")
print("  ✓ Various angles and backgrounds")
print("  ✓ No duplicates")
print("  ✓ Correct category placement")
print("  ✓ Mix of indoor/outdoor shots\n")

print("="*70)
print("📊 QUICK DATASET CHECK")
print("="*70 + "\n")

total = 0
for category in CATEGORIES.keys():
    path = Path(DATASET_DIR) / category
    if path.exists():
        count = len(list(path.glob('*.jpg'))) + len(list(path.glob('*.jpeg'))) + len(list(path.glob('*.png')))
        total += count
        status = "✅" if count >= 500 else "⚠️" if count >= 100 else "❌"
        print(f"{status} {category:15s}: {count:4d} images")
    else:
        print(f"❌ {category:15s}:    0 images (folder not found)")

print(f"\n📈 TOTAL: {total} images")
if total >= 2500:
    print("✅ Dataset ready for training!")
elif total >= 500:
    print("⚠️  Dataset small but usable for testing")
else:
    print("❌ Need more images - collect at least 500 total")

print("\n" + "="*70)
print("🚀 NEXT STEPS")
print("="*70)
print("\n1. Collect images using one of the methods above")
print("2. Verify image count: python download_images.py")
print("3. Train Model 2: python train_model2.py")
print("4. Wait ~30-60 minutes for training")
print("5. Test dual-model system!\n")

# Create a simple download helper
print("💡 TIP: For quick testing, start with 100 images per category")
print("   You can always add more and retrain later!\n")
