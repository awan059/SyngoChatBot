from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
 
app = Flask(__name__)
 
english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter",
            response_selection_method=get_random_response,
            logic_adapters = [
                 {
                     'import_path': 'chatterbot.logic.BestMatch',
                     'default_response': 'I am sorry, I did not understand. I am still learning. \
                     Please contact awanish.singh@siemens-healthineers.com for further assistance.',
                     'maximum_similarity_threshold': 0.80
                 }
             ],
             read_only = True,
             preprocessors=['chatterbot.preprocessors.clean_whitespace',
            'chatterbot.preprocessors.unescape_html',
            'chatterbot.preprocessors.convert_to_ascii'])


trainer = ChatterBotCorpusTrainer(english_bot)

trainer.train("chatterbot.corpus.english",
                "chatterbot.corpus.english.greetings",
                "chatterbot.corpus.english.conversations")

trainer.train(
    ".\\data\\conversations.yml",
    ".\\data\\jokes.yml",
    ".\\data\\plaza\\Plaza_initial_enquiry.yml",
    ".\\data\\plaza\\plaza_precheck.yml"
)
 
@app.route("/")
def home():
    return render_template("index.html")
 
@app.route("/get")#, methods = ["GET", "POST"])
def get_bot_response():
    #print("Getting user input")
    userText = request.args.get('msg')
    #print(userText)
    a = english_bot.get_response(userText)
    #print(a)
    return str(a)


if __name__ == "__main__":
    app.run()