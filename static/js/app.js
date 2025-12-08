// ==================== DISPOSAL INSTRUCTIONS DATA ====================
const disposalGuides = {
    metal: `How to Dispose of Metal in 3 Simple Steps

Sort and Clean: Separate metal items by type (e.g., aluminum, steel, copper) and remove non-metal parts. Clean off any residue or contaminants like grease or food.

Recycle or Sell: Take small items (e.g., cans) to curbside recycling if available. For larger items (e.g., appliances, tools), visit a local recycling center or scrap yard, where they may even pay you for the metal.

Follow Local Guidelines: Check local rules for proper disposal or recycling, and ensure hazardous items (like batteries) go to designated facilities.`,

    glass: `How to Dispose of Glass in 3 Simple Steps

Sort and Clean: Rinse glass items to remove residue, and separate them by type (e.g., bottles, jars) and color if required (clear, green, brown).

Recycle: Place clean glass items in your curbside recycling bin if accepted, or take them to a local glass recycling drop-off center. Avoid including broken glass unless permitted.

Handle Hazardous Glass Separately: Dispose of tempered glass (e.g., windows, mirrors) and non-recyclable glass (e.g., lightbulbs, ceramics) at designated facilities, following local guidelines.`,

    plastic: `How to Dispose of Plastic in 3 Simple Steps

Sort and Clean: Identify recyclable plastics by checking the recycling number (usually 1, 2, or 5). Rinse and remove food residues or labels.

Recycle or Reuse: Place recyclable plastics in curbside recycling bins if accepted, or take them to a nearby recycling facility. Consider reusing non-recyclable plastics for storage or DIY projects.

Avoid Landfill: For non-recyclable plastics, look for specialized recycling programs (e.g., for plastic bags or Styrofoam) and dispose of responsibly to minimize environmental impact.`,

    trash: `How to Dispose of Trash in 3 Simple Steps

Sort Trash: Separate recyclable, compostable, and hazardous items from general waste to minimize what goes to landfills.

Bag and Secure: Place non-recyclable, non-hazardous trash in durable garbage bags, ensuring they're sealed to prevent leaks or spills.

Dispose Properly: Drop off the trash at your local waste collection point or place it in your designated garbage bin for pickup on scheduled collection days.`,

    paper: `How to Dispose of Paper in 3 Simple Steps

Sort and Clean: Separate recyclable paper (e.g., newspapers, cardboard, office paper) from soiled or contaminated paper (e.g., greasy or wet paper). Remove staples or plastic if possible.

Recycle: Place clean, dry paper in your curbside recycling bin or take it to a local recycling facility. Flatten cardboard boxes to save space.

Compost Non-Recyclable Paper: Use shredded or soiled paper (e.g., napkins) as compost material, provided it's free of non-biodegradable coatings or inks.`,

    // New Categories
    food_waste: `How to Dispose of Food Waste

Compost: The best option! Use a compost bin or pile for fruit/veggie scraps, eggshells, and coffee grounds.
    
Green Bin: If your city has organic waste collection, place food scraps there.
    
Trash: Meat, dairy (if not compostable locally), and oils usually go in the trash. Avoid pouring oil down the drain.`,

    e_waste: `How to Dispose of E-Waste
    
Don't Bin It: Never put electronics in regular trash/recycling bins.
    
Drop-off Centers: Find a certified e-waste recycler or drop-off point (like Best Buy or Staples).
    
Donate: working electronics can often be donated to charities.`,

    textiles: `How to Dispose of Textiles
    
Donate: Clean, usable clothes should be donated to thrift stores or charities.
    
Textile Recycling: Worn/torn clothes can often be recycled at specific drop boxes or by clothing brands (e.g., H&M).
    
Repurpose: Turn old t-shirts into cleaning rags!`,

    hazardous: `How to Dispose of Hazardous Waste
    
Identify: Batteries, paint, chemicals, fluorescent bulbs.
    
Special Collection: These MUST go to a household hazardous waste facility or special collection event.
    
Safety: Keep in original containers if possible; do not mix chemicals.`,

    medical: `How to Dispose of Medical Waste
    
Sharps: Needles/syringes need a specialized sharps container (sturdy plastic). Check local "sharps" return programs.
    
Medication: Use pharmacy take-back programs or safe disposal kits. Do not flush meds unless instructed.`
};

