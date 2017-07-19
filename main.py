from app import db, Flask, request, redirect, render_template, app
from models import BlogPost

@app.route('/', methods=['GET'])
@app.route('/blog', methods=['GET'])
def index():
    posts = BlogPost.query.all()
    id = request.args.get("id")
    header = "Blog"
    #completed_tasks = Task.query.filter_by(completed=True).all()
    if id:
        posts = BlogPost.query.filter_by(id=id).all()
        header = posts[0].title 
    return render_template('blog.html',title="Me blog!", posts = posts, h1 = header)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    e_content = ""
    e_title = ""

    if request.method == 'POST':
        error = False
        title = request.form['title']
        if title == '':
            error = True
            e_title = "Please use a title for your blogpost"
        content = request.form['content']
        if content == '':
            error = True
            e_content = "Please input some content for your blogpost"
        
        if error:
            return render_template('newpost.html', 
        title = "New blog post", 
        title_ins = title, 
        content_ins = content,
        error_title = e_title, 
        error_content = e_content)
    

        new_post = BlogPost(title, content)
        db.session.add(new_post)
        db.session.commit()
        
        posts = BlogPost.query.filter_by(id=new_post.id).all()
        return render_template('blog.html', title='Me blog!', posts = posts, h1 = new_post.title)

    return render_template('newpost.html', title="New blog post", h1 = "New Post")



# @app.route('/delete-task', methods=['POST'])
# def delete_task():

#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     task.completed = True
#     db.session.add(task)
#     db.session.commit()

#     return redirect('/')


if __name__ == '__main__':
    app.run()