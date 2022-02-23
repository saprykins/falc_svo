"""
VM preparation:
mkdir flask
mkdir venv
mkdir application
python3 -m venv ./venv
# if needed sudo apt install python3.8-venv
# for Windows: source ./Script/activate
# for Ubuntu: source my-project-env/bin/activate
python application.py
you can check if site is available here
http://138.195.138.220:5000/
to put the website running without my connection via ssh
I run the command ~ python3 application.py
ctr+z
bg
now, to list background commands use "jobs"
"""


"""
possible improvement steps
port 80
domain name
"""
#
# !python3 -m spacy download fr_core_news_md
#

import fr_core_news_md
import spacy
from flask import Flask

nlp = fr_core_news_md.load()

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>!!! FALC is great !!!</h1>"

@app.route("/svo/<text>", methods=["POST"])
def upload_file(text):
    
    # go through all words
    # if there're no Named Entities -> find key words
    # there's a pb in case we have France in texte: it's entity,

    doc = nlp(text)
    
    line_all = ''

    if len(doc.ents) == 0:
        for token in doc:
            if token.dep_ == "nsubj":
                line_all += token.lemma_ + ' '
            if token.dep_ == "obj":
                line_all += token.lemma_ + ' '
            if token.dep_ == "conj":
                line_all += token.lemma_ + ' '
            if token.dep_ == "advmode":
                line_all += token.lemma_ + ' '
            if token.dep_ == "ROOT":
                line_all += token.lemma_ + ' '
            if token.dep_ == "cop":
                line_all += token.lemma_ + ' '
            if token.dep_ == "amod":
                line_all += token.lemma_ + ' '
            if token.dep_ == "obl":
                line_all += token.lemma_ + ' '

    # if there's at least one named entity
    else:
        for token in doc:
            # if the word is subj
            if token.dep_ == "nsubj":
                # check if it is a part of entities
                for i in range(len(doc.ents)):
                    important_part = token
                    if important_part.text in str(doc.ents[i]):
                        # print(important_part.text)
                        line_all += doc.ents[i] + ' '
                        # leave the cycle (United gives one, Kingdome gives two)
                        break
                    else: 
                        line_all += token.text + ' '
                        break

            elif token.dep_ == "obj":
                for i in range(len(doc.ents)):
                    important_part = token
                    if important_part.text in str(doc.ents[i]):
                        # print(important_part.text)
                        line_all += doc.ents[i] + ' '
                        break
                    else: 
                        line_all += token.text + ' '
                        break

            elif token.dep_ == "conj":
                for i in range(len(doc.ents)):
                    important_part = token
                    if important_part.text in str(doc.ents[i]):
                        # print(important_part.text)
                        line_all += doc.ents[i] + ' '
                        break
                    else: 
                        line_all += token.text + ' '
                        break

            elif token.dep_ == "advmod" or token.dep_ == "ROOT" or token.dep_ == "amod" or token.dep_ == "obl":
                line_all += token.lemma_ + ' '
            
        return line_all

    
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
