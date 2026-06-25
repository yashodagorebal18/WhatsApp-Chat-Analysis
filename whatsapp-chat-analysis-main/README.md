# 💬 Advanced WhatsApp Chat Analysis Platform

> A Full-Stack Data Analysis Application for WhatsApp Conversations

## 🎯 Project Overview

This is a comprehensive **Full-Stack Web Application** designed to analyze WhatsApp chat conversations with advanced analytics, sentiment analysis, and beautiful visualizations. Perfect for a final-year project showcasing both frontend and backend development expertise.

### ✨ Key Features

#### 📊 **Overview Dashboard**
- Total messages, words, media, and links statistics
- Monthly and daily timeline visualizations
- Weekly activity heatmaps
- Busiest day and month analysis
- Group-level user activity comparison

#### 🔬 **Detailed Analytics**
- **Emoji Analysis**: Most used emojis with distribution pie charts
- **Word Cloud**: Visual representation of frequent words
- **Word Frequency**: Top 15 most frequently used words

#### 💡 **Advanced Insights**
- **Sentiment Analysis**: Classify messages as positive, negative, or neutral
- **Response Time Analysis**: Average time between messages
- **Conversation Statistics**: Message length and word count metrics
- **Weekly Distribution**: Activity patterns across days of week

#### 🔄 **Comparison Features**
- Compare multiple users' messaging patterns
- Word statistics across users
- Activity level comparisons

---

## 🏗️ Architecture (Full-Stack)

### Two-Tier Architecture

```
┌─────────────────────────────────────────────┐
│         FRONTEND (Streamlit)                │
│  - Interactive Dashboard                    │
│  - File Upload & Real-time Visualizations   │
│  - Beautiful Charts (Plotly, Matplotlib)    │
└────────────────┬────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────┐
│         BACKEND (Python/Flask)              │
│  - REST API Endpoints                       │
│  - Data Preprocessing & Parsing             │
│  - Advanced Analytics Engine                │
│  - Sentiment Analysis & NLP                 │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend
- **Streamlit** - Interactive web interface
- **Plotly** - Interactive visualizations
- **Matplotlib & Seaborn** - Static charts
- **Wordcloud** - Word cloud generation

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - REST API server
- **Pandas** - Data manipulation
- **TextBlob** - Sentiment analysis
- **Regular Expressions** - Chat parsing

---

## 📋 Installation & Setup

### Prerequisites
```bash
Python 3.8 or higher
pip (Python package manager)
```

### Installation Steps

```bash
# 1. Clone repository
git clone <repository-url>
cd whatsapp-chat-analysis

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLP data
python -c "import nltk; nltk.download('punkt')"
```

---

## 🚀 Running the Application

### Option 1: Enhanced Streamlit App (Recommended)
```bash
streamlit run app_enhanced.py
```

### Option 2: Original Streamlit App
```bash
streamlit run app.py
```

### Option 3: Backend API
```bash
python api_backend.py
# API available at http://localhost:5000
```

---

## 📁 Project Structure

```
whatsapp-chat-analysis/
├── app.py                    # Original Streamlit app
├── app_enhanced.py          # Enhanced version with advanced features
├── api_backend.py           # Flask REST API backend
├── preprocessor.py          # Chat parsing & preprocessing
├── helper.py                # Analytics helper functions
├── advanced_analytics.py     # Sentiment & advanced statistics
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

---

## 💻 Expected Chat Format

```
DD/M/YYYY, HH:MM - Username: Message

Example:
15/1/2021, 9:45 - John: Hey everyone! 👋
15/1/2021, 9:46 - Sarah: Hi John, how are you? 😄
```

**Export from WhatsApp:**
1. Long-press chat → More → Export Chat (without media)
2. Save as .txt file

---

## 📊 Analysis Capabilities

### Statistics
- Message count, word count, media/links shared
- Average message length and words per message
- Message distribution by day of week

### Visualizations
- Monthly & daily timelines
- Activity heatmaps
- Word clouds & word frequency charts
- Emoji distribution pie charts
- User comparison bar charts

### Advanced Analytics
- **Sentiment Classification** (Positive/Negative/Neutral)
- **Response Time** (average, median, gaps)
- **Conversation Patterns** (temporal analysis)
- **Emoji Analysis** (usage frequency)
- **Word Frequency** (top N words)

---

## 🎓 Final Year Project Highlights

✅ **Full-Stack Application** - Both frontend and backend  
✅ **Data Analysis** - Advanced NLP and statistics  
✅ **User Interface** - Professional, interactive dashboard  
✅ **API Design** - RESTful backend endpoints  
✅ **Code Quality** - Modular, documented code  
✅ **Innovation** - Sentiment analysis, comparisons  
✅ **Documentation** - Complete README and code comments  

---

## 📈 Future Enhancements

- Database integration (SQLite/PostgreSQL)
- User authentication
- PDF/Excel export functionality
- Machine learning predictions
- Cloud deployment (AWS/Heroku)
- Mobile application
- Real-time analysis
- Multi-language support

---

## 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/upload` | POST | Upload chat file |
| `/api/stats/<user>` | GET | User statistics |
| `/api/sentiment/<user>` | GET | Sentiment analysis |
| `/api/words/<user>` | GET | Word frequency |
| `/api/emojis/<user>` | GET | Emoji analysis |
| `/api/response-time/<user>` | GET | Response time stats |

---

## 📝 License

MIT License - Open source project

---

**Created for Final Year Project - Full-Stack Data Analysis Application**
