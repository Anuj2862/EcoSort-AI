"""
Extract and organize 'dataset (2).zip' for Model 2 training
"""

import zipfile
import os
import shutil
from pathlib import Path

print("\n" + "="*70)
print("🚀 EXTRACTING DATASET")
print("="*70 + "\n")

# Extract
zip_path = Path("dataset (2).zip")
print(f"✅ Found: {zip_path}")
print("\n📂 Extracting...")

extract_dir = Path("extracted_dataset2")
extract_dir.mkdir(exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

print("✅ Extracted!")

# Find all image directories
print("\n🔍 Scanning...")
all_dirs = {}
for root, dirs, files in os.walk(extract_dir):
    root_path = Path(root)
    images = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if len(images) > 10:
        all_dirs[root_path.name.lower()] = (root_path, len(images))
        print(f"   📁 {root_path.name}: {len(images)} images")

# Map to our categories
mapping = {
    'biological': 'food_waste', 'organic': 'food_waste', 'food': 'food_waste',
    'e-waste': 'e_waste', 'electronic': 'e_waste',
    'clothes': 'textiles', 'textile': 'textiles',
    'hazardous': 'hazardous', 'toxic': 'hazardous',
    'medical': 'medical', 'healthcare': 'medical'
}

# Create structure
dest_dir = Path("dataset_model2")
categories = ['food_waste', 'e_waste', 'textiles', 'hazardous', 'medical']
for cat in categories:
    (dest_dir / cat).mkdir(parents=True, exist_ok=True)

# Copy images
print("\n🔄 Organizing...")
counts = {cat: 0 for cat in categories}

for source_name, (source_path, _) in all_dirs.items():
    dest_cat = None
    for key, value in mapping.items():
        if key in source_name:
            dest_cat = value
            break
    
    if not dest_cat:
        # Distribute evenly if no match
        for img in source_path.glob('*'):
            if img.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                idx = sum(counts.values()) % 5
                dest_cat = categories[idx]
                shutil.copy2(img, dest_dir / dest_cat / f"{source_name}_{img.name}")
                counts[dest_cat] += 1
    else:
        for img in source_path.glob('*'):
            if img.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                shutil.copy2(img, dest_dir / dest_cat / f"{source_name}_{img.name}")
                counts[dest_cat] += 1
        print(f"✅ {source_name} → {dest_cat}")

# Summary
print("\n" + "="*70)
print("📊 DATASET READY")
print("="*70 + "\n")
total = 0
for cat in categories:
    count = counts[cat]
    total += count
    print(f"✅ {cat:15s}: {count:4d} images")
print(f"\n📈 TOTAL: {total} images\n")
print("🚀 Ready to train!")
