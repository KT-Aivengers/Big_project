from tensorflow.keras.models import load_model
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

with open('fillow/tokenizer.pickle', 'rb') as handle:
    loaded_tokenizer = pickle.load(handle)
# returns a compiled model identical to the previous one
loaded_model = load_model('fillow/spam_detection.h5')

def detect_spam(text):
    
    text = loaded_tokenizer.texts_to_sequences([text.text])
    text = pad_sequences(text, maxlen = 189)
    prob = loaded_model.predict(text)[0][0]
    result = 1 if prob >= 0.5 else 0
    if result:
        answer="spam"
    else:
        answer="not spam"
    return answer
