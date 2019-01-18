import urllib.request
import urllib.response
import sys
import os, glob
import tika
from tika import parser
import http.client, urllib
import json
import re
tika.initVM()

def parsePDF(path):
    documents = { 'documents': []}
    count = 1
    for file in glob.glob(path):
        parsedPDF = parser.from_file(file)
        text = parsedPDF["content"]
        text = text.strip('\n')
        text = text.encode('ascii','ignore').decode('ascii')
        documents.setdefault('documents').append({"language":"en","id":str(count),"text":text})
        count+= 1
    return documents 
    
# Replace the accessKey string value with your valid access key.
accessKey = '0bf7acdf299a4d0e8fec402213b6847c'
url = 'westeurope.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/Sentiment'
 
def TextAnalytics(documents):
    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = http.client.HTTPSConnection(url)
    body = json.dumps (documents)
    conn.request ("POST", path, body, headers)
    response = conn.getresponse ()
    return response.read ()


docs = parsePDF("*.pdf")
print(docs)
print()
print ('Please wait a moment for the results to appear.\n')
result = TextAnalytics (docs)
print (json.dumps(json.loads(result), indent=4))