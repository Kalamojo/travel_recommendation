from flask import Flask, request, jsonify, render_template
import cohere
import math
from heapq import nsmallest

test = Flask(__name__)

#@test.before_first_request
#def do_something_only_onnce():
co = cohere.Client('0Qp52FnTMwc3dhwWafuGWw8yOqdyy1bKK0usvqxD')
options = ["When are you open?", "When do you close?", "What are the hours?", "Are you open on weekends?", "Are you available on holidays?", "How much is a burger?", "What\'s the price of a meal?", "How much for a few burgers?", "Do you have a vegan option?", "Do you have vegetarian?", "Do you serve non-meat alternatives?", "Do you have milkshakes?", "Milkshake", "Do you have desert?", "Can I bring my child?", "Are you kid friendly?", "Do you have booster seats?", "Do you do delivery?", "Is there takeout?", "Do you deliver?", "Can I have it delivered?", "Can you bring it to me?", "Do you have space for a party?", "Can you accommodate large groups?", "Can I book a party here?"]
response = co.embed(
    model='large',
    texts=options)
    
def co_sim(arr1, arr2, size):
    tempT = 0
    for i in range(size):
        tempT += (arr1[i] - arr2[i])**2
    return math.sqrt(tempT)

@test.route('/', methods=['GET']) #this is going to be the default site path
def home():
	return render_template("index.html")

@test.errorhandler(404) #this if they use some link that doesn't exist
def page_not_found(e):
	return "<h1>404</h1><p>The resource could not be found.</p>", 404

@test.route('/api', methods=['GET'])
def actualStuff():
    query_parameters = request.args
    search = query_parameters.get('search')
    print(search)
    emb = co.embed(model='large', texts=[search]).embeddings[0]
    cosine_sim = {}
    for i in range(len(options)):
        phrase = response.embeddings[i]
        cosine_sim[co_sim(emb, phrase, 4096)] = options[i]
	# call the function on the search and then return results
    return jsonify(nsmallest(5, cosine_sim.items()))

if __name__ == "__main__":
	test.run(debug=True)