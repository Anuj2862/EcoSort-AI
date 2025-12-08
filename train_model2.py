"""
Training Script for Model 2: Additional Waste Categories
Trains a 5-category model for: food_waste, e_waste, textiles, hazardous, medical
"""

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import matplotlib.pyplot as plt
import os

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 25
NUM_CLASSES = 5  # Only 5 new categories
DATASET_DIR = 'dataset_model2'

# New categories
NEW_CATEGORIES = ['food_waste', 'e_waste', 'textiles', 'hazardous', 'medical']

print("\n" + "="*60)
print("🚀 MODEL 2 TRAINING: Additional Waste Categories")
print("="*60)
print(f"\n📋 Categories: {', '.join(NEW_CATEGORIES)}\n")

# Check dataset
if not os.path.exists(DATASET_DIR):
    print(f"❌ Error: {DATASET_DIR} not found!")
    print("\n📝 Create dataset structure:")
    print(f"   {DATASET_DIR}/")
    for cat in NEW_CATEGORIES:
        print(f"   ├── {cat}/")
    print("\n💡 Add ~500 images per category, then run this script again.")
    exit(1)

# Count images
print("📊 Dataset Summary:")
total = 0
for cat in NEW_CATEGORIES:
    path = os.path.join(DATASET_DIR, cat)
    if os.path.exists(path):
        count = len([f for f in os.listdir(path) if f.endswith(('.jpg', '.jpeg', '.png'))])
        total += count
        print(f"   {cat:15s}: {count:4d} images")

print(f"\n   TOTAL: {total} images\n")

if total < 500:
    print("⚠️  WARNING: Very small dataset!")
    response = input("   Continue anyway? (y/n): ")
    if response.lower() != 'y':
        exit(0)

# Data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

# Load data
train_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_gen = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# Build model
print("\n🏗️  Building Model 2...")
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(NUM_CLASSES, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Callbacks
callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    ModelCheckpoint('model2_best.h5', monitor='val_accuracy', save_best_only=True),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3)
]

# Train
print("\n🎯 Training Model 2...\n")
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=callbacks
)

# Save
model.save('waste_model2.h5')
print("\n✅ Model 2 saved as: waste_model2.h5")

# Plot
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Val')
plt.title('Model 2 Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train')
plt.plot(history.history['val_loss'], label='Val')
plt.title('Model 2 Loss')
plt.legend()

plt.savefig('model2_training.png')
print("✅ Training plot saved: model2_training.png")

print(f"\n📈 Final Accuracy: {history.history['val_accuracy'][-1]:.2%}")
print("\n📌 Next: Update flaskapp.py with dual-model logic")
