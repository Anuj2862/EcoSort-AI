"""
Fast Image Downloader for Model 2 Dataset
Uses Bing Image Search API (no authentication needed)
Downloads images automatically for all 5 categories
"""

from bing_image_downloader import downloader
import os

print("\n" + "="*70)
print("🚀 AUTOMATED IMAGE DOWNLOAD FOR MODEL 2")
print("="*70 + "\n")

print("📥 Installing bing-image-downloader...")
os.system("pip install bing-image-downloader -q")

print("\n✅ Starting download...\n")

# Download configuration
categories = {
    'food_waste': [
        'food waste compost',
        'organic waste bin',
        'fruit vegetable scraps'
    ],
    'e_waste': [
        'electronic waste recycling',
        'broken phone waste',
        'old laptop disposal'
    ],
    'textiles': [
        'textile waste recycling',
        'old clothes donation',
        'fabric waste bin'
    ],
    'hazardous': [
        'hazardous waste container',
        'paint can disposal',
        'chemical waste symbol'
    ],
    'medical': [
        'medical waste disposal',
        'biohazard waste bin',
        'used mask waste'
    ]
}

total_downloaded = 0

for category, keywords in categories.items():
    print(f"\n📂 Downloading {category.upper()}...")
    
    for i, keyword in enumerate(keywords, 1):
        try:
            print(f"   [{i}/{len(keywords)}] {keyword}...", end=" ")
            
            downloader.download(
                keyword,
                limit=170,  # 170 x 3 keywords = ~500 images
                output_dir='dataset_model2',
                adult_filter_off=True,
                force_replace=False,
                timeout=15,
                verbose=False
            )
            
            print("✅")
            total_downloaded += 170
            
        except Exception as e:
            print(f"⚠️ {str(e)[:50]}")
            continue

print("\n" + "="*70)
print("📊 DOWNLOAD COMPLETE")
print("="*70)
print(f"\n✅ Downloaded ~{total_downloaded} images")
print("\n📌 Next: Run 'python train_model2.py' to start training!")
print()
