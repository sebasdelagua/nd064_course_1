import sqlite3
import logging, sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

db_connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    if post is None:
        app.logger.info('Article "' + str(post_id) + '" not found!')
        return render_template('404.html'), 404
    else:
        app.logger.info('Article "' + post['title'] + '" retrieved!')
        return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info('Article "' + str(post_id) + '" not found!')
      return render_template('404.html'), 404
    else:
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('The "About Us" page is retrieved.')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            
            app.logger.info('A new article ' + title + ' was created.')
            return redirect(url_for('index'))

    return render_template('create.html')

# Define the healthz endpoint
@app.route('/healthz')
def healthz():
    connection = get_db_connection()
    table_exists = connection.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='posts' ''')
    
    if table_exists.fetchone()[0]==1 : 
        response = app.response_class(
                response=json.dumps({"result":"OK - healthy"}),
                status=200,
                mimetype='application/json'
        )
    else:
        response = app.response_class(
                response=json.dumps({"result":"ERROR - unhealthy"}),
                status=500,
                mimetype='application/json'
        )

    return response

# Define the metrics endpoint
@app.route('/metrics')
def metrics():
    global db_connection_count
    connection = get_db_connection()
    count_posts = connection.execute('SELECT COUNT(*) FROM posts').fetchone()
    connection.close()
    response = app.response_class(
            response=json.dumps({"db_connection_count": db_connection_count, "post_count": count_posts[0]}),
            status=200,
            mimetype='application/json'
    )
    return response

# start the application on port 3111
if __name__ == "__main__":
    # set logger to handle STDOUT and STDERR 
    stdout_handler =  logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)
    handlers = [stderr_handler, stdout_handler]
    
    # format output
    format_output = '%(asctime)s - %(message)s'

    logging.basicConfig(format=format_output, level=logging.DEBUG, handlers=handlers)
        
    app.run(host='0.0.0.0', port='3111')
