# for app
from flask import Flask, request, redirect, render_template
# for congress.gov api
from cdg_client import CDGClient
import json
import requests
# new
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import datetime
from omnibuster import Omni_Parser
from OmniparseDOM import OmniparseDOM
import xml.dom.minidom

app = Flask(__name__)

directory = 'static/rendered_html/'

# startup site
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

#onevent: upload file
@app.route("/upload", methods = ["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']

        # print(f, file=sys.stderr, flush=True)

        filename = str(f.filename)
        f.save(secure_filename(filename))
        parser = OmniparseDOM(secure_filename(filename))
        parser.start_parse()
        # redirect
        return redirect('/static/rendered_html/HR_Template.html')
    
    
    for file in os.listdir(directory):
        if file.endswith(".html"):
            os.remove(directory + "/" + file)
            continue
        else:
            continue

    return render_template('index.html')

# onevent: submit button
@app.route('/search', methods=['POST'])
def search():

    # collect data from form
    API_KEY = request.form['API_KEY']
    congress = request.form['congress']
    billno = request.form['billno']
    chamber = request.form['billtype']
    #print(chamber)

    # fileID
    fileID = f"{congress}_{chamber}_{billno}"

    # check if this file has already been pulled before searching congress.gov
    
    omniRender = f"static/rendered_html/{fileID}.html"
    '''
    if (os.path.isfile(omniRender)):
        return redirect(omniRender)
    '''

    # api constants
    API_VERSION = "v3"
    ROOT_URL = "https://api.congress.gov/"
    RESPONSE_FORMAT = "xml"

    # create client
    apiClient = CDGClient(API_KEY, response_format="json")
    # this endpoint literally has json dictionaries and arrays mixed in!
    endpoint = f"bill/{congress}/{chamber}/{billno}/text"
    jsonstuff, _ = apiClient.get(endpoint)
    jsonTextVersions = jsonstuff['textVersions']
    # NOTE: changed [1] to [0] to fix senate bill pull - did it need to be [1]?
    jsonFormats = jsonTextVersions[0]['formats']

    xml = ""
    for format in jsonFormats: 
        if format['type'] == "Formatted XML":
            url = format['url']
            xml = requests.get(url, allow_redirects=False)
            break

    # save raw xml in file - technically we could set up the parser to just pass this xml.text
    orig = f"originalXMLs/{fileID}.xml"
    file = open(orig, "w", encoding="utf-8") 
    file.write(xml.text)
    file.close()

    # commence parsing
    parser = OmniparseDOM(orig, omniRender)
    parser.start_parse()
    # redirect to filled in file
    return redirect(omniRender)

# onevent: save button (comment)
@app.route('/comment', methods=['POST'])
def comment():
    rawComm = request.form['rawComm']
    commSrc = request.form['commSrc']
    commDst = request.form['commDst']

    now = datetime.now()
    dateString = "<span class=\"dateComm\">" + now.strftime("%m/%d/%Y") + "@" + now.strftime("%H:%M") + "</span>"
    htmlComm = "<div class=\"savedComm\">" + dateString + rawComm + "</div>\n"
    
    '''
    dom = xml.dom.minidom.parse(commSrc)
    commPane = dom.getElementsByTagName('.commPane')
    commPane[0].text = htmlComm
    '''

    file = open(commDst, "a", encoding="utf-8") 
    file.write(htmlComm)
    file.close()  
    
    return redirect(commSrc)