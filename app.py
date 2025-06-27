from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model and vectorizer
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# Load trigram files
common_trigrams = pd.read_excel('common_trigrams.xlsx')['Trigram'].str.lower().tolist()
uncommon_trigrams = pd.read_excel('top_100_uncommon_trigrams.xlsx')['Trigram'].str.lower().tolist()

# Trigram matching function
def count_matching_trigrams(text, trigram_list):
    text = text.lower()
    return sum(1 for trigram in trigram_list if trigram in text)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    news = request.form['news']
    vect = vectorizer.transform([news])
    prediction = model.predict(vect)[0]

    common_matches = count_matching_trigrams(news, common_trigrams)
    uncommon_matches = count_matching_trigrams(news, uncommon_trigrams)

    # Final basic prediction
    if prediction == 1:
        main_result = "🟢 This News is True"
    else:
        main_result = "🔴 This News is Fake"

    # Add trigram info ONLY if matches > 0
    extra_info = ""
    if common_matches > 0 or uncommon_matches > 0:
        parts = []
        if common_matches > 0:
            parts.append(f"✅ {common_matches} common trigrams")
        if uncommon_matches > 0:
            parts.append(f"⚠ {uncommon_matches} uncommon trigrams")
        extra_info = " (" + " & ".join(parts) + ")"

    # Combine and send
    final_output = main_result + extra_info
    return render_template('index.html', prediction_text=final_output)

if __name__ == "__main__":
    app.run(debug=True)
