## define the urls of each webpage ##

from app import app, db
from app.forms import LoginForm, RegisterForm, ManageQuestionsForm
from app.models import User, Answer, Question, Mark
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

# homepage (set to the root page)
@app.route('/')
def home():
    return render_template('home.html', title="A journey through the tcp/ip model")

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    #don't allow logged in users to access this page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    lForm = LoginForm()

    # if the login details are validated - NOTE WE WILL ALSO ADD JAVASCRIPT VALIDATION FOR RESPONSIVE FEEDBACK
    if lForm.validate_on_submit():
        # try setting user to the associated username's row - if that returns None then try email
        user = User.query.filter_by(username=lForm.username.data).first() or User.query.filter_by(email=lForm.username.data).first()
        # non-existant user or invalid password
        if user is None or not user.check_password(lForm.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=lForm.remember_me.data)
        # handle users clicking on pages that require login
        next_page = request.args.get('next')
        # if there is no specified next page, or the 'next' query points to a page outside this domain
        if not next_page or url_parse(next_page).netloc != '':
            # set the default location to the home page
            next_page = url_for('home')
        return redirect(next_page)

    return render_template('login.html', title="Login", lForm=lForm)

# logout button replaces login if the user is authenticated
@app.route('/logout')
def logout():
    logout_user()
    # if the link is clicked, log the user out then reroute them back to home
    return redirect(url_for('home'))

# register page - this function is very similar to the login function
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    rForm = RegisterForm()

    if rForm.validate_on_submit():
        user = User(
            first_name=rForm.firstname.data,
            last_name=rForm.lastname.data,
            username=rForm.username.data,
            email=rForm.email.data)
        user.set_password(rForm.password.data)
        # add the new user to the database and save the changes
        db.session.add(user)
        db.session.commit()

        # log the user in
        login_user(user, remember=rForm.remember_me.data)
        # we can edit the style of flash messages to help the website interact with users
        flash('Congratulations {}, you are now a registered user!'.format(rForm.firstname.data))
        return redirect(url_for('login'))

    return render_template('register.html', title="Register", rForm=rForm)

# register page - this function is very similar to the login function
@app.route('/register-admin', methods=['GET', 'POST'])
def register_admin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    rForm = RegisterForm()

    if rForm.validate_on_submit():
        user = User(
            first_name=rForm.firstname.data,
            last_name=rForm.lastname.data,
            username=rForm.username.data,
            email=rForm.email.data,
            admin=True)
        user.set_password(rForm.password.data)
        # add the new user to the database and save the changes
        db.session.add(user)
        db.session.commit()
        # we can edit the style of flash messages to help the website interact with users
        flash('Congratulations {}, you are now an admin user!'.format(rForm.firstname.data))
        return redirect(url_for('login'))

    return render_template('register.html', title="Register admin", rForm=rForm)

# all empty pages (yet to be implemented so far)

@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html', title="Progress")


@app.route('/application')
@login_required
def application():
    return render_template('./Content/application.html', title="Application Layer")

@app.route('/application-quiz')
@login_required
def application_link():
    return render_template('quiz.html', title="Application Layer Quiz")

@app.route('/transport')
@login_required
def transport():
    return render_template('./Content/transport.html', title="Transport Layer")

@app.route('/transport-quiz')
@login_required
def transport_quiz():
    return render_template('quiz.html', title="Transport Layer Quiz")


@app.route('/network')
@login_required
def network():
    return render_template('./Content/network.html', title="Network Layer")

@app.route('/network-quiz')
@login_required
def network_quiz():
    return render_template('quiz.html', title="Network Layer Quiz")


@app.route('/link')
@login_required
def link():
    return render_template('./Content/link.html', title="Link Layer")

@app.route('/link-quiz')
@login_required
def link_quiz():
    print('quiz link!')
    return render_template('quiz.html', title="Link Layer Quiz")


