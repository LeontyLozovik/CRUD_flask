from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    # __tablename__ = user #В обычной SQLAlchemy нужно обязательно
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    quizzes = db.relationship('Quiz', backref='user')

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name: str, user: User) -> None:
        super().__init__()
        self.name = name
        self.user = user

    def __repr__(self) -> str:
        return f'id - {self.id}, name - {self.name}'


quiz_question = db.Table('quiz_question',
            db.Column('quiz_id', db.Integer, db.ForeignKey('quiz.id')),
            db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
            )


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    wrong1 = db.Column(db.String(100), nullable=False)
    wrong2 = db.Column(db.String(100), nullable=False)
    wrong3 = db.Column(db.String(100), nullable=False)
    quizzes = db.relationship('Quiz', secondary=quiz_question, backref='question')

    def __init__(self, question: str, answer: str, wrong1: str, wrong2: str, wrong3: str) -> None:
        super().__init__()
        self.question = question
        self.answer = answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

    def __repr__(self):
        return f'{self.question}'


def db_add_new_data():
    db.drop_all()
    db.create_all()

    leo = User(name='Leontiy')
    dasha = User(name='Daria')

    quizzes = [
        Quiz('Мозгобойня', leo),
        Quiz('Туц-Туц', leo),
        Quiz('Сам Шазам', dasha),
        Quiz('WoW', dasha),
    ]

    questions = [
        Question('Какой год был провозглашен годом начала Великой Французской революции?', '1789', '1799', '1801', '1776'),
        Question('Какое самое высокое животное на Земле?', 'Жираф', 'Слон', 'Носорог', 'Гиппопотам'),
        Question('Кто написал "Войну и мир"?', 'Лев Толстой', 'Федор Достоевский', 'Иван Тургенев', 'Антон Чехов'),
        Question('Какое самое большое озеро в мире?', 'Каспийское море', 'Верхнее озеро', 'Байкал', 'Мичиган'),
        Question('Какая столица Австралии?', 'Канберра', 'Сидней', 'Мельбурн', 'Брисбен'),
        Question('Какая страна является самой многонациональной в мире?', 'Индия', 'США', 'Россия', 'Китай')
    ]

    quizzes[0].question.append(questions[0])
    quizzes[0].question.append(questions[3])
    quizzes[0].question.append(questions[2])
    quizzes[0].question.append(questions[4])

    quizzes[1].question.append(questions[4])
    quizzes[1].question.append(questions[2])
    quizzes[1].question.append(questions[5])
    quizzes[1].question.append(questions[0])

    quizzes[2].question.append(questions[1])
    quizzes[2].question.append(questions[3])
    quizzes[2].question.append(questions[5])
    quizzes[2].question.append(questions[2])

    quizzes[2].question.append(questions[0])
    quizzes[2].question.append(questions[1])
    quizzes[2].question.append(questions[2])
    quizzes[2].question.append(questions[4])

    db.session.add_all(quizzes)
    db.session.commit()
