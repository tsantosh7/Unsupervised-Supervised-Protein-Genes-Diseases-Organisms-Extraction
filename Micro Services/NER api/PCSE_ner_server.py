'''
Runs Flask web app server (on port 5200).
'''

__author__ = 'Santosh Tirunagari'


from flask import Flask, jsonify, request
from flask import render_template
from datetime import time
# from flask_cors import CORS

from flask import abort, Flask, jsonify, request

from nltk.tokenize import wordpunct_tokenize



from flair.data import Sentence, Token
from flair.models import SequenceTagger

app = Flask(__name__)

# sequence_model = SequenceTagger.load('/mnt/droplet/nfs/gns/literature/Santosh_Tirunagari/GitHub/flair_models/ner/multi_bio_ner_model/EBI/best-model.pt')
flair_model = flair_model = SequenceTagger.load('/nfs/gns/literature/Santosh_Tirunagari/GitHub/flair_models/ner/multi_bio_ner_model/EBI/best-model.pt')




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

    print(sentence.to_dict(tag_type='ner'))

    try:
        data_dict['tagged'] = sentence.to_dict(tag_type='ner')
        data_dict['status'] = 200
    except:
        data_dict['status'] = 400

    if data_dict['status'] != 200:
        data_dict['status'] = 400
        return jsonify(data_dict)
    else:
        return jsonify(data_dict)



# Runs the flask server on the specified port (5200)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5200, debug=True)
