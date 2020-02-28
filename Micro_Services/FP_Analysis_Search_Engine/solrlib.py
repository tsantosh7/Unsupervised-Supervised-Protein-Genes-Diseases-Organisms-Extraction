'''
Library of methods for performing solr queries on the EPMC data.

Santosh Tirunagani

(c) EBI, 2020

Note: a lot of repetition of code here - could do with refactoring


'''

__author__ = 'Santosh Tirunagani'

import requests
import math

_solr_ip_address = 'http://10.7.106.74:8157'

# location of solr standard query handler for application core data
_application_GP_standard_solr_query_url = _solr_ip_address+'/solr/FP_GP_20K/select?'
_application_DS_standard_solr_query_url = _solr_ip_address+'/solr/FP_DS_20K/select?'
_application_otar_standard_solr_query_url = _solr_ip_address+'/solr/FP_OTAR/select?'

### Freqs ###
_application_epmc_freq_standard_solr_query_url = _solr_ip_address+'/solr/EPMC_GP_Freq/select?'
_application_otar_freq_standard_solr_query_url = _solr_ip_address+'/solr/OTAR_GP_Freq/select?'

_application_epmc_DS_freq_standard_solr_query_url = _solr_ip_address+'/solr/EPMC_DS_Freq/select?'
_application_otar_DS_freq_standard_solr_query_url = _solr_ip_address+'/solr/OTAR_DS_Freq/select?'



# Gets EPMC data for a specified entity. (subject to max_docs per page)
# By supplying the page number you can statelessly scroll through all the results.
def get_all_otar_gp_frequencies(max_docs_per_page: int=50, page: int= 0) -> dict:

    # query solr using the standard request endpoint
    r = requests.get(_application_otar_freq_standard_solr_query_url,
                     params={
                         'q': '*:*',
                         'wt': 'json',
                         'rows': max_docs_per_page,
                         'start': page * max_docs_per_page,
                         'fl': '*'
                     })

    # process the solr response
    try:
        rjson = r.json()

    except Exception:
        raise ValueError("Could not parse response from solr. Reason: \n" + r.text)

    if rjson['responseHeader']['status'] != 0:
        raise ValueError('An error response (' + str(rjson['responseHeader']['status'])
                         + ') was received from solr. Likely cause: supplied query invalid.')

    if rjson['response']:

        num_found = rjson['response']['numFound']  # number of applications

        d = rjson['response']['docs']  # d is the docs

        output_dict = {}
        output_dict['numMatches'] = num_found
        output_dict['matches'] = d
        output_dict['maxDocs'] = max_docs_per_page

        return output_dict

    else:
        output_dict = {}
        output_dict['numMatches'] = 0
        output_dict['maxDocs'] = max_docs_per_page

        return output_dict



def get_all_otar_ds_frequencies(max_docs_per_page: int=50, page: int= 0) -> dict:

    # query solr using the standard request endpoint
    r = requests.get(_application_otar_DS_freq_standard_solr_query_url,
                     params={
                         'q': '*:*',
                         'wt': 'json',
                         'rows': max_docs_per_page,
                         'start': page * max_docs_per_page,
                         'fl': '*'
                     })

    # process the solr response
    try:
        rjson = r.json()

    except Exception:
        raise ValueError("Could not parse response from solr. Reason: \n" + r.text)

    if rjson['responseHeader']['status'] != 0:
        raise ValueError('An error response (' + str(rjson['responseHeader']['status'])
                         + ') was received from solr. Likely cause: supplied query invalid.')

    if rjson['response']:

        num_found = rjson['response']['numFound']  # number of applications

        d = rjson['response']['docs']  # d is the docs

        output_dict = {}
        output_dict['numMatches'] = num_found
        output_dict['matches'] = d
        output_dict['maxDocs'] = max_docs_per_page

        return output_dict

    else:
        output_dict = {}
        output_dict['numMatches'] = 0
        output_dict['maxDocs'] = max_docs_per_page

        return output_dict


