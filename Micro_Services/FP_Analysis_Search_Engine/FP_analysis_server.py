__author__ = 'Santosh Tirunagari'

from flask import Flask, jsonify, request, render_template
import solrlib


# app config and init
app = Flask(__name__)
app.secret_key = '20meerkats20'
#app.config['CORS_HEADERS'] = 'Content-Type'

# Test endpoint to check if server is running
@app.route("/hello", methods=['GET'])
def hello():

    return jsonify({
        'message': 'Hi',
        "status": 200,
        "service": 'hello'
    })

###################### Frequency #################################################################
# REST endpoint that gets assessors that have been matched with the specfied application key.
@app.route("/get_all_otar_gp_frequencies", methods=['GET'])
def get_all_otar_gp_frequencies():

    data_dict = {}


    # extract max docs GET parameter if present
    maxdocs = request.args.get('maxdocs')

    if maxdocs:

        try:
            maxdocs = int(maxdocs)
        except ValueError:

            return jsonify({
                'error': 'maxdocs must be an integer',
                "status": 400,
                "service": 'get_all_otar_gp_frequencies (maxdocs)'
            })
    else:
        maxdocs = 32000


    # extract max docs GET parameter if present
    page = request.args.get('page')

    if page:

        try:
            page = int(page)
        except ValueError:

            return jsonify({
                'error': 'page must be an integer',
                "status": 400,
                "service": 'get_all_otar_gp_frequencies'
            })
    else:
        page = 0

    # call solr query service
    try:
        data_dict['annot_data'] = solrlib.get_all_otar_gp_frequencies(max_docs_per_page=maxdocs, page= page)
        for each_match in data_dict['annot_data']['matches']:
            each_match['Entity'] = "<a href = get_otar_gp_annotation_data?otar_GP_entity=" + each_match['Entity'] + " target=”_blank”>" + each_match['Entity'] + "</a>"


    except Exception as ex:

        return jsonify({
            'error': str(ex),
            "status": 500,
            "service": 'get_all_otar_gp_frequencies'
        })

    data_dict['status'] = 200
    data_dict['service'] = 'get_all_otar_gp_frequencies'

    # return jsonify(data_dict)
    columns = [
        {
            "field": "Entity",  # which is the field's name of data key
            "title": "GP",  # display as the table header's name
            "width": 100,
            "sortable": True,
        },
        {
            "field": "Freq_of_ML_removed",
            "title": "Freq_of_ML_removed",
            "width": 100,
            "sortable": True,
        },
        {
            "field": "EPMC_total_Freq",
            "title": "EPMC_total_Freq NER",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        },
        {
            "field": "Percentage_removed",
            "title": "Percentage_removed EPMC NER",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        }
    ]

    return render_template("table.html",
                           data=data_dict['annot_data']['matches'],
                           columns=columns,
                           title='PCSE GP False Positive Analysis')



###################### Frequency #################################################################
# REST endpoint that gets assessors that have been matched with the specfied application key.
@app.route("/get_all_otar_ds_frequencies", methods=['GET'])
def get_all_otar_ds_frequencies():

    data_dict = {}


    # extract max docs GET parameter if present
    maxdocs = request.args.get('maxdocs')

    if maxdocs:

        try:
            maxdocs = int(maxdocs)
        except ValueError:

            return jsonify({
                'error': 'maxdocs must be an integer',
                "status": 400,
                "service": 'get_all_otar_ds_frequencies (maxdocs)'
            })
    else:
        maxdocs = 32000


    # extract max docs GET parameter if present
    page = request.args.get('page')

    if page:

        try:
            page = int(page)
        except ValueError:

            return jsonify({
                'error': 'page must be an integer',
                "status": 400,
                "service": 'get_all_otar_ds_frequencies'
            })
    else:
        page = 0

    # call solr query service
    try:
        data_dict['annot_data'] = solrlib.get_all_otar_ds_frequencies(max_docs_per_page=maxdocs, page= page)
        for each_match in data_dict['annot_data']['matches']:
            each_match['Entity'] = "<a href = get_otar_ds_annotation_data?otar_DS_entity=" + each_match['Entity'] + " target=”_blank”>" + each_match['Entity'] + "</a>"


    except Exception as ex:

        return jsonify({
            'error': str(ex),
            "status": 500,
            "service": 'get_all_otar_ds_frequencies'
        })

    data_dict['status'] = 200
    data_dict['service'] = 'get_all_otar_ds_frequencies'

    # return jsonify(data_dict)
    columns = [
        {
            "field": "Entity",  # which is the field's name of data key
            "title": "DS",  # display as the table header's name
            "width": 100,
            "sortable": True,
        },
        {
            "field": "Freq_of_ML_removed",
            "title": "Freq_of_ML_removed",
            "width": 100,
            "sortable": True,
        },
        {
            "field": "EPMC_total_Freq",
            "title": "EPMC_total_Freq NER",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        },
        {
            "field": "Percentage_removed",
            "title": "Percentage_removed EPMC NER",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        }
    ]

    return render_template("table.html",
                           data=data_dict['annot_data']['matches'],
                           columns=columns,
                           title='PCSE False Positive Analysis')



