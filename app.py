from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
from settings import DATABASE_URL
import os 

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["DATABASE_URL"] = DATABASE_URL

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Meme(db.Model):
    __tablename__ = "memes"
    id = db.Column(db.Integer, primary_key =True)
    text = db.Column(db.String(50))
    image = db.Column(db.String(500))
    favorite = db.Column(db.Boolean)
    
    def __init__(self, text, image, favorite):
        self.text = text
        self.image = image
        self.favorite = favorite
        
class MemeSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "image", "favorite")
        
meme_schema = MemeSchema()
memes_schema = MemeSchema(many=True)

@app.route("/")
def greeting():
    return "<h1>Meme Maker Api</h1>"
#crus post patch/put get delete get all
@app.route('/add-meme', methods=["POST"])
def add_meme():
    text = request.json["text"]
    image = request.json["image"]
    favorite = request.json["favorite"]
    
    new_meme = Meme(text, image, favorite)
    db.session.add(new_meme)
    db.session.commit()
    
    meme = Meme.query.get(new_meme.id)
    return meme_schema.jsonify(meme)

#get all route 
@app.route("/memes", methods=["GET"])
def get_memes():
    all_memes = Meme.query.all()
    result = memes_schema.dump(all_memes)
    
    return jsonify(result)
#show route
@app.route("/meme/<id>", methods=["GET"])
def get_meme(id):
    meme = Meme.query.get(id)
    
    return meme_schema.jsonify(meme)

#put route 
@app.route("/meme/<id>", methods=["PUT"])
def update_meme(id):
    meme = Meme.query.get(id)
    
    new_text = request.json["text"]
    new_favorite = request.json["favorite"]
    
    meme.text = new_text
    meme.favorite = new_favorite
    
    db.session.commit()
    return meme_schema.jsonify(meme)

#delete route 
@app.route("/delete-meme/<id>", methods=["Delete"])
def delete_meme(id):
    meme = Meme.query.get(id)
    
    db.session.delete(meme)
    db.session.commit()
    
    return jsonify({ "message": "Delete Successfully thank you for using my delete route"})

if __name__ == "__main__":
    app.run(debug=True)
