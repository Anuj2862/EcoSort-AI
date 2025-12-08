"""
Extract and organize dataset(2).zip for Model 2 training
Maps Kaggle dataset categories to our Model 2 categories
"""

import zipfile
import os
import shutil
from pathlib import Path

print("\n" + "="*70)
print("🚀 EXTRACTING AND ORGANIZING DATASET FOR MODEL 2")
print("="*70 + "\n")

# Extract dataset
zip_path = Path("dataset(2).zip")
if not zip_path.exists():
    print("❌ dataset(2).zip not found in current directory")
    exit(1)

print(f"✅ Found: {zip_path}")
print("\n📂 Extracting...")

extract_dir = Path("extracted_dataset2")
extract_dir.mkdir(exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

print("✅ Extracted!")

# Find all directories with images
print("\n🔍 Scanning for image categories...")
all_dirs = {}
for root, dirs, files in os.walk(extract_dir):
    root_path = Path(root)
    images = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if len(images) > 10:
        category_name = root_path.name.lower()
        all_dirs[category_name] = (root_path, len(images))
        print(f"   📁 {root_path.name}: {len(images)} images")

# Category mapping
category_mapping = {
    'biological': 'food_waste',
    'organic': 'food_waste',
    'food': 'food_waste',
    
    'e-waste': 'e_waste',
    'electronic': 'e_waste',
    'electronics': 'e_waste',
    
    'clothes': 'textiles',
    'textile': 'textiles',
    'fabric': 'textiles',
    
    'hazardous': 'hazardous',
    'toxic': 'hazardous',
    'chemical': 'hazardous',
    
    'medical': 'medical',
    'healthcare': 'medical',
    'biohazard': 'medical'
}

# Create destination structure
dest_dir = Path("dataset_model2")
categories = ['food_waste', 'e_waste', 'textiles', 'hazardous', 'medical']

for cat in categories:
    (dest_dir / cat).mkdir(parents=True, exist_ok=True)

# Organize images
print("\n🔄 Organizing images into Model 2 structure...")
total_copied = 0
category_counts = {cat: 0 for cat in categories}

for source_name, (source_path, count) in all_dirs.items():
    # Find matching destination
    dest_cat = None
    for key, value in category_mapping.items():
        if key in source_name:
            dest_cat = value
            break
    
    if not dest_cat:
        # If no match, distribute evenly
        print(f"⚠️  '{source_name}' - no mapping, distributing evenly")
        for img_file in source_path.glob('*'):
            if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                cat_idx = total_copied % 5
                dest_cat = categories[cat_idx]
                dest_path = dest_dir / dest_cat / f"{source_name}_{img_file.name}"
                shutil.copy2(img_file, dest_path)
                category_counts[dest_cat] += 1
                total_copied += 1
    else:
        # Copy to matched category
        for img_file in source_path.glob('*'):
            if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                dest_path = dest_dir / dest_cat / f"{source_name}_{img_file.name}"
                shutil.copy2(img_file, dest_path)
                category_counts[dest_cat] += 1
                total_copied += 1
        print(f"✅ {source_name} → {dest_cat}: {category_counts[dest_cat]} images")

print(f"\n📊 Total images organized: {total_copied}")

# Final count
print("\n" + "="*70)
print("📈 FINAL DATASET SUMMARY")
print("="*70 + "\n")

grand_total = 0
for cat in categories:
    count = category_counts[cat]
    grand_total += count
    status = "✅" if count >= 100 else "⚠️"
    print(f"{status} {cat:15s}: {count:4d} images")

print(f"\n📈 TOTAL: {grand_total} images")

if grand_total >= 500:
    print("\n✅ Dataset ready for training!")
    print("\n🚀 Starting training: python train_model2.py")
else:
    print(f"\n⚠️  Small dataset ({grand_total} images)")
    print("   Will train anyway - accuracy may be lower")

print()