// ==================== FUN FACTS DATABASE ====================
const funFacts = {
    metal: [
        "Aluminum cans can be recycled indefinitely without losing quality!",
        "Recycling one aluminum can saves enough energy to run a TV for 3 hours.",
        "Steel is the most recycled material on Earth - over 650 million tons annually!"
    ],
    glass: [
        "Glass can be recycled endlessly without loss in quality or purity.",
        "Recycling glass saves 30% of the energy needed to make new glass.",
        "A glass bottle takes 4,000 years to decompose in a landfill!"
    ],
    plastic: [
        "Only 9% of all plastic ever made has been recycled.",
        "Plastic bottles take 450 years to decompose in landfills.",
        "Recycling one plastic bottle saves enough energy to power a lightbulb for 3 hours!"
    ],
    paper: [
        "Recycling one ton of paper saves 17 trees, 7,000 gallons of water, and 4,000 kW of energy!",
        "Paper can be recycled 5-7 times before the fibers become too short.",
        "The average American uses 7 trees worth of paper products each year."
    ],
    trash: [
        "The average person generates 4.5 pounds of trash per day.",
        " About 75% of waste is recyclable, but we only recycle about 30%.",
        "Composting food waste can reduce household trash by up to 30%!"
    ],
    food_waste: [
        "Food waste in landfills generates methane, a potent greenhouse gas.",
        "About one-third of all food produced is lost or wasted.",
        "Composting saves money on fertilizers and improves soil health."
    ],
    e_waste: [
        "E-waste represents 2% of America's trash in landfills, but it equals 70% of overall toxic waste.",
        "Recycling 1 million laptops saves the energy equivalent to the electricity used by 3,657 US homes in a year."
    ],
    textiles: [
        "The fashion industry is responsible for 10% of annual global carbon emissions.",
        "Textile recycling can give old clothes new life as insulation or padding."
    ],
    hazardous: [
        "One gallon of motor oil can contaminate one million gallons of fresh water.",
        "Fluorescent bulbs contain mercury and should essentially never be broken."
    ],
    medical: [
        "Proper disposal of sharps prevents injury to waste workers.",
        "Unused medications flushed down the toilet can contaminate water supplies."
    ]
};

// Global State
let selectedFile = null;

// ==================== INITIALIZATION & EVENT LISTENERS ====================
document.addEventListener('DOMContentLoaded', () => {
    // 1. Element Selection
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const previewSection = document.getElementById('previewSection');
    const imagePreview = document.getElementById('imagePreview');
    const classifyBtn = document.getElementById('classifyBtn');
    const resetBtn = document.getElementById('resetBtn');

    // 2. Attach Event Listeners
    if (uploadArea && fileInput) {
        uploadArea.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => handleFileSelect(e, imagePreview, previewSection, uploadArea));

        // Drag & Drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) handleFile(files[0], imagePreview, previewSection, uploadArea);
        });
    }

    if (classifyBtn) {
        classifyBtn.addEventListener('click', () => classifyImage(selectedFile));
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', resetApp);
    }

    // 3. Prevent Global Defaults
    document.addEventListener('dragover', (e) => e.preventDefault());
    document.addEventListener('drop', (e) => e.preventDefault());

    // 4. Load Initial Data
    initializeTabs();
    loadStatistics();
    loadHistory();
    loadAchievements();
});

// ==================== FILE HANDLING ====================
function handleFileSelect(e, imagePreview, previewSection, uploadArea) {
    const file = e.target.files[0];
    if (file) handleFile(file, imagePreview, previewSection, uploadArea);
}

