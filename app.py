from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/attendee'

db = SQLAlchemy(app)


class Attendee(db.Model):
    __tablename__ = 'attendees'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(40))
    email = db.Column(db.String(40))

    def __init__(self, fname, email):
        self.fname = fname
        self.email = email


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/register")
def register():
    return render_template('register.html')


emailList = db.session.query(Attendee.email)


@app.route("/submit", methods=['POST'])
def submit():
    fname = request.form['fname']
    email = request.form['email']

    for emails in emailList:
        ee = emails.email
        if email == ee:
            return render_template('failure.html')

        else:
            attendee = Attendee(fname, email)
            db.session.add(attendee)
            db.session.commit()

            studentResult = db.session.query(Attendee.fname)

            for result in studentResult:
                return render_template('success.html', data=fname)


Result = db.session.query(Attendee.fname)


@app.route("/attendee")
def get():
    return render_template('attendee.html', data=Result)


if __name__ == "__main__":
    app.run(debug=True)
