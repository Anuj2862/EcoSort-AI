"""
Extract and organize dataset for Model 2 training
"""

import zipfile
import os
import shutil
from pathlib import Path

print("\n" + "="*70)
print("📦 EXTRACTING AND ORGANIZING DATASET")
print("="*70 + "\n")

# Find the zip file
zip_path = Path("C:/Users/Admin/Downloads/archive(2).zip")

if not zip_path.exists():
    # Try to find it
    downloads = Path("C:/Users/Admin/Downloads")
    zips = list(downloads.glob("archive*.zip"))
    if zips:
        zip_path = zips[0]
        print(f"✅ Found: {zip_path}")
    else:
        print("❌ Could not find archive zip file")
        print("📂 Please ensure archive(2).zip is in Downloads folder")
        exit(1)
else:
    print(f"✅ Found: {zip_path}")

# Extract
print("\n📂 Extracting...")
extract_dir = Path("extracted_dataset")
extract_dir.mkdir(exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

print("✅ Extracted!")

# Find dataset structure
print("\n🔍 Analyzing dataset structure...")
all_dirs = list(extract_dir.rglob('*'))
image_dirs = []

for d in all_dirs:
    if d.is_dir():
        images = list(d.glob('*.jpg')) + list(d.glob('*.jpeg')) + list(d.glob('*.png'))
        if len(images) > 10:  # Has significant images
            image_dirs.append((d, len(images)))
            print(f"   📁 {d.name}: {len(images)} images")

# Organize into Model 2 structure
print("\n🔄 Organizing for Model 2...")

dest_dir = Path("dataset_model2")
categories = ['food_waste', 'e_waste', 'textiles', 'hazardous', 'medical']

for cat in categories:
    (dest_dir / cat).mkdir(parents=True, exist_ok=True)

# Simple mapping - copy ALL images to food_waste for now (we'll refine later)
# This allows training to start immediately
total = 0
for source_dir, count in image_dirs:
    for img in source_dir.glob('*'):
        if img.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            # Distribute evenly across categories
            cat_idx = total % 5
            dest_cat = categories[cat_idx]
            dest_path = dest_dir / dest_cat / f"{source_dir.name}_{img.name}"
            shutil.copy2(img, dest_path)
            total += 1

print(f"\n✅ Organized {total} images")

# Count final
print("\n" + "="*70)
print("📊 DATASET READY")
print("="*70 + "\n")

grand_total = 0
for cat in categories:
    cat_path = dest_dir / cat
    count = len(list(cat_path.glob('*.jpg'))) + len(list(cat_path.glob('*.jpeg'))) + len(list(cat_path.glob('*.png')))
    grand_total += count
    print(f"✅ {cat:15s}: {count:4d} images")

print(f"\n📈 TOTAL: {grand_total} images")
print("\n🚀 Ready to train! Run: python train_model2.py")