function handleFile(file, imagePreview, previewSection, uploadArea) {
    if (!file.type.startsWith('image/')) {
        alert('Please upload an image file (PNG, JPG, JPEG)');
        return;
    }
    selectedFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        previewSection.classList.add('active');
        uploadArea.parentElement.style.display = 'none';
        document.getElementById('resultsSection').classList.remove('active');
        document.getElementById('qualityFeedback').style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// ==================== CLASSIFICATION ====================
async function classifyImage(file) {
    if (!file) {
        alert('Please select an image first');
        return;
    }

    const loadingSection = document.getElementById('loadingSection');
    const resultsSection = document.getElementById('resultsSection');
    const classifyBtn = document.getElementById('classifyBtn');

    loadingSection.classList.add('active');
    resultsSection.classList.remove('active');
    classifyBtn.disabled = true;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Classification failed');

        const data = await response.json();
        displayResults(data);

        // Trigger AI Recycling Coach after classification
        if (window.recyclingCoach) {
            setTimeout(() => {
                window.recyclingCoach.triggerAfterScan(data);
            }, 1000); // Delay 1 second for smooth UX
        }

        // Updates
        if (data.new_achievements && data.new_achievements.length > 0) {
            showAchievementNotification(data.new_achievements);
        }
        updateStatsBar(data.stats);

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to classify image. Please try again.');
    } finally {
        loadingSection.classList.remove('active');
        classifyBtn.disabled = false;
    }
}