# REST endpoint that gets assessors that have been matched with the specfied application key.
@app.route("/get_all_epmc_gp_frequencies", methods=['GET'])
def get_all_epmc_gp_frequencies():

    data_dict = {}


    # extract max docs GET parameter if present
    maxdocs = request.args.get('maxdocs')

    if maxdocs:

        try:
            maxdocs = int(maxdocs)
        except ValueError:

            return jsonify({
                'error': 'maxdocs must be an integer',
                "status": 400,
                "service": 'get_all_epmc_gp_frequencies (maxdocs)'
            })
    else:
        maxdocs = 32000


    # extract max docs GET parameter if present
    page = request.args.get('page')

    if page:

        try:
            page = int(page)
        except ValueError:

            return jsonify({
                'error': 'page must be an integer',
                "status": 400,
                "service": 'get_all_epmc_gp_frequencies'
            })
    else:
        page = 0

    # call solr query service
    try:
        data_dict['annot_data'] = solrlib.get_all_epmc_gp_frequencies(max_docs_per_page=maxdocs, page= page)
        for each_match in data_dict['annot_data']['matches']:
            each_match['Entity'] = "<a href = get_gp_annotation_data?epmc_GP_entity=" + each_match['Entity'] + " target=”_blank”>" + each_match['Entity'] + "</a>"


    except Exception as ex:

        return jsonify({
            'error': str(ex),
            "status": 500,
            "service": 'get_all_epmc_gp_frequencies'
        })

    data_dict['status'] = 200
    data_dict['service'] = 'get_all_epmc_gp_frequencies'

    # return jsonify(data_dict)
    columns = [
        {
            "field": "Entity",  # which is the field's name of data key
            "title": "GP",  # display as the table header's name
            "width": 100,
            "sortable": True,
        },
        {
            "field": "Freq_of_ML_removed",
            "title": "Freq_of_ML_removed",
            "width": 100,
            "sortable": True,
        },
        {
            "field": "EPMC_total_Freq",
            "title": "EPMC_total_Freq NER",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        },
        {
            "field": "Percentage_removed",
            "title": "Percentage_removed EPMC NER",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        }
    ]

    return render_template("table.html",
                           data=data_dict['annot_data']['matches'],
                           columns=columns,
                           title='PCSE GP False Positive Analysis')


