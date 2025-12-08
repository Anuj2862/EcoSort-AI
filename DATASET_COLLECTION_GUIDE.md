# Dataset Collection Resources for Model 2

## 🎯 Goal
Collect 2,500+ images (500+ per category) for training Model 2

---

## 📋 Categories Needed

1. **food_waste** - Organic matter, fruits, vegetables, spoiled food
2. **e_waste** - Electronics, phones, laptops, batteries, circuits  
3. **textiles** - Clothing, fabrics, shoes, torn textiles
4. **hazardous** - Paint cans, chemicals, pesticides, cleaning products
5. **medical** - Masks, syringes, medical gloves, biohazard waste

---

## 🔍 **Recommended Datasets (Kaggle)**

### Quick Links:
1. **Food Waste**: https://www.kaggle.com/datasets/sumn2u/garbage-classification-v2
2. **E-Waste**: https://www.kaggle.com/datasets/farzadnekouei/trash-type-image-dataset
3. **General Waste**: https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification

### Steps:
1. Create Kaggle account (free)
2. Download datasets
3. Extract and organize into `dataset_model2/` folders
4. Remove irrelevant images

---

## 💻 **Automated Download (Bing Images)**

```bash
# Install downloader
pip install bing-image-downloader

# Run Python script
python
```

```python
from bing_image_downloader import downloader

categories = {
    'food_waste': ['food waste', 'organic waste', 'compost'],
    'e_waste': ['electronic waste', 'broken phone', 'ewaste'],
    'textiles': ['textile waste', 'old clothes', 'fabric waste'],
    'hazardous': ['hazardous waste', 'paint can waste'],
    'medical': ['medical waste', 'used mask', 'biohazard']
}

for category, keywords in categories.items():
    for keyword in keywords:
        downloader.download(
            keyword,
            limit=200,  # 200 per keyword
            output_dir=f'dataset_model2/{category}',
            adult_filter_off=True
        )
```

---

## 📊 **Current Status**

Run this to check progress:
```bash
python download_images.py
```

---

## ⏱️ **Time Estimates**

- **Manual (Google Images)**: 2-3 hours
- **Kaggle Download**: 30-60 minutes
- **Automated Script**: 1-2 hours
- **Training Model 2**: 30-60 minutes

**Total**: 3-5 hours for complete system

---

## 🚀 **Quick Start (Minimum Viable)**

For testing, collect just 100 images per category (500 total):
- Faster collection (~30 min)
- Quick training (~15 min)
- Test dual-model system
- Expand dataset later

---

## ✅ **Next Steps**

1. Choose collection method
2. Download/collect images
3. Organize into folders
4. Run: `python train_model2.py`
5. Test system!
