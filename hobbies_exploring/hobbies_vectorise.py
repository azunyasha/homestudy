import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_excel("hobbies.xlsx")
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data.text_clean)
print(X.shape)
