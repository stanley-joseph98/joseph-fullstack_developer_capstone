import requests


def get_sentiment(review_text):
    try:
        # URL of the Flask app deployed on IBM Code Engine
        url = f"https://sentianalyzer.1oc2fdvq17zq.us-south.codeengine.appdomain.cloud/analyze/{review_text}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        sentiment_data = response.json()  # Assuming the Flask app returns JSON
        return sentiment_data.get('sentiment', 'neutral')  # Extract sentiment
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
        return 'neutral'