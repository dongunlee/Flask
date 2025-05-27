from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션을 위한 시크릿 키

qa_data = []


@app.route('/')
def index():
    username = session.get('username')
    return render_template('index.html', qa_data=qa_data, username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/ask', methods=['POST'])
def ask():
    if 'username' not in session:
        return redirect(url_for('login'))
    question = request.form['question']
    qa_data.append({'question': question, 'answer': '', 'author': session['username']})
    return redirect(url_for('index'))


@app.route('/answer/<int:qa_id>', methods=['GET', 'POST'])
def answer(qa_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        answer = request.form['answer']
        qa_data[qa_id]['answer'] = answer
        qa_data[qa_id]['answered_by'] = session['username']
        return redirect(url_for('index'))
    return render_template('answer.html', qa_id=qa_id, qa=qa_data[qa_id])


if __name__ == '__main__':
    app.run(debug=True)