import pandas as pd
import string

data = pd.read_excel('hobbies.xlsx')
data['text_clean'] = data.text.apply(lambda x: x.translate(str.maketrans('','', string.punctuation)).lower())
data.to_excel('hobbies.xlsx')
