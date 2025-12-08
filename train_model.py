"""
Model Training Script for 10-Category Waste Classification
Uses transfer learning with MobileNetV2
"""

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import matplotlib.pyplot as plt
import numpy as np
import os

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 30
NUM_CLASSES = 10
DATASET_DIR = 'dataset'

print("\n" + "="*60)
print("🚀 WASTE CLASSIFICATION MODEL TRAINING")
print("="*60 + "\n")

# Check if dataset exists
if not os.path.exists(DATASET_DIR):
    print("❌ Error: Dataset directory not found!")
    print("   Run: python prepare_dataset.py first")
    exit(1)

# Count images per category
print("📊 Dataset Summary:")
categories = sorted(os.listdir(DATASET_DIR))
total_images = 0
for cat in categories:
    cat_path = os.path.join(DATASET_DIR, cat)
    if os.path.isdir(cat_path):
        count = len([f for f in os.listdir(cat_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
        total_images += count
        print(f"   {cat:20s}: {count:4d} images")

print(f"\n   TOTAL: {total_images} images")

if total_images < 500:
    print("\n⚠️  WARNING: Very small dataset! Model accuracy may be low.")
    print("   Recommended: 5000+ total images (500+ per category)")
    response = input("\n   Continue anyway? (y/n): ")
    if response.lower() != 'y':
        print("   Training cancelled.")
        exit(0)

print("\n" + "-"*60 + "\n")

# Data augmentation for training
print("🔧 Setting up data augmentation...")
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)

# Load training data
print("📥 Loading training data...")
train_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

# Load validation data
print("📥 Loading validation data...")
validation_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# Save class indices for later use
class_indices = train_generator.class_indices
class_labels = {v: k for k, v in class_indices.items()}
print(f"\n📋 Class Labels: {list(class_labels.values())}")

# Build model with transfer learning
print("\n🏗️  Building model architecture...")
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

# Freeze base model layers
base_model.trainable = False

# Add custom classification layers
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(NUM_CLASSES, activation='softmax')
])

# Compile model
print("⚙️  Compiling model...")
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
)

# Print model summary
print("\n📐 Model Architecture:")
model.summary()

# Callbacks
callbacks = [
    EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),
    ModelCheckpoint(
        'best_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=0.00001,
        verbose=1
    )
]

# Train model
print("\n" + "="*60)
print("🎯 STARTING TRAINING")
print("="*60 + "\n")

history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=EPOCHS,
    callbacks=callbacks,
    verbose=1
)

# Save final model
print("\n💾 Saving model...")
model.save('waste_classifier_10cat.h5')
print("   ✅ Saved as: waste_classifier_10cat.h5")

# Save class labels
import json
with open('class_labels.json', 'w') as f:
    json.dump(class_labels, f, indent=2)
print("   ✅ Saved class labels: class_labels.json")

# Plot training history
print("\n📊 Generating training plots...")
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Accuracy plot
axes[0].plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Loss plot
axes[1].plot(history.history['loss'], label='Training Loss', linewidth=2)
axes[1].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('training_history.png', dpi=150, bbox_inches='tight')
print("   ✅ Saved plot: training_history.png")

# Print final results
print("\n" + "="*60)
print("✅ TRAINING COMPLETE!")
print("="*60)
print(f"\n📈 Final Results:")
print(f"   Training Accuracy:   {history.history['accuracy'][-1]:.2%}")
print(f"   Validation Accuracy: {history.history['val_accuracy'][-1]:.2%}")
print(f"   Training Loss:       {history.history['loss'][-1]:.4f}")
print(f"   Validation Loss:     {history.history['val_loss'][-1]:.4f}")

if 'top_3_accuracy' in history.history:
    print(f"   Top-3 Accuracy:      {history.history['val_top_3_accuracy'][-1]:.2%}")

print("\n📌 Next Steps:")
print("   1. Review training_history.png")
print("   2. Backup old model: cp my_model.h5 my_model_5cat_backup.h5")
print("   3. Replace model: mv waste_classifier_10cat.h5 my_model.h5")
print("   4. Update flaskapp.py with new class labels")
print("   5. Test the new model!")
print()