# REST endpoint that gets assessors that have been matched with the specfied application key.
@app.route("/get_all_epmc_ds_frequencies", methods=['GET'])
def get_all_epmc_ds_frequencies():

    data_dict = {}


    # extract max docs GET parameter if present
    maxdocs = request.args.get('maxdocs')

    if maxdocs:

        try:
            maxdocs = int(maxdocs)
        except ValueError:

            return jsonify({
                'error': 'maxdocs must be an integer',
                "status": 400,
                "service": 'get_all_epmc_ds_frequencies (maxdocs)'
            })
    else:
        maxdocs = 32000


    # extract max docs GET parameter if present
    page = request.args.get('page')

    if page:

        try:
            page = int(page)
        except ValueError:

            return jsonify({
                'error': 'page must be an integer',
                "status": 400,
                "service": 'get_all_epmc_ds_frequencies'
            })
    else:
        page = 0

    # call solr query service
    try:
        data_dict['annot_data'] = solrlib.get_all_epmc_ds_frequencies(max_docs_per_page=maxdocs, page= page)
        for each_match in data_dict['annot_data']['matches']:
            each_match['Entity'] = "<a href = get_ds_annotation_data?epmc_GP_entity=" + each_match['Entity'] + " target=”_blank”>" + each_match['Entity'] + "</a>"


    except Exception as ex:

        return jsonify({
            'error': str(ex),
            "status": 500,
            "service": 'get_all_epmc_ds_frequencies'
        })

    data_dict['status'] = 200
    data_dict['service'] = 'get_all_epmc_ds_frequencies'

    # return jsonify(data_dict)
    columns = [
        {
            "field": "Entity",  # which is the field's name of data key
            "title": "DS",  # display as the table header's name
            "width": 100,
            "sortable": True,
        },
        {
            "field": "Freq_of_ML_removed",
            "title": "Freq_of_ML_removed",
            "width": 100,
            "sortable": True,
        },
        {
            "field": "EPMC_total_Freq",
            "title": "EPMC_total_Freq NER",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        },
        {
            "field": "Percentage_removed",
            "title": "Percentage_removed EPMC NER",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        }
    ]

    return render_template("table.html",
                           data=data_dict['annot_data']['matches'],
                           columns=columns,
                           title='PCSE GP False Positive Analysis')
######################### Annotation Data ###################################################################
@app.route("/get_gp_annotation_data", methods=['GET'])
def get_annotation_data_by_epmc_gp():

    data_dict = {}
    appkey = request.args.get('epmc_GP_entity')

    if not appkey:

        return jsonify({
            'error': 'No epmc_ner_entity supplied',
            "status": 400,
            "service": 'get_annotation_data_by_epmc_ner (appkey)'
        })

    # extract max docs GET parameter if present
    maxdocs = request.args.get('maxdocs')

    if maxdocs:

        try:
            maxdocs = int(maxdocs)
        except ValueError:

            return jsonify({
                'error': 'maxdocs must be an integer',
                "status": 400,
                "service": 'get_annotation_data_by_epmc_ner (maxdocs)'
            })
    else:
        maxdocs = 5000


    # extract max docs GET parameter if present
    page = request.args.get('page')

    if page:

        try:
            page = int(page)
        except ValueError:

            return jsonify({
                'error': 'page must be an integer',
                "status": 400,
                "service": 'get_annotation_data_by_epmc_ner (page)'
            })
    else:
        page = 0

    # call solr query service
    try:
        data_dict['annot_data'] = solrlib.get_GP_annotation_data(epmc_GP_entity=appkey, max_docs_per_page=maxdocs, page= page)

        for each_match in data_dict['annot_data']['matches']:
            each_match['sentence'] = solrlib.term_highlighter(each_match['sentence'], each_match['eurpmc_ner'])


    except Exception as ex:

        return jsonify({
            'error': str(ex),
            "status": 500,
            "service": 'get_annotation_data_by_epmc_ner'
        })

    data_dict['status'] = 200
    data_dict['service'] = 'get_annotation_data_by_epmc_ner'


    # return jsonify(data_dict)
    columns = [
        {
            "field": "pmc_id",  # which is the field's name of data key
            "title": "PMCID",  # display as the table header's name
            "width": 100,
            "sortable": True,
        },
        {
            "field": "section",
            "title": "Section",
            "width": 100,
            "sortable": True,
        },
        {
            "field": "sentence",
            "title": "Sentence",
            "width": 600,
            "sortable": True,
        },
        {
            "field": "eurpmc_ner",
            "title": "EuropePMC NER",
            "width": 100,
            'widthUnit':'px',
            "sortable": True,
        },
        {
            "field": "ml_ner",
            "title": "PCSE NER",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        }
    ]

    return render_template("table.html",
      data=data_dict['annot_data']['matches'],
      columns=columns,
      title='PCSE GP False Positive Analysis')