@app.route('/retrieve-progress-data')
@login_required
def progress_data():
    user_data = User.query.filter_by(id = current_user.id).first()
    progress = user_data.progress

    progress_by_topic = {
        'Application': False,
        'Transport': False,
        'Network': False,
        'Link': False,
    }

    if progress:
        if progress >= 1:
            progress_by_topic['Link'] = True
        if progress >= 2:
            progress_by_topic['Network'] = True
        if progress >= 3:
            progress_by_topic['Transport'] = True
        if progress >= 4:
            progress_by_topic['Application'] = True

    return progress_by_topic

@app.route('/retrieve-accuracy-data', methods=["POST"])
@login_required
def accuracy_data():
    print('accuracy data')

    requested_topics = request.form['topics']

    print('request topics', requested_topics)

    topic_of_interest = []
    accuracy_per_topic = {
        'Application': 0,
        'Transport': 0,
        'Network': 0,
        'Link': 0
    }

    if requested_topics == 'All':
        topic_of_interest = ['Link', 'Network', 'Transport', 'Application']
    else:
        topic_of_interest.append(requested_topics)

    print('topic of interest')

    for topic in topic_of_interest:
        print('topic', topic)
        mark_per_question = []

        questions_in_topic = Question.query.filter_by(section=topic).all()

        for question in questions_in_topic:
            print('question', question)
            mark_for_question = Mark.query.filter_by(question_id_fk=question.question_id).first() if (Mark.query.filter_by(question_id_fk=question.question_id).first()) else 0
            print('mark for question', mark_per_question)
            mark_per_question.append(mark_for_question)

        # If there is no marks in database, this means the user/student has not attempted this quiz, thus, returning 0
        if len(mark_per_question) == 0:
            accuracy_per_topic[topic] = 0
        else:
            mark_for_topic = sum(mark_per_question) / len(mark_per_question)
            accuracy_per_topic[topic] = mark_for_topic

    return accuracy_per_topic

@app.route('/manage-questions',  methods=['GET', 'POST'])
@login_required
def manage_questions():

    # check if current user has admin privileges or not - else flash error message
    print(current_user.admin)

    if not current_user.admin:
        flash('You need admin privileges to access this page! ' +
              'If you are an admin, please logout and login again using your admin account')
        return redirect(url_for('logout'))

    questions_form = ManageQuestionsForm()

    if questions_form.validate_on_submit():
        answer_options = []

        for answers in questions_form.answer_options.data:
            answer_option = Answer(
                answer = answers
            )
            answer_options.append(answer_option)
            db.session.add(answer_option)

        # Commit correct answer as well
        answer_option = Answer (
            answer = questions_form.correct_answer.data
        )
        answer_options.append(answer_option)
        db.session.add(answer_option)

        question = Question(
            section = questions_form.section.data,
            question = questions_form.question.data,
            correct_answer = questions_form.correct_answer.data,
            answer_options = answer_options
        )
        db.session.add(question)

        db.session.commit()

        flash('Question successfully added! To enter another question, enter the new question details and resubmit the form.')
        return (redirect(url_for('manage_questions')))

    return render_template('manage-questions.html', title="Manage Questions", questions_form= questions_form)


@app.route('/retrieve-questions')
@login_required
def retrieve_questions():
    topic = str(request.args.get('topic'))

    # Check if we need to implement auto shuffle questions
    questions_array = []

    question_list = Question.query.filter_by(section=topic).all()

    for question in question_list:
        answer_options = []
        answer_list = question.answer_options.all()

        for answers in answer_list:
            answer_options.append(answers.answer)

        questionConfig = {
            'questionContent': question.question,
            'questionId': 'question-id-' + str(question.question_id),
            'answerOptions': answer_options
        }
        questions_array.append(questionConfig)

    return jsonify(data=questions_array)

@app.route('/retrieve-results', methods=["POST"])
@login_required
def check_answers():

    return '50'


