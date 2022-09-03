from flask import Flask, request, jsonify, render_template

test = Flask(__name__)

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
	# call the function on the search and then return results
	return jsonify("""our results""")

if __name__ == "__main__":
	test.run(debug=True)