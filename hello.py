import json
import os

from flask import Flask
from flask import request
from flask import make_response
import numpy as np

@app.route('/')
def hello_world():
    return 'Hello my chatbot!'

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):

    print("     ")
    # Parsing the POST request body into a dictionary for easy access.
    req_dict = json.loads(request.data)
    print(req_dict)
    print("     ")
    print("     ")
    
    # Accessing the fields on the POST request boduy of API.ai invocation of the webhook
    intent = req_dict["queryResult"]["intent"]["displayName"]
    #print(intent)
    
    #Return to format dictionnary 
    #req_dict["queryResult"]["outputContexts"][0]
    #{'name': 'projects/newagent-liaq/agent/sessions/9f25365d-13d0-33b3-bfac-2921ab672199/contexts/register-followup', 'parameters': {'person': {'name': 'คมสัน'}, 'person.original': 'นายคมสัน', 'number-integer': 1134456.0, 'number-integer.original': '1134456', 'department': 'คอมพิวเตอร์', 'department.original': 'คอมพิวเตอร์', 'any': 'ใช่', 'any.original': 'ใช่'}}

    outputContexts = req_dict["queryResult"]["outputContexts"][0]['parameters']

    print(outputContexts)

    print(outputContexts['person.original'])

    if intent == 'register - yes':
        speech = "ได้เเลยครับ คุณ!" + outputContexts['person']['name']
    else:
        speech = "ผมไม่เข้าใจ คุณต้องการอะไร"

    res = makeWebhookResult(speech)

    return res

def makeWebhookResult(speech):
    return {
  "fulfillmentText": speech
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
    
    
