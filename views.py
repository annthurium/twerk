from flask import Flask, render_template, redirect, request, url_for
import stripper
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

#def something():
	#pass
	#user_1 = 'annthurium'
	#user_2 = 'queerviolet'
	# timeline_1 = stripper.consume_timeline(user_1)
	# timeline_2 = stripper.consume_timeline(user_2)
	# replies = stripper.find_replies(timeline_1, user_2)
	# moar_replies = stripper.find_replies(timeline_2, user_1)
	# return render_template("list_tweets.html", at_replies = replies)

if __name__== "__main__":
	app.run(debug = True)