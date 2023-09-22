from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)


class Mtw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(200), nullable=False, default='Unwatched...')

    def __repr__(self):
        return '<movie %r>' % self.id


db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        movie_mname = request.form['content']
        new_movie = Mtw(mname=movie_mname)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'There was an issue adding your movie'

    else:
        movies = Mtw.query.order_by(Mtw.date_created).all()
        return render_template('index.html', movies=movies)


@app.route('/delete/<int:id>')
def delete(id):
    movie_to_delete = Mtw.query.get_or_404(id)

    try:
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception:
        return 'There was a problem deleting that movie'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    movie = Mtw.query.get_or_404(id)

    if request.method != 'POST':
        return render_template('update.html', movie=movie)
    movie.mname = request.form['mname']

    try:
        db.session.commit()
        return redirect('/')
    except Exception:
        return 'There was an issue updating your movie'


@app.route('/watched/<int:id>')
def maw(id):
    movie_seen = Mtw.query.get_or_404(id)

    try:
        movie_seen.status = 'Watched!'
        db.session.commit()
        return redirect('/')
    except Exception:
        return 'There was a problem marking that movie as watched'


@app.route('/unwatched/<int:id>')
def mau(id):
    movie_seen = Mtw.query.get_or_404(id)

    try:
        movie_seen.status = 'Unwatched...'
        db.session.commit()
        return redirect('/')
    except Exception:
        return 'There was a problem marking that movie as unwatched'


if __name__ == "__main__":
    app.run(debug=True)
