'''
Runs Flask web app server (on port 5200).
'''

__author__ = 'Santosh Tirunagari'



from flask import render_template, Markup


from flask import Flask, jsonify, request
from nltk.tokenize import wordpunct_tokenize, WordPunctTokenizer

import spacy
import re

from spacy import util


# app config and init
app = Flask(__name__)
# CORS(app)

app.secret_key = '20meerkats20'
app.config['CORS_HEADERS'] = 'Content-Type'



best_model_path = '/nfs/misc/literature/Santosh_Tirunagari/GitHub/spacy_models/pretrain_exp/best/'

print("Loading from", best_model_path)
nlp2 = util.load_model_from_path(best_model_path)

print("Loading finsihed!")

def term_highlighter(text: str = None, terms: list = None) -> str:
    if not text or not terms:
        raise ValueError('Either the supplied text or list of terms and scores is empty or of type None')

    used_term_strs = set()

    for term in terms:

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



# Test endpoint to check if server is running
@app.route("/hello", methods=['GET'])
def hello():

    return jsonify({
        'message': 'Hi Santosh',
        "status": 200,
        "service": 'hello',
        "host" : request.host_url
    })


@app.route("/spaCy_ner", methods=['GET'])
def spaCy_ner():

    # return jsonify({
    #     'message': 'Hi',
    #     "status": 200,
    #     "service": 'hello'
    # })
    return render_template('get_ner.html')


@app.route("/spaCy_ner_predictor", methods=['GET'])
def spaCy_ner_predictor():

    data_dict ={}
    text_sentence = request.args.get('text_sentence')

    if not text_sentence:
        return jsonify({
            'error': 'No parameters supplied',
            "status": 400,
            "service": 'spaCy_ner_predictor'
        })


    try:
        doc = nlp2(text_sentence)

        terms_entities = []
        for ent in doc.ents:
            terms_entities.append(
                [ent.start_char, ent.end_char, ent.label_, ent.text])

        # print(text_input)
        # print(terms_entities)
        # data_dict['highlighted_text'] = term_highlighter(text_sentence,terms_entities)
        data_dict['annotations'] = terms_entities

        data_dict['status'] = 200
    except:
        data_dict['status'] = 400

    if data_dict['status'] != 200:
        data_dict['status'] = 400
        return jsonify(data_dict)
    else:
        return jsonify(data_dict)


@app.route("/spaCy_ner_highlighter", methods=['GET'])
def spaCy_ner_highlighter():

    data_dict ={}
    text_sentence = request.args.get('text_sentence')

    if not text_sentence:
        return jsonify({
            'error': 'No parameters supplied',
            "status": 400,
            "service": 'spaCy_ner_highlighter'
        })

    try:
        doc = nlp2(text_sentence)

        terms_entities = []
        for ent in doc.ents:
            terms_entities.append(
                [ent.start_char, ent.end_char, ent.label_, ent.text])

        # print(text_input)
        # print(terms_entities)
        data_dict['highlighted_text'] = term_highlighter(text_sentence,terms_entities)

        data_dict['status'] = 200
    except:
        data_dict['status'] = 400

    if data_dict['status'] != 200:
        data_dict['status'] = 400
        return data_dict
    else:
        return render_template('spaCy_ner_output.html', text_highlighted= Markup(data_dict['highlighted_text']))



# Runs the flask server on the specified port (5200)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5200, debug=True)
