"""
Organize Downloaded Dataset for Model 2 Training
Maps downloaded dataset categories to our Model 2 categories
"""

import os
import shutil
from pathlib import Path

print("\n" + "="*70)
print("📦 ORGANIZING DATASET FOR MODEL 2")
print("="*70 + "\n")

# Source and destination
SOURCE_DIR = 'extracted_dataset'
DEST_DIR = 'dataset_model2'

# Find the actual dataset directory
print("🔍 Searching for dataset structure...")
source_path = Path(SOURCE_DIR)

# Common dataset structures
possible_paths = [
    source_path,
    source_path / 'dataset',
    source_path / 'Garbage classification',
    source_path / 'archive',
]

dataset_root = None
for path in possible_paths:
    if path.exists():
        subdirs = [d for d in path.iterdir() if d.is_dir()]
        if subdirs:
            dataset_root = path
            print(f"✅ Found dataset at: {path}")
            break

if not dataset_root:
    print("❌ Could not find dataset structure")
    print("📂 Available directories:")
    for item in source_path.rglob('*'):
        if item.is_dir():
            print(f"   {item}")
    exit(1)

# Map source categories to our Model 2 categories
category_mapping = {
    # Common mappings - adjust based on actual dataset
    'food': 'food_waste',
    'organic': 'food_waste',
    'biological': 'food_waste',
    
    'e-waste': 'e_waste',
    'electronic': 'e_waste',
    'electronics': 'e_waste',
    
    'textile': 'textiles',
    'clothes': 'textiles',
    'fabric': 'textiles',
    
    'hazardous': 'hazardous',
    'toxic': 'hazardous',
    'chemical': 'hazardous',
    
    'medical': 'medical',
    'healthcare': 'medical',
    'biohazard': 'medical',
}

print("\n📂 Available categories in dataset:")
categories_found = []
for item in dataset_root.iterdir():
    if item.is_dir():
        print(f"   • {item.name}")
        categories_found.append(item.name.lower())

print("\n🔄 Organizing images...")

# Create destination directories
for cat in ['food_waste', 'e_waste', 'textiles', 'hazardous', 'medical']:
    os.makedirs(os.path.join(DEST_DIR, cat), exist_ok=True)

# Copy images
total_copied = 0
for source_cat in dataset_root.iterdir():
    if not source_cat.is_dir():
        continue
    
    # Find matching destination category
    source_name = source_cat.name.lower()
    dest_cat = None
    
    for key, value in category_mapping.items():
        if key in source_name:
            dest_cat = value
            break
    
    if not dest_cat:
        print(f"⚠️  Skipping '{source_cat.name}' - no mapping found")
        continue
    
    # Copy images
    image_count = 0
    for img_file in source_cat.glob('*'):
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
            dest_path = Path(DEST_DIR) / dest_cat / f"{source_cat.name}_{img_file.name}"
            shutil.copy2(img_file, dest_path)
            image_count += 1
            total_copied += 1
    
    print(f"✅ {source_cat.name} → {dest_cat}: {image_count} images")

print(f"\n📊 Total images copied: {total_copied}")

# Count final dataset
print("\n" + "="*70)
print("📈 FINAL DATASET SUMMARY")
print("="*70 + "\n")

grand_total = 0
for cat in ['food_waste', 'e_waste', 'textiles', 'hazardous', 'medical']:
    cat_path = Path(DEST_DIR) / cat
    if cat_path.exists():
        count = len(list(cat_path.glob('*.jpg'))) + len(list(cat_path.glob('*.jpeg'))) + len(list(cat_path.glob('*.png')))
        grand_total += count
        status = "✅" if count >= 100 else "⚠️"
        print(f"{status} {cat:15s}: {count:4d} images")

print(f"\n📈 GRAND TOTAL: {grand_total} images")

if grand_total >= 500:
    print("\n✅ Dataset ready for training!")
    print("\n🚀 Next: Run 'python train_model2.py'")
else:
    print(f"\n⚠️  Dataset small ({grand_total} images)")
    print("   Training will work but accuracy may be lower")
    print("   Recommended: 500+ images total\n")