def get_all_epmc_ds_frequencies(max_docs_per_page: int=50, page: int= 0) -> dict:

    # query solr using the standard request endpoint
    r = requests.get(_application_epmc_DS_freq_standard_solr_query_url,
                     params={
                         'q': '*:*',
                         'wt': 'json',
                         'rows': max_docs_per_page,
                         'start': page * max_docs_per_page,
                         'fl': '*'
                     })

    # process the solr response
    try:
        rjson = r.json()

    except Exception:
        raise ValueError("Could not parse response from solr. Reason: \n" + r.text)

    if rjson['responseHeader']['status'] != 0:
        raise ValueError('An error response (' + str(rjson['responseHeader']['status'])
                         + ') was received from solr. Likely cause: supplied query invalid.')

    if rjson['response']:

        num_found = rjson['response']['numFound']  # number of applications

        d = rjson['response']['docs']  # d is the docs

        output_dict = {}
        output_dict['numMatches'] = num_found
        output_dict['matches'] = d
        output_dict['maxDocs'] = max_docs_per_page

        return output_dict

    else:
        output_dict = {}
        output_dict['numMatches'] = 0
        output_dict['maxDocs'] = max_docs_per_page

        return output_dict




def get_all_epmc_gp_frequencies(max_docs_per_page: int=50, page: int= 0) -> dict:

    # query solr using the standard request endpoint
    r = requests.get(_application_epmc_freq_standard_solr_query_url,
                     params={
                         'q': '*:*',
                         'wt': 'json',
                         'rows': max_docs_per_page,
                         'start': page * max_docs_per_page,
                         'fl': '*'
                     })

    # process the solr response
    try:
        rjson = r.json()

    except Exception:
        raise ValueError("Could not parse response from solr. Reason: \n" + r.text)

    if rjson['responseHeader']['status'] != 0:
        raise ValueError('An error response (' + str(rjson['responseHeader']['status'])
                         + ') was received from solr. Likely cause: supplied query invalid.')

    if rjson['response']:

        num_found = rjson['response']['numFound']  # number of applications

        d = rjson['response']['docs']  # d is the docs

        output_dict = {}
        output_dict['numMatches'] = num_found
        output_dict['matches'] = d
        output_dict['maxDocs'] = max_docs_per_page

        return output_dict

    else:
        output_dict = {}
        output_dict['numMatches'] = 0
        output_dict['maxDocs'] = max_docs_per_page

        return output_dict



from nltk.tokenize import wordpunct_tokenize, WordPunctTokenizer


# Attempt to highlight terms in a piece of text by surrounding them with <em></em> in the response.
def term_highlighter(text: str=None, terms: list=None, kind:str=None) -> str:
    if not text or not terms:
        raise ValueError('Either the supplied text string or list of terms and scores is empty or of type None')

    used_term_strs = set()

    for term_str in terms:

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

        if kind == 'ML':
            text = text.replace(new_term_str, '<span class="badge badge-warning">' + new_term_str + '</span>')
        else:
            text = text.replace(new_term_str, '<span class="badge badge-warning">' + new_term_str + '</span>')

        # also try with 1st letter uppercased and all upper cased

    return text


# Retrieve a dict containing annotation form data for a supplied entity name
def get_GP_annotation_data(epmc_GP_entity: str=None, max_docs_per_page: int=50, page: int= 0) -> dict:


    if not epmc_GP_entity:
        raise ValueError("You must supply an entity")

    solrfield = 'eurpmc_ner'
    # query solr using the standard request endpoint for SBR_application core
    r = requests.get(_application_GP_standard_solr_query_url,
                     params={
                         'q': solrfield + ':' + epmc_GP_entity,
                         'wt': 'json',
                         'rows': max_docs_per_page,
                         'start': page * max_docs_per_page,
                         'fl': '*'
                     })

    # process the solr response
    try:
        rjson = r.json()

    except Exception:
        raise ValueError("Could not parse response from solr. Reason: \n" + r.text)

    if rjson['responseHeader']['status'] != 0:
        raise ValueError('An error response (' + str(rjson['responseHeader']['status'])
                         + ') was received from solr. Likely cause: supplied query invalid.')

    numFound = rjson['response']['numFound']

    if numFound == 0:
        doc = {}
        doc[solrfield] = epmc_GP_entity
        doc['Warning'] = 'Entity not found'

        return doc

    # get the doc
    doc = rjson['response']['docs']

    # # add text snippet
    # doc['snippet'] = doc
    output_dict = {}
    output_dict['numMatches'] = numFound
    output_dict['matches'] = doc

    return output_dict

