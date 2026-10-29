# LGB Social Bot Detection

## Overview
LGB Social Bot Detection is a machine-learning web application designed to classify text as bot-related or non-bot-related using a trained text-classification model.

## Features
- Flask-based web application
- Text-based prediction interface
- Machine-learning model and text vectorizer
- Web pages for interacting with the application

## Technologies Used
- Python
- Flask
- Pandas
- Scikit-learn
- HTML and CSS

## Project Structure
- `app.py` — Main Flask application
- `dataset/` — Dataset files
- `model/` — Trained model, vectorizer, and model-related scripts
- `templates/` — HTML templates
- `static/` — CSS and other static assets

## Setup and Installation

1. Install Python.
2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open the local URL displayed in the terminal.

## Dataset
The project includes a dataset used for text classification. Review the dataset documentation for its actual columns, labels, and limitations.

## Notes
This project is intended for educational and demonstration purposes. Predictions depend on the dataset and the trained model and should not be treated as definitive proof that an account is a social bot.

## Author
Nikhil Goud Panjala