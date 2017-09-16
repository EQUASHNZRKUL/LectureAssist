from flask import Flask, jsonify, request
import json


app = Flask(__name__)


#TODO: Grab text from image
#TODO: Grab keywords
SIMILARITY_INDEX = 0.5

'''
Takes a list of keywords and
returns the similarity
'''

def similiarity(keywords1, keywords2):
    counter = 0
    for word in keywords1:
        if word in keywords2:
            counter += 2
    return 1.0*counter/(len(keywords1) + len(keywords2))


'''
Takes a string of text that represents a question and store it
also compare the string to all existing strings
'''


@app.rout('/getText', methods=['POST', 'GET'])
def getText():
    # compare text to all strings
    # questions.json stores all the questions
    # key is the question and value is the list of keywords
    if request.method == 'POST':
        question = json.dumps(request.json['question'])
        # EXTRACT KEYWORDS FROM question
        keywords = []
        with open('questions.json') as f:
            quest = json.loads(f)

        for questionToCompare in quest:
            s = similiarity(keywords, quest[questionToCompare])
            if s > SIMILARITY_INDEX:
                # we need to return a positive count
                return {"count": 1}
        # at this point the question is new
        quest[question] = keywords
        with open('questions.json', 'w') as f:
            json.dump(quest, f)
        return {"count": 0}

'''
    Takes question's count and age and gives a score. 
'''
def getPriority(upCount, age):
    

'''
    Takes encoded_string of pptx slide image and stores keywords into a json.
'''
def get_image_mssg(encoded_string):
  img_request = {}
  rtype = {}
  img_request["image"] = {"content" : encoded_string}
  img_request["features"] = []
  img_request["features"].append({"type": "TEXT_DETECTION"})

  payload = {}
  payload["requests"] = []
  payload["requests"].append(img_request)

  request_string = 'https://vision.googleapis.com/v1/images:annotate?key=' + AIzaSyBxdgB4Hf7E504gHXbKVEVt6-FnZEXBpzM
  r = requests.post(request_string, data=json.dumps(payload))
  res = json.loads(r.text)

  return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
