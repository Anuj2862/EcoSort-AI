from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import uuid
import sqlite3
from datetime import datetime
from PIL import Image
import io
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY or GEMINI_API_KEY == 'your_gemini_api_key_here':
    print("⚠️  WARNING: GEMINI_API_KEY not set! Chatbot will use fallback responses.")
    print("   Set your API key in the .env file")
else:
    print("✅ Gemini API key loaded successfully")
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('models/gemini-2.5-flash')

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load models
print("Loading Model 1 (Original 5 categories)...")
model1 = load_model('my_model.h5')
model1_labels = ['glass', 'metal', 'paper', 'plastic', 'trash']

# Try to load Model 2 (New 5 categories)
try:
    print("Loading Model 2 (Additional 5 categories)...")
    model2 = load_model('waste_model2.h5')
    model2_labels = ['food_waste', 'e_waste', 'textiles', 'hazardous', 'medical']
    DUAL_MODEL_MODE = True
    print("✅ Dual-model mode activated!")
except:
    print("⚠️  Model 2 not found - using single model mode")
    model2 = None
    model2_labels = []
    DUAL_MODEL_MODE = False

# Combined class labels (10 total)
class_labels = model1_labels + model2_labels
print(f"📋 Total categories: {len(class_labels)}")


# Initialize database
def init_db():
    conn = sqlite3.connect('waste_sorting.db')
    c = conn.cursor()
    
    # Classifications table
    c.execute('''CREATE TABLE IF NOT EXISTS classifications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  image_path TEXT,
                  predicted_class TEXT,
                  confidence REAL,
                  all_predictions TEXT,
                  recyclable BOOLEAN,
                  recyclable_confidence REAL,
                  eco_score INTEGER,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Achievements table
    c.execute('''CREATE TABLE IF NOT EXISTS achievements
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  achievement_id TEXT UNIQUE,
                  name TEXT,
                  description TEXT,
                  unlocked_at DATETIME)''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)

    try:
        # Analyze image quality
        quality_check = analyze_image_quality(file_path)
        
        # Load and preprocess image
        image = load_img(file_path, target_size=(224, 224))  
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0) / 255.0
        
        # DUAL-MODEL ENSEMBLE PREDICTION
        if DUAL_MODEL_MODE:
            # Run both models
            predictions1 = model1.predict(image)[0]
            predictions2 = model2.predict(image)[0]
            
            print(f"\n--- DEBUG PREDICTION ---")
            print(f"Model 1 Raw: {predictions1}")
            print(f"Model 2 Raw: {predictions2}")

            # Get best prediction from each model
            max_conf1 = np.max(predictions1)
            max_idx1 = np.argmax(predictions1)
            
            max_conf2 = np.max(predictions2)
            max_idx2 = np.argmax(predictions2)
            
            print(f"Model 1 Best: {model1_labels[max_idx1]} ({max_conf1*100:.2f}%)")
            print(f"Model 2 Best: {model2_labels[max_idx2]} ({max_conf2*100:.2f}%)")

            # Choose model with higher confidence
            if max_conf1 > max_conf2:
                predicted_class_idx = max_idx1
                predicted_class = model1_labels[max_idx1]
                confidence = float(max_conf1) * 100
                source_model = "Model 1"
            else:
                predicted_class_idx = len(model1_labels) + max_idx2  # Offset for model2
                predicted_class = model2_labels[max_idx2]
                confidence = float(max_conf2) * 100
                source_model = "Model 2"
            
            print(f"Selected: {predicted_class} from {source_model}")
            print(f"------------------------\n")

            # Combine all predictions for display
            all_predictions = {}
            for i, label in enumerate(model1_labels):
                all_predictions[label] = round(float(predictions1[i]) * 100, 2)
            for i, label in enumerate(model2_labels):
                all_predictions[label] = round(float(predictions2[i]) * 100, 2)
                
        else:
            # Single model mode (fallback)
            predictions = model1.predict(image)
            predicted_class_idx = np.argmax(predictions[0])
            predicted_class = model1_labels[predicted_class_idx]
            confidence = float(predictions[0][predicted_class_idx]) * 100
            source_model = "Model 1 (Single)"
            
            all_predictions = {
                model1_labels[i]: round(float(predictions[0][i]) * 100, 2)
                for i in range(len(model1_labels))
            }
        
        # Sort predictions by confidence
        sorted_predictions = dict(sorted(all_predictions.items(), 
                                        key=lambda x: x[1], 
                                        reverse=True))
        
        # Determine recyclability
        is_recyclable, recyclable_confidence, recyclability_reason, eco_score = determine_recyclability(
            predicted_class, 
            confidence, 
            quality_check['score']
        )
        
        # Save to database with recyclability
        save_classification(file_path, predicted_class, confidence, str(sorted_predictions), 
                          is_recyclable, recyclable_confidence, eco_score)
        
        # Check and unlock achievements
        achievements = check_achievements()
        
        # Get statistics
        stats = get_statistics()
        
        return jsonify({
            'label': predicted_class,
            'confidence': round(confidence, 2),
            'all_predictions': sorted_predictions,
            'recyclable': is_recyclable,
            'recyclable_confidence': round(recyclable_confidence, 2),
            'recyclability_reason': recyclability_reason,
            'eco_score': eco_score,
            'image_path': file_path,
            'quality_check': quality_check,
            'new_achievements': achievements,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def determine_recyclability(category, confidence, quality_score):
    """
    Rule-based recyclable classifier
    Returns: (is_recyclable, confidence, reason, eco_score)
    """
    recyclability_rules = {
        'metal': {
            'recyclable': True,
            'base_confidence': 95,
            'reason': 'Metals are highly recyclable - aluminum and steel can be recycled indefinitely'
        },
        'glass': {
            'recyclable': True,
            'base_confidence': 90,
            'reason': 'Glass is 100% recyclable and can be recycled endlessly without quality loss'
        },
        'plastic': {
            'recyclable': True,
            'base_confidence': 75,
            'reason': 'Most plastics are recyclable if clean and dry (check recycling number)'
        },
        'paper': {
            'recyclable': True,
            'base_confidence': 85,
            'reason': 'Paper is recyclable if clean and dry (not contaminated with food or grease)'
        },
        'trash': {
            'recyclable': False,
            'base_confidence': 95,
            'reason': 'General waste - not recyclable through standard programs'
        },
        # NEW CATEGORIES
        'food_waste': {
            'recyclable': True,  # Via composting
            'base_confidence': 90,
            'reason': 'Food waste is compostable - turns into nutrient-rich soil for gardens'
        },
        'e_waste': {
            'recyclable': True,
            'base_confidence': 80,
            'reason': 'E-waste recyclable at specialized facilities - contains valuable materials'
        },
        'textiles': {
            'recyclable': True,
            'base_confidence': 70,
            'reason': 'Textiles can be donated or recycled into new fabrics and materials'
        },
        'hazardous': {
            'recyclable': False,
            'base_confidence': 95,
            'reason': 'Hazardous waste requires special disposal - contact local hazardous waste facility'
        },
        'medical': {
            'recyclable': False,
            'base_confidence': 95,
            'reason': 'Medical waste requires biohazard disposal - never throw in regular trash'
        }
    }
    
    rule = recyclability_rules.get(category.lower(), {
        'recyclable': False,
        'base_confidence': 50,
        'reason': 'Unknown category - recyclability uncertain'
    })
    
    is_recyclable = rule['recyclable']
    recyclable_confidence = rule['base_confidence']
    reason = rule['reason']
    
    # Adjust confidence based on image quality
    if quality_score < 60:
        recyclable_confidence = max(50, recyclable_confidence - 20)
        reason += " (Note: Poor image quality may affect accuracy)"
    
    # Adjust confidence based on category confidence
    if confidence < 70:
        recyclable_confidence = max(50, recyclable_confidence - 15)
    
    # Calculate eco-score (0-100)
    eco_score = 0
    if is_recyclable:
        eco_score = 70
        if category.lower() in ['metal', 'glass']:
            eco_score += 20
        elif category.lower() == 'paper':
            eco_score += 15
        elif category.lower() == 'plastic':
            eco_score += 10
        if confidence > 85:
            eco_score += 5
        if quality_score > 80:
            eco_score += 5
    else:
        eco_score = 30
        if confidence > 85:
            eco_score += 10
    
    eco_score = min(100, max(0, eco_score))
    
    return is_recyclable, recyclable_confidence, reason, eco_score

def analyze_image_quality(image_path):
    """Analyze image quality and provide feedback"""
    try:
        img = Image.open(image_path)
        
        # Convert to grayscale for analysis
        gray = img.convert('L')
        pixels = np.array(gray)
        
        # Calculate brightness
        brightness = np.mean(pixels)
        
        # Calculate blur (variance of Laplacian)
        laplacian = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        blur_score = np.var(pixels)
        
        feedback = []
        quality_score = 100
        
        if brightness < 50:
            feedback.append("⚠️ Image is too dark - try better lighting")
            quality_score -= 30
        elif brightness > 200:
            feedback.append("⚠️ Image is too bright - reduce lighting")
            quality_score -= 20
        
        if blur_score < 100:
            feedback.append("⚠️ Image appears blurry - hold camera steady")
            quality_score -= 25
        
        if not feedback:
            feedback.append("✅ Image quality is good!")
        
        return {
            'score': max(0, quality_score),
            'feedback': feedback,
            'brightness': round(brightness, 2),
            'blur_score': round(blur_score, 2)
        }
    except:
        return {'score': 100, 'feedback': ['✅ Image quality is good!'], 'brightness': 128, 'blur_score': 200}

def save_classification(image_path, predicted_class, confidence, all_predictions, recyclable=None, recyclable_confidence=None, eco_score=None):
    """Save classification to database"""
    conn = sqlite3.connect('waste_sorting.db')
    c = conn.cursor()
    c.execute('''INSERT INTO classifications 
                 (image_path, predicted_class, confidence, all_predictions, recyclable, recyclable_confidence, eco_score)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (image_path, predicted_class, confidence, all_predictions, recyclable, recyclable_confidence, eco_score))
    conn.commit()
    conn.close()

def check_achievements():
    """Check and unlock new achievements"""
    conn = sqlite3.connect('waste_sorting.db')
    c = conn.cursor()
    
    # Get total classifications
    c.execute('SELECT COUNT(*) FROM classifications')
    total = c.fetchone()[0]
    
    new_achievements = []
    
    # Define achievements
    achievements_list = [
        ('first_scan', 'First Scan', 'Classified your first item!', 1),
        ('eco_newbie', 'Eco Newbie', 'Classified 10 items', 10),
        ('recycling_hero', 'Recycling Hero', 'Classified 50 items', 50),
        ('planet_protector', 'Planet Protector', 'Classified 100 items', 100),
        ('waste_wizard', 'Waste Wizard', 'Classified 500 items', 500),
    ]
    
    for ach_id, name, desc, required in achievements_list:
        if total >= required:
            # Check if already unlocked
            c.execute('SELECT id FROM achievements WHERE achievement_id = ?', (ach_id,))
            if not c.fetchone():
                # Unlock achievement
                c.execute('''INSERT INTO achievements (achievement_id, name, description, unlocked_at)
                            VALUES (?, ?, ?, ?)''',
                         (ach_id, name, desc, datetime.now()))
                new_achievements.append({'id': ach_id, 'name': name, 'description': desc})
    
    conn.commit()
    conn.close()
    
    return new_achievements

def get_statistics():
    """Get user statistics"""
    conn = sqlite3.connect('waste_sorting.db')
    c = conn.cursor()
    
    # Total classifications
    c.execute('SELECT COUNT(*) FROM classifications')
    total = c.fetchone()[0]
    
    # By category
    c.execute('''SELECT predicted_class, COUNT(*) 
                 FROM classifications 
                 GROUP BY predicted_class''')
    by_category = dict(c.fetchall())
    
    # This week
    c.execute('''SELECT COUNT(*) FROM classifications 
                 WHERE timestamp >= datetime('now', '-7 days')''')
    this_week = c.fetchone()[0]
    
    # Average confidence
    c.execute('SELECT AVG(confidence) FROM classifications')
    avg_confidence = c.fetchone()[0] or 0
    
    # Achievements unlocked
    c.execute('SELECT COUNT(*) FROM achievements')
    achievements_count = c.fetchone()[0]
    
    # Recyclability statistics
    c.execute('SELECT COUNT(*) FROM classifications WHERE recyclable = 1')
    recyclable_count = c.fetchone()[0] or 0
    
    c.execute('SELECT COUNT(*) FROM classifications WHERE recyclable = 0')
    non_recyclable_count = c.fetchone()[0] or 0
    
    c.execute('SELECT AVG(eco_score) FROM classifications WHERE eco_score IS NOT NULL')
    avg_eco_score = c.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'total': total,
        'by_category': by_category,
        'this_week': this_week,
        'avg_confidence': round(avg_confidence, 2),
        'achievements_count': achievements_count,
        'recyclable_count': recyclable_count,
        'non_recyclable_count': non_recyclable_count,
        'recyclability_rate': round((recyclable_count / total * 100) if total > 0 else 0, 1),
        'avg_eco_score': round(avg_eco_score, 1)
    }

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get classification history"""
    conn = sqlite3.connect('waste_sorting.db')
    c = conn.cursor()
    
    limit = request.args.get('limit', 20, type=int)
    
    c.execute('''SELECT id, image_path, predicted_class, confidence, timestamp
                 FROM classifications
                 ORDER BY timestamp DESC
                 LIMIT ?''', (limit,))
    
    history = []
    for row in c.fetchall():
        history.append({
            'id': row[0],
            'image_path': row[1],
            'predicted_class': row[2],
            'confidence': row[3],
            'timestamp': row[4]
        })
    
    conn.close()
    return jsonify(history)

@app.route('/api/achievements', methods=['GET'])
def get_achievements():
    """Get all achievements"""
    conn = sqlite3.connect('waste_sorting.db')
    c = conn.cursor()
    
    c.execute('''SELECT achievement_id, name, description, unlocked_at
                 FROM achievements
                 ORDER BY unlocked_at DESC''')
    
    achievements = []
    for row in c.fetchall():
        achievements.append({
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'unlocked_at': row[3]
        })
    
    conn.close()
    return jsonify(achievements)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get detailed statistics"""
    return jsonify(get_statistics())

@app.route('/api/chat', methods=['POST'])
def chat():
    """AI Recycling Coach chatbot endpoint"""
    try:
        data = request.json
        user_message = data.get('message', '')
        context = data.get('context', {})
        history = data.get('history', [])
        
        # Check if Gemini is configured
        if not GEMINI_API_KEY or GEMINI_API_KEY == 'your_gemini_api_key_here':
            return jsonify({
                'response': "I'm not fully configured yet! Please set your Gemini API key in the .env file to enable AI conversations. For now, try the quick action buttons! 🤖"
            })
        
        # Build conversation prompt
        system_prompt = """You are a friendly, encouraging AI Recycling Coach assistant named "Coach". 
Your personality is like a supportive friend who's passionate about the environment.

Key traits:
- Friendly and encouraging (use emojis appropriately)
- Educational but not preachy
- Celebrates user actions
- Keeps responses under 100 words
- Uses simple language

Current context:"""
        
        if context:
            category = context.get('label', 'unknown').replace('_', ' ')
            confidence = context.get('confidence', 0)
            recyclable = context.get('recyclable', False)
            
            system_prompt += f"""
The user just scanned: {category}
Confidence: {confidence}%
Recyclable: {'Yes' if recyclable else 'No'}
"""
        
        # Build conversation history
        conversation_context = system_prompt + "\n\nConversation:\n"
        for msg in history[-3:]:  # Last 3 messages for context
            role = "User" if msg['role'] == 'user' else "Coach"
            conversation_context += f"{role}: {msg['content']}\n"
        
        conversation_context += f"User: {user_message}\nCoach:"
        
        # Get Gemini response
        response = gemini_model.generate_content(conversation_context)
        bot_response = response.text
        
        return jsonify({'response': bot_response})
        
    except Exception as e:
        print(f"Chat error: {e}")
        import traceback
        traceback.print_exc()
        # Fallback response
        return jsonify({
            'response': "I'm having a bit of trouble right now, but I'm here to help! Try asking me about disposal methods, recycling tips, or your environmental impact! 🌍"
        })


if __name__ == '__main__':
    app.run(debug=True)
