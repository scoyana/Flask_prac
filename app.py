from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:root@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.title}>'

    
# 앱 컨텍스트 안에서 DB 테이블 생성
with app.app_context():
    db.create_all() # 모델 클래스에 정의된 모든 테이블을 데이터베이스에 생성 -> 애플리케이션 첫 실행시 주로 사용



@app.route("/")
def index():
    posts = Post.query.all() # 모든 게시글 조회
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/')
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get(id)  # 해당 id로 게시글 조회
    
    print(f"Edit function called with id: {id}")  # 디버그 출력
    
    post = Post.query.get(id)
    print(f"Post found: {post}")  # 게시물 데이터 확인

    if post is None:
        return redirect('/')  # 게시글이 없다면 메인 페이지로 리디렉션
    

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        
        db.session.commit()  # 수정 사항을 DB에 반영
        print(f"Updated Post: {post.title}, {post.content}")  # 디버그 출력

        return redirect('/')
    
    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    post = Post.query.get(id)  # 해당 id로 게시글 조회
    db.session.delete(post)  # 삭제
    db.session.commit()  # 커밋하여 DB에서 제거

    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)