// ==================== DISPLAY RESULTS ====================
function displayResults(data) {
    const { label, confidence, all_predictions, quality_check, recyclable, recyclable_confidence, recyclability_reason, eco_score } = data;

    // 1. Update Category Badge
    const categoryBadge = document.getElementById('categoryBadge');
    if (categoryBadge) {
        categoryBadge.textContent = label.toUpperCase().replace('_', ' ');
        categoryBadge.className = 'category-badge category-' + label.toLowerCase();
        categoryBadge.style.display = 'inline-block';
    }

    // 2. Update Recyclability Badge
    const recyclabilityBadge = document.getElementById('recyclabilityBadge');
    if (recyclabilityBadge) {
        if (recyclable !== undefined) {
            recyclabilityBadge.style.display = 'block';
            if (recyclable) {
                recyclabilityBadge.className = 'recyclability-badge recyclable';
                recyclabilityBadge.innerHTML = `
                    <div class="recyclable-icon">♻️</div>
                    <div class="recyclable-status">RECYCLABLE</div>
                    <div class="recyclable-confidence">${recyclable_confidence}% confidence</div>
                    <p class="recyclable-reason">${recyclability_reason}</p>
                `;
            } else {
                recyclabilityBadge.className = 'recyclability-badge non-recyclable';
                recyclabilityBadge.innerHTML = `
                    <div class="recyclable-icon">🚫</div>
                    <div class="recyclable-status">NON-RECYCLABLE</div>
                    <div class="recyclable-confidence">${recyclable_confidence}% confidence</div>
                    <p class="recyclable-reason">${recyclability_reason}</p>
                `;
            }
        } else {
            recyclabilityBadge.style.display = 'none';
        }
    }

    // 3. Update Eco-Score
    const ecoScoreContainer = document.getElementById('ecoScoreContainer');
    if (ecoScoreContainer && eco_score !== undefined) {
        ecoScoreContainer.style.display = 'block';
        const ecoScoreFill = document.getElementById('ecoScoreFill');
        const ecoScoreValue = document.getElementById('ecoScoreValue');
        ecoScoreFill.style.width = eco_score + '%';
        ecoScoreValue.textContent = eco_score + '/100';

        if (eco_score >= 80) ecoScoreFill.style.background = 'linear-gradient(90deg, #0ba360, #56ab2f)';
        else if (eco_score >= 60) ecoScoreFill.style.background = 'linear-gradient(90deg, #f2994a, #f2c94c)';
        else ecoScoreFill.style.background = 'linear-gradient(90deg, #eb3349, #f2994a)';
    }

    // 4. Quality Feedback
    const qualityFeedback = document.getElementById('qualityFeedback');
    const qualityMessages = document.getElementById('qualityMessages');
    if (qualityFeedback && quality_check && quality_check.score < 80) {
        qualityMessages.innerHTML = quality_check.feedback.map(f => `<p class="quality-message">${f}</p>`).join('');
        qualityFeedback.style.display = 'block';
    }

    // 5. Instructions & Confidence
    const disposalInstructions = document.getElementById('disposalInstructions');
    const confidenceHTML = createConfidenceDisplay(confidence, all_predictions);
    const instructions = disposalGuides[label.toLowerCase()] || 'No disposal instructions available.';
    const funFact = getRandomFact(label.toLowerCase());

    if (disposalInstructions) {
        disposalInstructions.innerHTML = `
            <h3>📋 Disposal Instructions</h3>
            <p>${instructions}</p>
            
            <div class="fun-fact-box">
                <h4>💡 Did You Know?</h4>
                <p>${funFact}</p>
            </div>
            
            ${confidenceHTML}
        `;
    }

    const resultsSection = document.getElementById('resultsSection');
    resultsSection.classList.add('active');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function createConfidenceDisplay(confidence, allPredictions) {
    let confidenceLevel, confidenceColor;
    if (confidence >= 80) {
        confidenceLevel = 'Very Confident';
        confidenceColor = '#0ba360';
    } else if (confidence >= 60) {
        confidenceLevel = 'Confident';
        confidenceColor = '#f2994a';
    } else {
        confidenceLevel = 'Uncertain';
        confidenceColor = '#eb3349';
    }

    const sortedPredictions = Object.entries(allPredictions).slice(0, 3);
    const predictionBars = sortedPredictions.map(([category, conf]) => `
        <div class="prediction-item">
            <span class="prediction-label">${category.charAt(0).toUpperCase().replace('_', ' ')}</span>
            <div class="prediction-bar-container">
                <div class="prediction-bar" style="width: ${conf}%"></div>
            </div>
            <span class="prediction-value">${conf}%</span>
        </div>
    `).join('');

    return `
        <div class="confidence-section">
            <h3>🎯 Confidence Score</h3>
            <div class="confidence-meter">
                <div class="confidence-bar" style="width: ${confidence}%; background: ${confidenceColor}">
                    ${confidence}%
                </div>
            </div>
            <p class="confidence-level" style="color: ${confidenceColor}">${confidenceLevel}</p>
            
            <div class="all-predictions">
                <h4>All Predictions:</h4>
                ${predictionBars}
            </div>
        </div>
    `;
}

// ==================== TABS, STATS, ACTIONS ====================
function initializeTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetPane = document.getElementById(tabName + 'Tab');
            if (targetPane) targetPane.classList.add('active');

            if (tabName === 'history') loadHistory();
            if (tabName === 'achievements') loadAchievements();
            if (tabName === 'stats') loadDetailedStats();
        });
    });
}

function resetApp() {
    selectedFile = null;
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');

    fileInput.value = '';
    document.getElementById('previewSection').classList.remove('active');
    document.getElementById('resultsSection').classList.remove('active');
    document.getElementById('loadingSection').classList.remove('active');
    uploadArea.parentElement.style.display = 'block';
    document.getElementById('imagePreview').src = '';
    document.getElementById('qualityFeedback').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==================== API HELPERS ====================
async function loadStatistics() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        updateStatsBar(stats);
    } catch (error) { console.error('Error loading stats:', error); }
}

function updateStatsBar(stats) {
    const elTotal = document.getElementById('totalScans');
    const elWeek = document.getElementById('thisWeek');
    const elAch = document.getElementById('achievements');
    if (elTotal) elTotal.textContent = stats.total || 0;
    if (elWeek) elWeek.textContent = stats.this_week || 0;
    if (elAch) elAch.textContent = stats.achievements_count || 0;
}

