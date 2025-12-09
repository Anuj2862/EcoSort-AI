# 🌍 EcoSort AI - Smart Waste Classification System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10+-orange.svg)](https://www.tensorflow.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered waste sorting assistant that helps users classify waste, provides disposal instructions, and features an interactive AI Recycling Coach chatbot. Built with MobileNetV2 deep learning models and Google Gemini AI.

![EcoSort AI Demo](https://via.placeholder.com/800x400/0ba360/ffffff?text=EcoSort+AI+Demo)

## 🌟 Features

### 🤖 AI Recycling Coach Chatbot
- **Auto-appears after classification** - Friendly assistant pops up to help
- **Quick action buttons** - Instant disposal help, CO2 impact, tips, and stats
- **AI-powered conversations** - Ask anything about recycling (powered by Gemini)
- **Context-aware** - Remembers what you just scanned
- **Beautiful UI** - Glassmorphism design with smooth animations

### 🎯 Dual-Model Classification
- **10 waste categories** across two specialized models
  - Model 1: Glass, Metal, Paper, Plastic, Trash
  - Model 2: Food Waste, E-Waste, Textiles, Hazardous, Medical
- **High accuracy** with MobileNetV2 architecture
- **Ensemble prediction** - Chooses best result from both models

### ♻️ Recyclability Detection
- Binary classification (Recyclable/Non-recyclable)
- Confidence scoring with reasoning
- Category-specific rules and guidelines

### 🌍 Environmental Impact Tracking
- **Eco-Score** (0-100) for each classification
- **Statistics dashboard** - Trees saved, water conserved, CO2 reduced
- **Achievement system** - Gamification with 5 achievement tiers
- **Classification history** - Visual grid of past scans

### 📋 Comprehensive Disposal Guides
- Step-by-step instructions for all 10 categories
- Educational fun facts about recycling
- Best practices and tips

### 🎨 Modern UI/UX
- Glassmorphism design with eco-friendly theme
- Smooth animations and transitions
- Responsive layout (mobile, tablet, desktop)
- Dynamic category badges with gradients
- Real-time image preview

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Google Gemini API key (optional, for AI chatbot)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ecosort-ai.git
cd ecosort-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables** (optional for AI chatbot)
```bash
# Create .env file
echo GEMINI_API_KEY=your_api_key_here > .env
```

4. **Run the application**
```bash
python flaskapp.py
```

5. **Open in browser**
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
ecosort-ai/
├── flaskapp.py                 # Flask backend server
├── my_model.h5                 # Model 1 (5 categories)
├── waste_model2.h5             # Model 2 (5 categories)
├── waste_sorting.db            # SQLite database
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not committed)
├── .gitignore                  # Git ignore rules
│
├── templates/
│   └── index.html              # Main frontend template
│
├── static/
│   ├── css/
│   │   ├── style.css           # Main styles
│   │   ├── recyclability.css   # Recyclability badge styles
│   │   ├── category_badge.css  # Dynamic category badges
│   │   └── chatbot.css         # AI chatbot styles
│   │
│   ├── js/
│   │   ├── app.js              # Main application logic
│   │   └── chatbot.js          # AI chatbot functionality
│   │
│   └── uploads/                # User uploaded images
│
└── README.md                   # This file
```

---

## 🎯 Usage

### 1. Classify Waste
1. Click "Choose File" or drag & drop an image
2. Click "Classify Waste"
3. View classification result with confidence score

### 2. Use AI Recycling Coach
- Chatbot appears automatically after classification
- Click quick action buttons:
  - 🗑️ **How to dispose?** - Step-by-step guide
  - 🌍 **CO₂ saved?** - Environmental impact
  - 💡 **Recycling tip** - Educational facts
  - 📊 **My impact** - Your statistics
- Or type custom questions for AI responses

### 3. Track Your Impact
- Navigate to **Stats** tab
- View environmental metrics
- See category breakdown
- Monitor achievements

### 4. Review History
- Navigate to **History** tab
- See past classifications
- Review confidence scores
- Check timestamps

---

## 🤖 AI Chatbot Setup

The AI Recycling Coach uses Google Gemini for conversational responses.

### Get API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key

### Configure
1. Create `.env` file in project root
2. Add your key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Features
- **Quick actions work without API** (disposal, tips, stats)
- **AI conversations require API** (custom questions)
- **Fallback responses** if API unavailable

---

## 🧠 Model Information

### Architecture
- **Base**: MobileNetV2 (transfer learning)
- **Input**: 224x224 RGB images
- **Output**: Softmax probabilities

### Training
- **Data augmentation**: Rotation, shift, zoom, flip
- **Optimizer**: Adam
- **Loss**: Categorical crossentropy
- **Metrics**: Accuracy

### Categories

**Model 1 (Traditional Waste)**
- Glass
- Metal
- Paper
- Plastic
- Trash

**Model 2 (Specialized Waste)**
- Food Waste
- E-Waste
- Textiles
- Hazardous
- Medical

---

## 🎨 Features Showcase

### Dynamic Category Badges
- Curved pill-shaped design
- Category-specific gradients
- Pulse and shimmer animations
- Hover effects

### Recyclability Detection
- Visual indicators (♻️ or 🚫)
- Color-coded badges (green/red)
- Confidence percentages
- Reasoning explanations

### Eco-Score System
- 0-100 rating scale
- Dynamic color coding
- Animated progress bar
- Based on recyclability and quality

### Achievement System
- 🌱 First Scan (1 item)
- ♻️ Eco Newbie (10 items)
- 🦸 Recycling Hero (50 items)
- 🌍 Planet Protector (100 items)
- 🧙 Waste Wizard (500 items)

---

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **TensorFlow/Keras** - Deep learning
- **SQLite** - Database
- **Pillow** - Image processing
- **NumPy** - Numerical operations
- **Google Generative AI** - Chatbot

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (Glassmorphism)
- **JavaScript (ES6)** - Interactivity
- **Fetch API** - AJAX requests

---

## 📊 API Endpoints

### POST `/api/predict`
Classify waste image
- **Input**: Image file (multipart/form-data)
- **Output**: Classification results, recyclability, eco-score

### POST `/api/chat`
AI chatbot conversations
- **Input**: Message, context, history
- **Output**: AI-generated response

### GET `/api/stats`
User statistics
- **Output**: Total scans, category breakdown, achievements

### GET `/api/history`
Classification history
- **Output**: Recent classifications with metadata

### GET `/api/achievements`
Unlocked achievements
- **Output**: Achievement list with timestamps

---

## 🎓 Educational Content

### Disposal Guides
Detailed 3-step instructions for each category:
- Proper preparation
- Disposal method
- Best practices

### Fun Facts
30+ environmental facts including:
- Recycling statistics
- Environmental impact
- Material properties
- Sustainability tips

---

## 🔒 Security & Privacy

- **API keys** protected via `.env` (not committed)
- **Input validation** on file uploads
- **Error handling** with graceful fallbacks
- **No personal data** collection
- **Local processing** for images

---

## 🚧 Future Enhancements

- [ ] Voice interaction
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Barcode scanning
- [ ] Location-based recycling centers
- [ ] Social sharing features


---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **TensorFlow** for the deep learning framework
- **Google Gemini** for AI capabilities
- **MobileNetV2** for the base architecture
- **Flask** for the web framework
- **Open-source community** for inspiration

---

## 📧 Contact

**Project Link**: [https://github.com/yourusername/ecosort-ai](https://github.com/yourusername/ecosort-ai)

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐!

---

**Made with ❤️ for a greener planet 🌍**
