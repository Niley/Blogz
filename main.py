from app import db, Flask, request, redirect, render_template, app, session
from models import BlogPost, User




@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'userlist']
    if request.endpoint not in allowed_routes and 'usrnm' not in session:
        return redirect('/login')

@app.route('/blog', methods=['GET', 'POST'])
def index():
    usrnm = ""
    header = "Blog-Z"
    post_id = request.args.get("post")
    author_id = request.args.get("author")
    # posts = []

    # #checking whether I have an active session; will display user info if so
    if 'usrnm' in session:
        author = User.query.filter_by(usrnm=session['usrnm']).first()
        usrnm = author.usrnm
        header = author.usrnm + " 's blog"
    #     usrnm = session['usrnm']
    posts = BlogPost.query.all()
    if post_id:
        posts = BlogPost.query.filter_by(id=post_id).all()
        header = posts[0].title
    if author_id:
        posts = BlogPost.query.filter_by(author_id=author_id).all()
        author = User.query.filter_by(id=author_id).first()
        header = author.usrnm + "'s posts."

    return render_template('blog.html', title= header, posts = posts, h1 = header, usrnm = usrnm)

    # return render_template('blog.html',title="Me blog!", posts = posts, h1 = header, usrnm=usrnm)

@app.route('/', methods=['GET', 'POST'])
@app.route('/users', methods=['GET'])
def userlist():
    usrnm = ''
    if 'usrnm' in session:
        usrnm = session['usrnm']
    users = User.query.all()
    return render_template('users.html', title = "User list", users = users, usrnm = usrnm)


@app.route('/login', methods=['POST', 'GET'])
def login():
    e_login = ''
    usrnm = ""
    if request.method == 'POST':
        usrnm = request.form['usrnm']
        password = request.form['password']
        user = User.query.filter_by(usrnm=usrnm).first()
        if user and user.password == password:
            session['usrnm'] = usrnm
            return redirect('/newpost')
        else:
            e_login = "Username and/or password are wrong or don't exist!"

    return render_template('login.html', e_login=e_login, usrnm = usrnm)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    e_content = ""
    e_title = ""

    if "usrnm" not in session:
        return '<h1>Not logged in, fixit</h1>'

    if request.method == 'POST':

        author = User.query.filter_by(usrnm=session['usrnm']).first()
        title = request.form['title']
        content = request.form['content']
        #_______________begin input error handling____________
        error = False
        
        # __checking if input variables are okay__
        if title == '':
            error = True
            e_title = "Please use a title for your blogpost"
        
        if content == '':
            error = True
            e_content = "Please input some content for your blogpost"
        
        # __returning error page if any input is faulty__
        if error:
            return render_template('newpost.html', 
        title = "New blog post", 
        title_ins = title, 
        content_ins = content,
        error_title = e_title, 
        error_content = e_content)
        #_______________end input error handling____________

        new_post = BlogPost(title, content, author)
        db.session.add(new_post)
        db.session.commit()
        
        posts = BlogPost.query.filter_by(id=new_post.id).all()
        return render_template('blog.html', title='Me blog!', posts = posts, h1 = new_post.title, usrnm = session['usrnm'])

    return render_template('newpost.html', title="New blog post", h1 = "New Post", usrnm = session['usrnm'])

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    usrnm = ""
    if request.method == 'POST':

        #_______________begin input error handling____________
        error =  False
        usrnm = request.form['usrnm']
        e_usrnm = ""
        pw = request.form['password']
        e_pw = ""
        verify = request.form['verify']

        # __checking if input variables are okay__
        if len(usrnm) < 3 or len(pw) < 3:
            error = True
            e_usrnm = "Both your username and password have to be more than 3 characters!"
        if usrnm == '':
            error = True
            e_usrnm = "Please type a user name."
        if pw == '':
            error = True
            e_pw = "Please type a password."
        if pw != verify:
            error = True
            e_pw = "Both password entries must be the same!"
         

        # __returning error page if any input is faulty__
        if error:
            return render_template("signup.html",
        usrnm_ins = usrnm,
        pw_ins = pw,
        verify_ins = verify,
        error_usrnm = e_usrnm,
        error_pw = e_pw)
        #_______________end input error handling____________
  
        existing_user = User.query.filter_by(usrnm=usrnm).first()
        if existing_user:
            return '<h1>Dupe user yo!</h1>'

        new_user = User(usrnm, pw)
        db.session.add(new_user)
        db.session.commit()
        session['usrnm'] = usrnm
        
        return redirect('/newpost')

    return render_template('signup.html', title="User signup", h1 = "User signup", usrnm = usrnm)
    
@app.route('/logout', methods=['POST'])
def logout():
    
    if 'usrnm' in session:
        del session['usrnm']
    return redirect('/blog')


if __name__ == '__main__':
    app.run()