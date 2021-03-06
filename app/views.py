"""
routes file for handling get/post request for crowdscholar
Author: Harry Rybacki
Date: 5June13
"""

import json

import raw_db
import articles_db
import articles_endpoint_validator

from flask import render_template, request, Response
from app import app
from json_controller import JSONController

# connect to the database
articles_db = articles_db.DB(host="localhost", port=27017)
raw_db = raw_db.DB(host="localhost", port=27018)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/citebin', methods=['GET', 'POST'])
def Citebin():
    """drop box for users to donate of raw or specific data for citations to
    our DB"""
    # if post -- convert and store citation
    if request.method == 'POST':
        # convert post data to citation
        citation = json.loads(request.data)
        # @todo fix this to meet new db parse/insert procedures
        #article_id = db.articles.insert(citation)
        return ""

    return render_template("citebin.html")

"""begin API handlers
"""


@app.route('/articles', methods=['GET', 'POST'])
def ArticleEndpoint():
    """
    RESTFull API endpoint for retrieving / submitting articles
    @TODO: Switch function to pluggable view approach
    """

    if request.method == 'GET':
        # load articles endpoint informational page
        return render_template("articles.html")

    elif request.method == 'POST':
        if request.headers['content-type'] == 'application/json':
            # if post's content-type is JSON
            try:
                # try to convert post data
                user_submission = json.loads(request.data)
            except ValunteError:
                # return error if fail
                return Response(status=405)

            # validate data or return error
            if not articles_endpoint_validator.validate(user_submission):
                return Response(status=405)

            # add meta-data to user submission -- headers and what not
            # @todo user submission is a string at this point. Need to make it a string.
            # @todo find proper way to append request.headers to the json
            # user_submission['headers'] = request.headers

            # add parsed data to DB
            #submission_id = articles_db.add(user_submission)

            # return URI of new resource to submitter
            #@todo: format return body with objectid?
            return Response(status=201)

        else:
            # return HTTP submission error code to user
            return Response(status=405)

    else:
        # return HTTP submission error code to user
        return Response(status=405)


@app.route('/raw', methods=['GET', 'POST'])
def RawEndpoint():
    """
    RESTFull API endpoint for submitting raw article data.
    @TODO: Switch function to pluggable view approach
    """
    if request.method == 'GET':
        # load raw endpoint informational page
        return render_template("raw.html")

    elif request.method == 'POST':
        if request.headers['content-type'] == 'application/json':
        # if post's content-type is JSON
            try:
                # ensure it is a valid JSON
                user_submission = json.loads(request.data)
            except ValueError:
                # return error if not a valid JSON
                return Response(status=405)

            # hand user submission ot the controller and return Response
            controller_response = JSONController(user_submission, db=raw_db).submit()
            print "All done, status code: " + str(controller_response.status_code)
            return controller_response

        # user submitted a content-type no currently supported
        else:
            print "not a json"
            return Response(status=400)

    # user tried to call an unsupported HTTP method
    else:
        return Response(status=405)