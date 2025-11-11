from flask import Flask, render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@localhost:5432/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@host.docker.internal:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Learner(db.Model):
    __tablename__ = 'learner'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[String] = mapped_column(String(100),nullable=False)
    age: Mapped[int] = mapped_column(Integer,nullable=False)

    def __repr__(self):
        return f'Learner(name={self.name}, age={self.age})'


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        learner_name = request.form.get('name')
        learner_age = request.form.get('age')

        if not learner_name or not learner_age:
            flash('Bothe Name and Age are required')
            return redirect(url_for('index'))

        try:
            new_learner = Learner(name=learner_name, age=int(learner_age))
            db.session.add(new_learner)
            db.session.commit()

            flash(f'Learner {new_learner.name}  with age {new_learner.age}created!')
            return redirect(url_for('index'))

        except ValueError as e:
            db.session.rollback()
            flash(f'value Error the input not in correct format: {e}')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}')

    learners = Learner.query.all()

    return render_template('index.html',learners=learners)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000,debug=True)