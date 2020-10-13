#tasks.py
from celery import Celery
app = Celery('tasks', backend='rpc://', broker='pyamqp://capo:capo@ai-capo-api-lb-2.ebi.ac.uk:5672/capo_rabbit_host')

@app.task
def sentence_length(sentence):
    return len(sentence)

#def sentence_name(sentence):
#    return sentence