# Retrieve a dict containing annotation form data for a supplied entity name
def get_DS_annotation_data(epmc_DS_entity: str=None, max_docs_per_page: int=50, page: int= 0) -> dict:


    if not epmc_DS_entity:
        raise ValueError("You must supply an entity")

    solrfield = 'eurpmc_ner'
    # query solr using the standard request endpoint for SBR_application core
    r = requests.get(_application_DS_standard_solr_query_url,
                     params={
                         'q': solrfield + ':' + epmc_DS_entity,
                         'wt': 'json',
                         'rows': max_docs_per_page,
                         'start': page * max_docs_per_page,
                         'fl': '*'
                     })

    # process the solr response
    try:
        rjson = r.json()

    except Exception:
        raise ValueError("Could not parse response from solr. Reason: \n" + r.text)

    if rjson['responseHeader']['status'] != 0:
        raise ValueError('An error response (' + str(rjson['responseHeader']['status'])
                         + ') was received from solr. Likely cause: supplied query invalid.')

    numFound = rjson['response']['numFound']

    if numFound == 0:
        doc = {}
        doc[solrfield] = epmc_DS_entity
        doc['Warning'] = 'Entity not found'

        return doc

    # get the doc
    doc = rjson['response']['docs']

    # # add text snippet
    # doc['snippet'] = doc
    output_dict = {}
    output_dict['numMatches'] = numFound
    output_dict['matches'] = doc

    return output_dict


########################## OTAR DS ###################################

# Retrieve a dict containing annotation form data for a supplied entity name
def get_otar_DS_annotation_data(otar_DS_entity: str=None, max_docs_per_page: int=50, page: int= 0) -> dict:


    if not otar_DS_entity:
        raise ValueError("You must supply an entity")

    solrfield = 'EP_DS'
    # query solr using the standard request endpoint for SBR_application core
    r = requests.get(_application_otar_standard_solr_query_url,
                     params={
                         'q': solrfield + ':' + otar_DS_entity,
                         'wt': 'json',
                         'rows': max_docs_per_page,
                         'start': page * max_docs_per_page,
                         'fl': '*'
                     })

    # process the solr response
    try:
        rjson = r.json()

    except Exception:
        raise ValueError("Could not parse response from solr. Reason: \n" + r.text)

    if rjson['responseHeader']['status'] != 0:
        raise ValueError('An error response (' + str(rjson['responseHeader']['status'])
                         + ') was received from solr. Likely cause: supplied query invalid.')

    numFound = rjson['response']['numFound']

    if numFound == 0:
        doc = {}
        doc[solrfield] = otar_DS_entity
        doc['Warning'] = 'Entity not found'

        return doc

    # get the doc
    doc = rjson['response']['docs']

    output_dict = {}
    output_dict['numMatches'] = numFound
    output_dict['matches'] = doc

    return output_dict

######################## OTAR GP ##########################


# Retrieve a dict containing annotation form data for a supplied entity name
def get_otar_GP_annotation_data(otar_GP_entity: str=None, max_docs_per_page: int=50, page: int= 0) -> dict:


    if not otar_GP_entity:
        raise ValueError("You must supply an entity")

    solrfield = 'EP_GP'
    # query solr using the standard request endpoint for SBR_application core
    r = requests.get(_application_otar_standard_solr_query_url,
                     params={
                         'q': solrfield + ':' + otar_GP_entity,
                         'wt': 'json',
                         'rows': max_docs_per_page,
                         'start': page * max_docs_per_page,
                         'fl': '*'
                     })

    # process the solr response
    try:
        rjson = r.json()

    except Exception:
        raise ValueError("Could not parse response from solr. Reason: \n" + r.text)

    if rjson['responseHeader']['status'] != 0:
        raise ValueError('An error response (' + str(rjson['responseHeader']['status'])
                         + ') was received from solr. Likely cause: supplied query invalid.')

    numFound = rjson['response']['numFound']

    if numFound == 0:
        doc = {}
        doc[solrfield] = otar_GP_entity
        doc['Warning'] = 'Entity not found'

        return doc

    # get the doc
    doc = rjson['response']['docs']

    output_dict = {}
    output_dict['numMatches'] = numFound
    output_dict['matches'] = doc

    return output_dict

if __name__ == '__main__':

    # result = get_all_GP_annotations_data()
    result = get_GP_annotation_data(epmc_ner_entity='FACS', max_docs_per_page=10, page= 0)
    print(result)