@app.route("/get_ds_annotation_data", methods=['GET'])
def get_annotation_data_by_epmc_ds():

    data_dict = {}
    appkey = request.args.get('epmc_DS_entity')

    if not appkey:

        return jsonify({
            'error': 'No epmc_ner_entity supplied',
            "status": 400,
            "service": 'get_annotation_data_by_epmc_ner (appkey)'
        })

    # extract max docs GET parameter if present
    maxdocs = request.args.get('maxdocs')

    if maxdocs:

        try:
            maxdocs = int(maxdocs)
        except ValueError:

            return jsonify({
                'error': 'maxdocs must be an integer',
                "status": 400,
                "service": 'get_annotation_data_by_epmc_ner (maxdocs)'
            })
    else:
        maxdocs = 5000


    # extract max docs GET parameter if present
    page = request.args.get('page')

    if page:

        try:
            page = int(page)
        except ValueError:

            return jsonify({
                'error': 'page must be an integer',
                "status": 400,
                "service": 'get_annotation_data_by_epmc_ner (page)'
            })
    else:
        page = 0

    # call solr query service
    try:
        data_dict['annot_data'] = solrlib.get_DS_annotation_data(epmc_DS_entity=appkey, max_docs_per_page=maxdocs, page= page)

        for each_match in data_dict['annot_data']['matches']:
            each_match['sentence'] = solrlib.term_highlighter(each_match['sentence'], each_match['eurpmc_ner'])


    except Exception as ex:

        return jsonify({
            'error': str(ex),
            "status": 500,
            "service": 'get_annotation_data_by_epmc_ner'
        })

    data_dict['status'] = 200
    data_dict['service'] = 'get_annotation_data_by_epmc_ner'


    # return jsonify(data_dict)
    columns = [
        {
            "field": "pmc_id",  # which is the field's name of data key
            "title": "PMCID",  # display as the table header's name
            "width": 100,
            "sortable": True,
        },
        {
            "field": "section",
            "title": "Section",
            "width": 100,
            "sortable": True,
        },
        {
            "field": "sentence",
            "title": "Sentence",
            "width": 600,
            "sortable": True,
        },
        {
            "field": "eurpmc_ner",
            "title": "EuropePMC NER",
            "width": 100,
            'widthUnit':'px',
            "sortable": True,
        },
        {
            "field": "ml_ner",
            "title": "PCSE NER",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        }
    ]

    return render_template("table.html",
      data=data_dict['annot_data']['matches'],
      columns=columns,
      title='PCSE DS False Positive Analysis')


########################### OTAR DS ##########################################################################




@app.route("/get_otar_ds_annotation_data", methods=['GET'])
def get_annotation_data_by_otar_ds():

    data_dict = {}
    appkey = request.args.get('otar_DS_entity')

    if not appkey:

        return jsonify({
            'error': 'No otar_ner_entity supplied',
            "status": 400,
            "service": 'get_annotation_data_by_otar_ds_ner (appkey)'
        })

    # extract max docs GET parameter if present
    maxdocs = request.args.get('maxdocs')

    if maxdocs:

        try:
            maxdocs = int(maxdocs)
        except ValueError:

            return jsonify({
                'error': 'maxdocs must be an integer',
                "status": 400,
                "service": 'get_annotation_data_by_otar_ds_ner'
            })
    else:
        maxdocs = 5000


    # extract max docs GET parameter if present
    page = request.args.get('page')

    if page:

        try:
            page = int(page)
        except ValueError:

            return jsonify({
                'error': 'page must be an integer',
                "status": 400,
                "service": 'get_annotation_data_by_otar_ds_ner'
            })
    else:
        page = 0

    # call solr query service
    try:
        data_dict['annot_data'] = solrlib.get_otar_DS_annotation_data(otar_DS_entity=appkey, max_docs_per_page=maxdocs, page= page)

        for each_match in data_dict['annot_data']['matches']:
            each_match['sentence'] = solrlib.term_highlighter(each_match['sentence'], each_match['EP_DS'])
            each_match['pmc_id'] = "<a href = http://europepmc.org/"+each_match['pmc_id']+" target=”_blank”>"+each_match['pmc_id']+"</a>"


    except Exception as ex:

        return jsonify({
            'error': str(ex),
            "status": 500,
            "service": 'get_annotation_data_by_otar_ds_ner'
        })

    data_dict['status'] = 200
    data_dict['service'] = 'get_annotation_data_by_otar_ds_ner'


    # return jsonify(data_dict)
    columns = [
        {
            "field": "pmc_id",  # which is the field's name of data key
            "title": "PMCID",  # display as the table header's name
            "width": 100,
            "sortable": True,
        },
        {
            "field": "section",
            "title": "Section",
            "width": 100,
            "sortable": True,
        },
        {
            "field": "sentence",
            "title": "Sentence",
            "width": 600,
            "sortable": True,
        },
        {
            "field": "EP_GP",
            "title": "EuropePMC GP",
            "width": 100,
            'widthUnit':'px',
            "sortable": True,
        },
        {
            "field": "ML_GP",
            "title": "PCSE GP",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        },
        {
            "field": "EP_DS",
            "title": "EuropePMC DS",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        },
        {
            "field": "ML_DS",
            "title": "PCSE DS",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        }
    ]

    return render_template("table.html",
      data=data_dict['annot_data']['matches'],
      columns=columns,
      title='PCSE OTAR DS False Positive Analysis')


