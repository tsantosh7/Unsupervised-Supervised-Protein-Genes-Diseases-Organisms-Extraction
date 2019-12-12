'''
Runs Flask web app server (on port 5200).
'''

__author__ = 'Santosh Tirunagari'



from flask import render_template, flash, Markup
from datetime import time
# from flask_cors import CORS

from flask import Flask, jsonify, request
from nltk.tokenize import wordpunct_tokenize, WordPunctTokenizer
from typing import List

from flair.data import Sentence, Token
from flair.models import SequenceTagger
import re

app = Flask(__name__)

# sequence_model = SequenceTagger.load('/mnt/droplet/nfs/gns/literature/Santosh_Tirunagari/GitHub/flair_models/ner/multi_bio_ner_model/EBI/best-model.pt')
flair_model = SequenceTagger.load('/nfs/gns/literature/Santosh_Tirunagari/GitHub/flair_models/ner/manual_annotated_dataset/best-model.pt')



def term_highlighter(text: str = None, terms: list = None) -> str:
    if not text or not terms:
        raise ValueError('Either the supplied text or list of terms and scores is empty or of type None')

    used_term_strs = set()

    for term in terms:

        # because here  each term is something like 'ProjectSummary:AI' followed by a float score
        # (this is just the format that solr returns the 'interesting terms' list).
        term_str = term[3]

        if type(term_str) != str:
            continue

        # prevent double highlighting
        if term_str in used_term_strs:
            continue

        used_term_strs.add(term_str)
        new_term = set()
        for s in filter(lambda x: term_str in x, wordpunct_tokenize(text)):
            new_term.add(s)
        try:
            new_term_str = list(new_term)[0]
        except:
            new_term_str = term_str

        if term[2] == 'GP':
            text = re.sub(r"\b%s\b" % new_term_str , '<span class=\'GP\'>' + new_term_str + '</span>', text)
        elif term[2] == 'DS':
            text = re.sub(r"\b%s\b" % new_term_str , '<span class=\'DS\'>' + new_term_str + '</span>', text)
        elif term[2] == 'OG':
            text = re.sub(r"\b%s\b" % new_term_str , '<span class=\'OG\'>' + new_term_str + '</span>', text)

    return text





def custom_tokenizer(text: str) -> List[Token]:
    """
    Tokenizer based on space character only.
    """
    tokens: List[Token] = []

    tokenizer = WordPunctTokenizer()

    text = tokenizer.tokenize(text)

    index = 0
    for index, word in enumerate(text):
        tokens.append(
            Token(
                text=word, start_position=index, whitespace_after=False
            )
        )

    return tokens



# app config and init
app = Flask(__name__)
# CORS(app)

app.secret_key = '20meerkats20'
app.config['CORS_HEADERS'] = 'Content-Type'

# Test endpoint to check if server is running
@app.route("/hello", methods=['GET'])
def hello():

    return jsonify({
        'message': 'Hi Santosh',
        "status": 200,
        "service": 'hello'
    })


@app.route("/pcse_ner", methods=['GET'])
def pcse_ner():

    # return jsonify({
    #     'message': 'Hi',
    #     "status": 200,
    #     "service": 'hello'
    # })
    return render_template('get_ner.html')


@app.route("/pcse_ner_predictor", methods=['GET'])
def pcse_ner_predictor():

    data_dict ={}
    text_sentence = request.args.get('text_sentence')

    if not text_sentence:
        return jsonify({
            'error': 'No parameters supplied',
            "status": 400,
            "service": 'pcse_ner_predictor'
        })

    sentence = Sentence(' '.join(wordpunct_tokenize(text_sentence)))
    # print(sentence)
    # print(text_sentence)
    flair_model.predict(sentence)

    # print(sentence.to_dict(tag_type='ner'))

    try:
        data_dict['tagged'] = sentence.to_dict(tag_type='ner')

        text_input = data_dict['tagged']['text']

        terms_entities = []
        for each_entity in data_dict['tagged']['entities']:
            terms_entities.append(
                [each_entity['start_pos'], each_entity['end_pos'], each_entity['type'], each_entity['text']])

        # print(text_input)
        # print(terms_entities)
        data_dict['highlighted_text'] = term_highlighter(text_input,terms_entities)

        data_dict['status'] = 200
    except:
        data_dict['status'] = 400

    if data_dict['status'] != 200:
        data_dict['status'] = 400
        return data_dict
    else:
        return data_dict


@app.route("/pcse_ner_multi_batch_predictor", methods=['POST'])
def pcse_ner_multi_batch_predictor():

    data_dict ={}
    text_sentence = request.form.get('text_sentence')

    if not text_sentence:
        return jsonify({
            'error': 'No parameters supplied',
            "status": 400,
            "service": 'pcse_ner_multi_batch_predictor'
        })

    sentences = []
    for each_sentence in text_sentence:
        sentences.append(Sentence(each_sentence, use_tokenizer=custom_tokenizer))
    # print(sentence)
    # print(text_sentence)
    flair_model.predict(sentence)

    # print(sentence.to_dict(tag_type='ner'))

    try:
        data_dict['tagged'] = sentence.to_dict(tag_type='ner')

        text_input = data_dict['tagged']['text']

        terms_entities = []
        for each_entity in data_dict['tagged']['entities']:
            terms_entities.append(
                [each_entity['start_pos'], each_entity['end_pos'], each_entity['type'], each_entity['text']])

        # print(text_input)
        # print(terms_entities)
        data_dict['highlighted_text'] = term_highlighter(text_input,terms_entities)

        data_dict['status'] = 200
    except:
        data_dict['status'] = 400

    if data_dict['status'] != 200:
        data_dict['status'] = 400
        return data_dict
    else:
        return data_dict



@app.route("/pcse_ner_highlighter", methods=['GET'])
def pcse_ner_highlighter():

    data_dict ={}
    text_sentence = request.args.get('text_sentence')

    if not text_sentence:
        return jsonify({
            'error': 'No parameters supplied',
            "status": 400,
            "service": 'pcse_ner_highlighter'
        })

    sentence = Sentence(' '.join(wordpunct_tokenize(text_sentence)))
    # print(sentence)
    # print(text_sentence)
    flair_model.predict(sentence)

    # print(sentence.to_dict(tag_type='ner'))

    try:
        data_dict['tagged'] = sentence.to_dict(tag_type='ner')

        text_input = data_dict['tagged']['text']

        terms_entities = []
        for each_entity in data_dict['tagged']['entities']:
            terms_entities.append(
                [each_entity['start_pos'], each_entity['end_pos'], each_entity['type'], each_entity['text']])

        # print(text_input)
        # print(terms_entities)
        data_dict['highlighted_text'] = term_highlighter(text_input,terms_entities)

        data_dict['status'] = 200
    except:
        data_dict['status'] = 400

    if data_dict['status'] != 200:
        data_dict['status'] = 400
        return data_dict
    else:
        return render_template('pcse_ner_output.html', text_highlighted= Markup(data_dict['highlighted_text']))





# Runs the flask server on the specified port (5200)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5201, debug=True)
