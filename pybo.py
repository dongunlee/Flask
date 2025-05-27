from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션을 위한 시크릿 키

qa_data = []

# 관리자 계정 (간단한 방식으로 하드코딩)
ADMIN_USER = 'admin'

@app.route('/')
def index():
    username = session.get('username')
    is_admin = username == ADMIN_USER
    return render_template('index.html', qa_data=qa_data, username=username, is_admin=is_admin)

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
    qa_data.append({
        'question': question,
        'answer': '',
        'author': session['username'],
        'answered_by': '',
        'accepted': False
    })
    return redirect(url_for('index'))

@app.route('/answer/<int:qa_id>', methods=['GET', 'POST'])
def answer(qa_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        answer = request.form['answer']
        qa_data[qa_id]['answer'] = answer
        qa_data[qa_id]['answered_by'] = session['username']
        qa_data[qa_id]['accepted'] = False
        return redirect(url_for('index'))
    return render_template('answer.html', qa_id=qa_id, qa=qa_data[qa_id])

@app.route('/accept/<int:qa_id>')
def accept_answer(qa_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    qa = qa_data[qa_id]
    if session['username'] != qa['author']:
        flash("작성자만 답변을 채택할 수 있습니다.")
        return redirect(url_for('index'))

    qa['accepted'] = True
    flash("답변이 채택되었습니다.")
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    if session.get('username') != ADMIN_USER:
        flash("관리자만 접근 가능합니다.")
        return redirect(url_for('index'))
    return render_template('admin.html', qa_data=qa_data)

@app.route('/admin/delete/<int:qa_id>', methods=['POST'])
def delete_question(qa_id):
    if session.get('username') != ADMIN_USER:
        flash("관리자만 질문을 삭제할 수 있습니다.")
        return redirect(url_for('index'))

    if 0 <= qa_id < len(qa_data):
        qa_data.pop(qa_id)
        flash("질문이 삭제되었습니다.")
    else:
        flash("존재하지 않는 질문입니다.")
    return redirect(url_for('admin_panel'))