async function loadDetailedStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        const categoryStats = document.getElementById('categoryStats');
        const categories = stats.by_category || {};
        const total = stats.total || 1;

        if (categoryStats) {
            categoryStats.innerHTML = Object.entries(categories).map(([cat, count]) => {
                const percentage = ((count / total) * 100).toFixed(1);
                return `
                    <div class="category-stat-item">
                        <div class="category-stat-header">
                            <span class="category-name">${cat.charAt(0).toUpperCase().replace('_', ' ')}</span>
                            <span class="category-count">${count} (${percentage}%)</span>
                        </div>
                        <div class="category-bar-container">
                            <div class="category-bar category-${cat}" style="width: ${percentage}%"></div>
                        </div>
                    </div>
                `;
            }).join('') || '<p class="empty-state">No data yet</p>';
        }

        // Impact
        const totalItems = stats.total || 0;
        const elTrees = document.getElementById('treesSaved');
        if (elTrees) elTrees.textContent = Math.floor(totalItems * 0.05);
        document.getElementById('waterSaved').textContent = Math.floor(totalItems * 2.5) + 'L';
        document.getElementById('energySaved').textContent = Math.floor(totalItems * 0.3) + 'kWh';
        document.getElementById('co2Saved').textContent = Math.floor(totalItems * 0.5) + 'kg';

    } catch (error) { console.error('Error loading detailed stats:', error); }
}

async function loadHistory() {
    try {
        const response = await fetch('/api/history?limit=20');
        const history = await response.json();
        const historyGrid = document.getElementById('historyGrid');

        if (historyGrid) {
            if (history.length === 0) {
                historyGrid.innerHTML = '<p class="empty-state">No classifications yet. Start by uploading an image!</p>';
                return;
            }
            historyGrid.innerHTML = history.map(item => `
                <div class="history-card">
                    <img src="/${item.image_path}" alt="${item.predicted_class}">
                    <div class="history-info">
                        <span class="history-category category-${item.predicted_class}">${item.predicted_class.toUpperCase().replace('_', ' ')}</span>
                        <span class="history-confidence">${item.confidence}%</span>
                        <span class="history-time">${formatTime(item.timestamp)}</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) { console.error('Error loading history:', error); }
}

async function loadAchievements() {
    try {
        const response = await fetch('/api/achievements');
        const unlocked = await response.json();
        const achievementsGrid = document.getElementById('achievementsGrid');
        if (!achievementsGrid) return;

        const cards = achievementsGrid.querySelectorAll('.achievement-card');
        cards.forEach(card => {
            card.className = 'achievement-card locked';
            card.querySelector('.achievement-status').textContent = 'Locked';
        });

        unlocked.forEach(ach => {
            const card = Array.from(cards).find(c => c.querySelector('h3').textContent === ach.name);
            if (card) {
                card.classList.remove('locked');
                card.classList.add('unlocked');
                card.querySelector('.achievement-status').textContent = `Unlocked ${formatTime(ach.unlocked_at)}`;
            }
        });
    } catch (error) { console.error('Error loading achievements:', error); }
}

function showAchievementNotification(achievements) {
    const notification = document.getElementById('achievementNotification');
    const content = document.getElementById('achievementContent');
    if (!notification || !content) return;

    content.innerHTML = achievements.map(ach => `
        <div class="achievement-unlock">
            <h4>${ach.name}</h4>
            <p>${ach.description}</p>
        </div>
    `).join('');

    notification.style.display = 'block';
    setTimeout(() => { notification.style.display = 'none'; }, 5000);
}

function getRandomFact(category) {
    // Basic fallback if category not found
    const facts = funFacts[category] || funFacts.trash;
    return facts ? facts[Math.floor(Math.random() * facts.length)] : "Recycling saves energy!";
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;
    return date.toLocaleDateString();
}
