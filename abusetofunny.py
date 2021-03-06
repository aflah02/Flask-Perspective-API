from googleapiclient import discovery
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.tokenize import word_tokenize     
from textblob import TextBlob
import pandas as pd
import random
import nltk
from funny_words import build_n_gram
import json
sid = SentimentIntensityAnalyzer()
df = pd.read_excel('expandedLexicon.xlsx')
df_words = df['Word_type']
ls_onlywords = []
ls_words = []
my_file = open("stopwords.txt", "r")
content_list = my_file.readlines()
stop_words = []
for i in range(len(content_list)):
    stop_words.append(content_list[i].strip('\n'))
for i in df_words:
    ls_words.append(i)
for i in range(len(ls_words)):
    ls_onlywords.append(ls_words[i].split("_")[0])
API_KEY=''
def word_gen(type):
    while True:
        replacement_word = list(build_n_gram().split())[0]
        text = word_tokenize(replacement_word)
        if nltk.pos_tag(text)[0][-1] == type:
            return replacement_word
        
def abusetofunny(message):
    service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=API_KEY, discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,)

    analyze_request = {
      'comment': { 'text': message },
      'requestedAttributes': {'TOXICITY': {}}
    }

    response = service.comments().analyze(body=analyze_request).execute()

    result = eval(json.dumps(response, indent=2))
    toxicity_score = result["attributeScores"]["TOXICITY"]['spanScores'][0]['score']['value']
    if toxicity_score < 0.5:
        return message
    else:
        sentences = list(message.split('.'))
        ls_sentiment = []
        for i in range(len(sentences)):
            ls_words_remove_stop = list(sentences[i].split())
            for i in ls_words_remove_stop:
                if i in stop_words:
                    ls_words_remove_stop.remove(i)
            sentence_no_stop_words = ' '.join(ls_words_remove_stop)
            ss = sid.polarity_scores(sentence_no_stop_words)
            for k in sorted(ss):
                if k == 'compound':
                    ls_sentiment.append(ss[k])
        for m in range(len(sentences)):
            if ls_sentiment[m] > 0:
                pass
            else:
                ls_sentence = sentences[m].split()
                for j in range(len(ls_sentence)):
                    if ls_sentence[j].lower() in ls_onlywords:
                        blob = TextBlob(ls_sentence[j].lower())
                        tag = blob.tags[0][-1]
                        if tag == 'RB':
                            ls_sentence[j] = word_gen('RB')
                        elif tag == 'NN':
                            ls_sentence[j] = word_gen('NN')
                        elif tag == 'JJ':
                            ls_sentence[j] = word_gen('JJ')
                        else:
                            ls_sentence[j] = list(build_n_gram().split())[0]
                    sentences[m] = ' '.join(ls_sentence)
        return ' '.join(sentences)
    