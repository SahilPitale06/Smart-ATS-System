# Smart ATS System

This repository contains the code and resources for an **Applicant Tracking System (ATS)** developed as a project. The system is designed to help employers manage job applications efficiently by leveraging **Natural Language Processing (NLP)** and **Machine Learning (ML)** techniques.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Model Training](#model-training)
- [Evaluation](#evaluation)
- [Contributors](#contributors)
- [License](#license)

## Overview

An **Applicant Tracking System (ATS)** is a tool used by employers to streamline the hiring process by automating job application screening. This project integrates **Resume Parsing**, **Job Matching**, and **Candidate Ranking** functionalities using **Python, Flask, and Machine Learning models**.

## Features

- **Resume Parsing**: Extracts structured data from resumes.
- **Keyword Matching**: Compares resumes against job descriptions.
- **Candidate Ranking**: Assigns scores based on skill-job alignment.
- **Web Interface**: Built using Flask for easy interaction.

## Installation

To run this project locally, ensure you have Python installed. Then, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SahilPitale06/Smart-ATS-System.git
   cd Smartr-ATS-System
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *Note: If `requirements.txt` is not available, manually install the necessary packages:*

   ```bash
   pip install numpy pandas scikit-learn flask spacy
   ```

4. **Download NLP model for resume parsing:**

   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

1. **Run the Flask application:**

   ```bash
   python app.py
   ```

2. **Access the web interface:**

   Open a web browser and navigate to `http://127.0.0.1:5000/`. You can upload resumes and job descriptions to see the ranking results.

## Model Training

The model training process is documented in the Jupyter Notebook `ats_model.ipynb`. It includes:

- Data Preprocessing: Cleaning and extracting key details from resumes.
- Feature Engineering: Using NLP techniques to convert text into numerical features.
- Model Selection: Training ML models such as **Logistic Regression** and **Random Forest** for candidate ranking.
- Model Serialization: Saving the trained model (`ats_model.pkl`) for future use.

## Evaluation

The trained model's performance is evaluated using metrics like **accuracy, precision, recall, and F1-score**. Detailed evaluation results and visualizations are available in the Jupyter Notebook.

## Contributors

- [Sahil Pitale](https://github.com/SahilPitale06)
- [Sanket Pawar](https://github.com/Sankkkett)

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

*Note: This README provides a general overview. For detailed explanations and code insights, refer to the Jupyter Notebook and Python scripts in the repository.*