################################ OTAR GP ############################################################


@app.route("/get_otar_gp_annotation_data", methods=['GET'])
def get_annotation_data_by_otar_gp():

    data_dict = {}
    appkey = request.args.get('otar_GP_entity')

    if not appkey:

        return jsonify({
            'error': 'No otar_ner_entity supplied',
            "status": 400,
            "service": 'get_annotation_data_by_otar_ds_ner (appkey)'
        })

    # extract max docs GET parameter if present
    maxdocs = request.args.get('maxdocs')

    if maxdocs:

        try:
            maxdocs = int(maxdocs)
        except ValueError:

            return jsonify({
                'error': 'maxdocs must be an integer',
                "status": 400,
                "service": 'get_annotation_data_by_otar_gp_ner'
            })
    else:
        maxdocs = 5000


    # extract max docs GET parameter if present
    page = request.args.get('page')

    if page:

        try:
            page = int(page)
        except ValueError:

            return jsonify({
                'error': 'page must be an integer',
                "status": 400,
                "service": 'get_annotation_data_by_otar_gp_ner'
            })
    else:
        page = 0

    # call solr query service
    try:
        data_dict['annot_data'] = solrlib.get_otar_GP_annotation_data(otar_GP_entity=appkey, max_docs_per_page=maxdocs, page= page)

        for each_match in data_dict['annot_data']['matches']:
            each_match['sentence'] = solrlib.term_highlighter(each_match['sentence'], each_match['EP_GP'])
            each_match['pmc_id'] = "<a href = http://europepmc.org/"+each_match['pmc_id']+" target=”_blank”>"+each_match['pmc_id']+"</a>"


    except Exception as ex:

        return jsonify({
            'error': str(ex),
            "status": 500,
            "service": 'get_annotation_data_by_otar_gp_ner'
        })

    data_dict['status'] = 200
    data_dict['service'] = 'get_annotation_data_by_otar_gp_ner'


    # return jsonify(data_dict)
    columns = [
        {
            "field": "pmc_id",  # which is the field's name of data key
            "title": "PMCID",  # display as the table header's name
            "width": 100,
            "sortable": True,
        },
        {
            "field": "section",
            "title": "Section",
            "width": 100,
            "sortable": True,
        },
        {
            "field": "sentence",
            "title": "Sentence",
            "width": 600,
            "sortable": True,
        },
        {
            "field": "EP_GP",
            "title": "EuropePMC GP",
            "width": 100,
            'widthUnit':'px',
            "sortable": True,
        },
        {
            "field": "ML_GP",
            "title": "PCSE GP",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        },
        {
            "field": "EP_DS",
            "title": "EuropePMC DS",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        },
        {
            "field": "ML_DS",
            "title": "PCSE DS",
            "width": 100,
            'widthUnit': 'px',
            "sortable": True,
        }
    ]

    return render_template("table.html",
      data=data_dict['annot_data']['matches'],
      columns=columns,
      title='PCSE OTAR GP False Positive Analysis')



@app.route("/", methods=['GET'])
def index():
    return render_template('get_ner.html')


# Runs the flask server on the specified port (5200)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5200, debug=True)