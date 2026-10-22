# CivicAI — AI-Powered Government Grievance Classification and Routing System

CivicAI is an NLP-based web application designed to analyze citizens' complaints, classify them into relevant categories, suggest the responsible government department, and estimate complaint urgency. It demonstrates how Natural Language Processing and Machine Learning can help organize and streamline the grievance management process.

## Overview

Citizens frequently report issues related to water supply, electricity, roads, sanitation, public safety, and other civic services. Manually reviewing and forwarding these complaints can require significant effort.

CivicAI aims to simplify this process by automatically analyzing complaint text and providing useful information to support complaint management.

## Features

- **Complaint Classification:** Predicts the category of a complaint using a TF-IDF and Logistic Regression model.
- **Department Routing:** Maps the predicted complaint category to the relevant department.
- **Urgency Detection:** Estimates urgency using predefined keywords and rules.
- **Named Entity Extraction:** Identifies useful information from complaint text using pattern-based extraction and optional spaCy support.
- **Text Summarization:** Generates a concise complaint summary using an optional Gemini integration, with an extractive fallback.
- **Similar Complaint Detection:** Finds complaints with similar text using Sentence Transformers when available, with a TF-IDF-based fallback.
- **Batch Analysis:** Analyzes multiple complaints.
- **Complaint History:** Stores and displays complaint records using SQLite.
- **Model Evaluation:** Provides tools for evaluating the complaint classification model.
- **Interactive Dashboard:** Presents complaint information through a Streamlit interface.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application and dashboard |
| Pandas | Data handling |
| Scikit-learn | Machine learning and text classification |
| TF-IDF | Text feature extraction |
| Logistic Regression | Complaint category prediction |
| spaCy | Optional named entity recognition |
| Sentence Transformers | Optional semantic similarity |
| Google Gemini API | Optional AI-based summarization |
| SQLite | Local complaint data storage |
| Regular Expressions | Text pattern and entity extraction |

## Project Structure

```text
CivicAI_NLP_Project/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── data/
│   └── sample_complaints.csv
├── scripts/
│   ├── train_classifier.py
│   ├── evaluate_classifier.py
│   └── seed_data.py
├── src/
│   ├── preprocessing.py
│   ├── classification.py
│   ├── ner_extraction.py
│   ├── urgency_detection.py
│   ├── department_routing.py
│   ├── summarization.py
│   ├── similarity.py
│   ├── database.py
│   └── pipeline.py
└── tests/
    └── test_pipeline.py
```

## How It Works

1. **Complaint submission:** The user enters a civic complaint in natural language.
2. **Text preprocessing:** The application cleans and normalizes the complaint text.
3. **Feature extraction:** TF-IDF converts the text into numerical features.
4. **Classification:** Logistic Regression predicts the complaint category.
5. **Department routing:** A predefined mapping suggests the responsible department.
6. **Additional NLP analysis:** The system estimates urgency, extracts entities, generates a summary, and searches for similar complaints where supported.
7. **Storage and display:** The application displays the results and can save complaint records in SQLite.

## Installation and Setup

### Prerequisites

- Python 3.10 or a compatible Python version supported by the dependencies
- pip
- Git (optional, for cloning the repository)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CivicAI.git
cd CivicAI
```

Replace `YOUR_USERNAME` with your GitHub username. If your repository has a different name, use its actual URL and folder name.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python and pip executables directly.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure optional environment variables

Copy `.env.example` to `.env` and add the required values for any optional integrations you want to use.

For example:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The Gemini integration is optional if the application can use its fallback summarization method. Never commit `.env` or publish API keys to GitHub.

### 5. Run the application

From the project root directory, run:

```bash
streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser.

## Sample Complaint

**Input:**

> The electricity supply in our area has been interrupted repeatedly for the past three days. Several households are affected, and a damaged electrical wire is hanging near a local school. Please arrange an urgent inspection and restore the power supply.

CivicAI analyzes the complaint and displays its predicted category, suggested department, estimated urgency, and other available analysis results.

The exact output depends on the model prediction and the application's rules.

## Dataset

The project includes a sample dataset containing 120 synthetic complaints across 12 categories. These examples are intended for demonstrating the classification pipeline.

Because the dataset is small and synthetic, evaluation results may not represent performance on real-world government complaints. A larger, representative, and appropriately anonymized dataset would be required for production use.

## Model and Evaluation

The complaint classifier uses:

- **TF-IDF:** Represents complaint text as numerical features.
- **Logistic Regression:** Learns patterns from labelled complaint examples and predicts complaint categories.
- **Evaluation metrics:** Accuracy, precision, recall, and F1-score can be used to assess classification performance.

A reliable evaluation should use held-out test data that is separate from the training data.

## Limitations

- The prototype uses a limited synthetic dataset.
- Urgency detection is rule-based and may not understand every context.
- Entity extraction may miss information or identify incorrect entities.
- Optional AI integrations require additional configuration and dependencies.
- SQLite data stored on a cloud deployment may not persist reliably across restarts or rebuilds.
- The application is not connected to live government departments or official grievance systems.

## Future Scope

Potential improvements include:

- Training and evaluating the model on larger, real-world anonymized complaint datasets.
- Supporting regional Indian languages.
- Improving urgency detection with labelled training data.
- Adding citizen, officer, and administrator authentication.
- Integrating a hosted database for reliable data persistence.
- Adding complaint status tracking and notifications.
- Integrating with official grievance-management systems, subject to authorization.

