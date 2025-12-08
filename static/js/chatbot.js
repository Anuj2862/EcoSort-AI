// ==================== AI RECYCLING COACH CHATBOT ====================

class RecyclingCoach {
    constructor() {
        this.container = null;
        this.messagesArea = null;
        this.input = null;
        this.sendBtn = null;
        this.toggleBtn = null;
        this.currentContext = null;
        this.conversationHistory = [];
        this.isOpen = false;

        this.init();
    }

    init() {
        // Create chatbot HTML
        this.createChatbotHTML();

        // Get elements
        this.container = document.getElementById('chatbotContainer');
        this.messagesArea = document.getElementById('chatbotMessages');
        this.input = document.getElementById('chatbotInput');
        this.sendBtn = document.getElementById('chatbotSendBtn');
        this.toggleBtn = document.getElementById('chatbotToggle');

        // Attach event listeners
        this.attachEventListeners();
    }

    createChatbotHTML() {
        const chatbotHTML = `
            <!-- Chatbot Toggle Button -->
            <button id="chatbotToggle" class="chatbot-toggle">
                ♻️
            </button>

            <!-- Chatbot Container -->
            <div id="chatbotContainer" class="chatbot-container">
                <!-- Header -->
                <div class="chatbot-header">
                    <div class="chatbot-title">
                        <span class="chatbot-mascot">♻️</span>
                        <span>Recycling Coach</span>
                    </div>
                    <button class="chatbot-close" id="chatbotClose">×</button>
                </div>

                <!-- Messages Area -->
                <div id="chatbotMessages" class="chatbot-messages">
                    <!-- Messages will be inserted here -->
                </div>

                <!-- Input Area -->
                <div class="chatbot-input-area">
                    <input 
                        type="text" 
                        id="chatbotInput" 
                        class="chatbot-input" 
                        placeholder="Ask me anything..."
                        autocomplete="off"
                    />
                    <button id="chatbotSendBtn" class="chatbot-send-btn">
                        ➤
                    </button>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    attachEventListeners() {
        // Toggle chatbot
        this.toggleBtn.addEventListener('click', () => this.toggle());
        document.getElementById('chatbotClose').addEventListener('click', () => this.close());

        // Send message
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        this.container.classList.add('active');
        this.toggleBtn.classList.add('hidden');
        this.isOpen = true;
        this.input.focus();

        // Welcome message if first time
        if (this.conversationHistory.length === 0) {
            this.addBotMessage("Hi! I'm your Recycling Coach! 🌍 I'm here to help you make eco-friendly choices. How can I assist you today?", true);
        }
    }

    close() {
        this.container.classList.remove('active');
        this.toggleBtn.classList.remove('hidden');
        this.isOpen = false;
    }

    // Called after classification
    triggerAfterScan(scanData) {
        this.currentContext = scanData;
        this.open();

        const { label, confidence, recyclable, eco_score } = scanData;
        const categoryName = label.replace('_', ' ').toUpperCase();

        // Greeting message
        const greeting = `Great job scanning! 🎉 That's ${categoryName} with ${confidence}% confidence. ${recyclable ? "It's recyclable! ♻️" : ""}`;
        this.addBotMessage(greeting);

        // Quick actions
        this.addQuickActions();
    }

