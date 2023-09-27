from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from models import db, Author, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return 'Validations lab'

@app.route('/authors', methods=['GET', 'POST'])
def authors():
    if request.method == 'GET':
        authors = Author.query.all()
        authors_data = [author.__dict__ for author in authors]
        return make_response(jsonify(authors_data), 200)

    if request.method == 'POST':
        data = request.get_json()
        try:
            new_author = Author(
                name=data['name'],
                phone_number=data.get('phone_number')
            )
            db.session.add(new_author)
            db.session.commit()
            return make_response(new_author.__dict__, 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 400)

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        posts = Post.query.all()
        posts_data = [post.__dict__ for post in posts]
        return make_response(jsonify(posts_data), 200)

    if request.method == 'POST':
        data = request.get_json()
        try:
            new_post = Post(
                title=data['title'],
                content=data.get('content'),
                category=data.get('category'),
                summary=data.get('summary')
            )
            db.session.add(new_post)
            db.session.commit()
            return make_response(new_post.__dict__, 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
