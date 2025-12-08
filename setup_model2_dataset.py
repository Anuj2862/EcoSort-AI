"""
Quick Dataset Setup for Model 2
Creates directory structure and provides download instructions
"""

import os

DATASET_DIR = 'dataset_model2'
CATEGORIES = ['food_waste', 'e_waste', 'textiles', 'hazardous', 'medical']

print("\n" + "="*60)
print("📁 CREATING DATASET STRUCTURE FOR MODEL 2")
print("="*60 + "\n")

# Create directories
for cat in CATEGORIES:
    path = os.path.join(DATASET_DIR, cat)
    os.makedirs(path, exist_ok=True)
    print(f"✅ Created: {path}")

print("\n" + "="*60)
print("📥 DATASET COLLECTION GUIDE")
print("="*60 + "\n")

instructions = {
    'food_waste': {
        'keywords': 'food waste, organic waste, fruit waste, vegetable waste, compost',
        'examples': 'banana peels, apple cores, vegetable scraps, spoiled food',
        'sources': 'Kaggle: Food Waste Dataset, Google Images'
    },
    'e_waste': {
        'keywords': 'electronic waste, e-waste, old electronics, broken phones',
        'examples': 'old phones, broken laptops, circuit boards, batteries',
        'sources': 'Kaggle: E-Waste Dataset, Google Images'
    },
    'textiles': {
        'keywords': 'textile waste, old clothes, fabric waste, clothing waste',
        'examples': 'old t-shirts, torn jeans, fabric scraps, shoes',
        'sources': 'Google Images, Fashion datasets'
    },
    'hazardous': {
        'keywords': 'hazardous waste, chemical waste, paint cans, cleaning products',
        'examples': 'paint cans, batteries, chemicals, pesticides',
        'sources': 'Google Images (use carefully)'
    },
    'medical': {
        'keywords': 'medical waste, biohazard, masks, syringes, medical supplies',
        'examples': 'used masks, syringes, medical gloves, bandages',
        'sources': 'Google Images, Medical waste datasets'
    }
}

for cat, info in instructions.items():
    print(f"📂 {cat.upper()}")
    print(f"   Keywords: {info['keywords']}")
    print(f"   Examples: {info['examples']}")
    print(f"   Sources:  {info['sources']}")
    print(f"   Target:   500+ images\n")

print("="*60)
print("🔍 QUICK DOWNLOAD OPTIONS")
print("="*60 + "\n")

print("Option 1: Google Images (Manual)")
print("  1. Search category keywords")
print("  2. Download 500+ images")
print("  3. Save to dataset_model2/{category}/\n")

print("Option 2: Kaggle Datasets")
print("  1. Visit kaggle.com/datasets")
print("  2. Search 'waste classification'")
print("  3. Download and organize\n")

print("Option 3: Use Existing Small Dataset (Quick Test)")
print("  - Download 50-100 images per category")
print("  - Train for testing purposes")
print("  - Expand dataset later\n")

print("="*60)
print("📌 NEXT STEPS")
print("="*60 + "\n")
print("1. Add images to dataset_model2/ folders")
print("2. Run: python train_model2.py")
print("3. Wait for training (~30-60 min)")
print("4. Model will be saved as waste_model2.h5\n")

# Create README
readme = """# Model 2 Dataset

## Structure
```
dataset_model2/
├── food_waste/     (500+ images)
├── e_waste/        (500+ images)
├── textiles/       (500+ images)
├── hazardous/      (500+ images)
└── medical/        (500+ images)
```

## Quick Start
1. Add images to each category folder
2. Run: `python train_model2.py`
3. Model saved as `waste_model2.h5`

## Image Requirements
- Format: JPG, JPEG, PNG
- Size: Any (will be resized to 224x224)
- Quality: Clear, well-lit images
- Quantity: 500+ per category (minimum 100 for testing)
"""

with open(os.path.join(DATASET_DIR, 'README.md'), 'w') as f:
    f.write(readme)

print("✅ Setup complete! README created in dataset_model2/\n")