    addQuickActions() {
        const actionsHTML = `
            <div class="quick-actions">
                <button class="quick-action-btn" data-action="disposal">
                    🗑️ How to dispose?
                </button>
                <button class="quick-action-btn" data-action="co2">
                    🌍 CO₂ saved?
                </button>
                <button class="quick-action-btn" data-action="tip">
                    💡 Recycling tip
                </button>
                <button class="quick-action-btn" data-action="impact">
                    📊 My impact
                </button>
            </div>
        `;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message bot';
        messageDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-bubble">
                What would you like to know?
                ${actionsHTML}
            </div>
        `;

        this.messagesArea.appendChild(messageDiv);
        this.scrollToBottom();

        // Attach quick action listeners
        messageDiv.querySelectorAll('.quick-action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                this.handleQuickAction(action);
            });
        });
    }

    handleQuickAction(action) {
        switch (action) {
            case 'disposal':
                this.addUserMessage("How do I dispose of this?");
                this.getDisposalInstructions();
                break;
            case 'co2':
                this.addUserMessage("How much CO₂ did I save?");
                this.getCO2Impact();
                break;
            case 'tip':
                this.addUserMessage("Give me a recycling tip");
                this.getRecyclingTip();
                break;
            case 'impact':
                this.addUserMessage("Show me my environmental impact");
                this.getImpactStats();
                break;
        }
    }

    async sendMessage() {
        const message = this.input.value.trim();
        if (!message) return;

        this.addUserMessage(message);
        this.input.value = '';
        this.sendBtn.disabled = true;

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Call backend API with Gemini
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    context: this.currentContext,
                    history: this.conversationHistory.slice(-5) // Last 5 messages
                })
            });

            const data = await response.json();
            this.removeTypingIndicator();
            this.addBotMessage(data.response);

        } catch (error) {
            console.error('Chat error:', error);
            this.removeTypingIndicator();
            this.addBotMessage("Oops! I'm having trouble connecting. Please try again! 😅");
        } finally {
            this.sendBtn.disabled = false;
        }
    }

    getDisposalInstructions() {
        if (!this.currentContext) {
            this.addBotMessage("Please scan an item first so I can help you! 📸");
            return;
        }

        const category = this.currentContext.label;
        this.showTypingIndicator();

        setTimeout(() => {
            this.removeTypingIndicator();

            // Get disposal guide from existing data
            const guide = disposalGuides[category] || "No disposal instructions available.";
            this.addBotMessage(`Here's how to dispose of your ${category.replace('_', ' ')}:\n\n${guide}\n\nYou're making a difference! 🌱`);
        }, 1000);
    }

    getCO2Impact() {
        this.showTypingIndicator();

        setTimeout(() => {
            this.removeTypingIndicator();

            const impact = `By properly sorting this waste, you've saved:\n\n⚡ 0.3 kWh of energy\n💧 2.5 liters of water\n🌫️ 0.5 kg of CO₂\n\nThat's like charging your phone 30 times! 📱\n\nKeep up the great work! 💪`;

            this.addBotMessage(impact);
        }, 1000);
    }

    getRecyclingTip() {
        this.showTypingIndicator();

        const tips = [
            "💡 Always rinse containers before recycling - contaminated items can ruin entire batches!",
            "💡 Flatten cardboard boxes to save space in recycling bins and trucks!",
            "💡 Remove caps from plastic bottles - they're often made of different plastic types!",
            "💡 Pizza boxes with grease can't be recycled, but clean parts can be composted!",
            "💡 Aluminum foil can be recycled if you ball it up to at least golf ball size!",
            "💡 Glass can be recycled endlessly without losing quality - it's infinitely recyclable!",
            "💡 Shredded paper is harder to recycle - try to keep paper whole when possible!",
            "💡 Check the recycling number on plastics - 1, 2, and 5 are most commonly accepted!"
        ];

        const randomTip = tips[Math.floor(Math.random() * tips.length)];

        setTimeout(() => {
            this.removeTypingIndicator();
            this.addBotMessage(randomTip);
        }, 1000);
    }

    async getImpactStats() {
        this.showTypingIndicator();

        try {
            const response = await fetch('/api/stats');
            const stats = await response.json();

            this.removeTypingIndicator();

            const message = `🌟 Your Environmental Impact:\n\n📊 Total scans: ${stats.total || 0}\n🌳 Trees saved: ${Math.floor((stats.total || 0) * 0.05)}\n💧 Water saved: ${Math.floor((stats.total || 0) * 2.5)}L\n⚡ Energy saved: ${Math.floor((stats.total || 0) * 0.3)} kWh\n🌫️ CO₂ reduced: ${Math.floor((stats.total || 0) * 0.5)} kg\n\nYou're a recycling hero! 🦸`;

            this.addBotMessage(message);
        } catch (error) {
            this.removeTypingIndicator();
            this.addBotMessage("I couldn't fetch your stats right now. Try again later! 📊");
        }
    }

    addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message user';
        messageDiv.innerHTML = `
            <div class="message-avatar">👤</div>
            <div class="message-bubble">${this.escapeHtml(text)}</div>
        `;

        this.messagesArea.appendChild(messageDiv);
        this.scrollToBottom();

        this.conversationHistory.push({ role: 'user', content: text });
    }

    addBotMessage(text, skipHistory = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message bot';
        messageDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-bubble">${this.formatMessage(text)}</div>
        `;

        this.messagesArea.appendChild(messageDiv);
        this.scrollToBottom();

        if (!skipHistory) {
            this.conversationHistory.push({ role: 'bot', content: text });
        }
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message bot';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;

        this.messagesArea.appendChild(typingDiv);
        this.scrollToBottom();
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) indicator.remove();
    }

    scrollToBottom() {
        this.messagesArea.scrollTop = this.messagesArea.scrollHeight;
    }

    formatMessage(text) {
        // Convert newlines to <br>
        return this.escapeHtml(text).replace(/\n/g, '<br>');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize chatbot when DOM is ready
let recyclingCoach;
document.addEventListener('DOMContentLoaded', () => {
    recyclingCoach = new RecyclingCoach();
});

// Export for use in app.js
window.recyclingCoach = recyclingCoach;
