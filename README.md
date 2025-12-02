# innopolis-pmldl-bloombuddy
## 💡 Project Idea
The goal of the project is to develop an AI-powered system that analyzes images of plant
leaves, detects diseases, and provides actionable recommendations for treatment. The project
combines Computer Vision for image analysis and Machine Learning / NLP for recommendation
generation.

Plant diseases are a major cause of crop loss worldwide. Early detection and timely inter-
vention can significantly reduce agricultural losses and increase crop yield. This tool can help
farmers, gardeners, and agricultural researchers monitor plant health efficiently, even without
expert knowledge.

## 🌱 Features

- 🖼 **Upload Leaf Images** – Easily upload images of plant leaves to get instant analysis.  
- 🩺 **Automatic Disease Classification** – Detect whether the leaf is healthy or affected by a disease.    
- 💡 **Actionable Recommendations** – Provides treatment and care suggestions for detected diseases, powered by NLP knowledge base.  
- 🌐 **User-Friendly Interface** – Intuitive web interface that allows quick interaction even without prior expertise.  
- 🔍 **Visual Explanations** – Optionally highlight affected areas on leaves to understand the model's decisions.  

##  🗺️ Roadmap

### 📦 Stage 0: Datasets
- ✅ Collect and organize datasets  
- ✅ Perform preprocessing (resizing, normalization, cleaning)  
- ✅ Explore datasets and visualize examples  
- ✅ Split data into training, validation, and testing sets  

### 🟡 Stage 1: Core Functionality (MVP)
- 🟡 Basic image classification of healthy vs. diseased leaves  
- 🟡 Web interface to upload leaf images  
- 🟡 Display predicted disease with confidence score  

### 🚀 Stage 2: Model & Analysis Enhancements
- 🟡 Experiment with different CV and DL architectures  
- 🟡 Compare training strategies (from scratch vs. transfer learning)  
- 🟡 Highlight diseased regions on the leaf (localization/segmentation)  
- 🟡 Add visual explanations to show how the model makes decisions  
- 🟡 Apply data augmentation techniques to improve generalization  
- 🟡 Evaluate results with appropriate metrics and visualizations  

### 🤖 Stage 3: NLP & Recommendations
- ✅ Provide actionable treatment or care recommendations based on predictions  
- 🟡 Implement a simple assistant (chat/FAQ) to answer user questions  
- 🟡 Add multi-language support for both interface and recommendations  

### 📲 Stage 4: Deployment & Usability
- 🟡 Enable batch image upload and processing  
- 🟡 Export results/reports in CSV or Excel format  
- 🟡 Optimize the model for faster inference and lighter deployment  
- 🟡 Explore deployment on mobile or embedded devices  

## ⚙️ How to Run the Application

Follow these steps to run the project locally:

1. Install dependencies:
```pip install -r requirements.txt```

2. Start the backend service:
```uvicorn backend.main:app --reload ```

4. Start the application:
```python frontend/app.py```

## 👥 Contributors
- Azalia Alisheva
- Aisylu Fattakhova
- Kira Maslennikova
