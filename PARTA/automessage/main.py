from library import *
from utilits import *

app = Flask(__name__)

@app.route('/')
def home():
	return render_template(
		'home.html',
		token=get_token()
	)

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
	if request.method == 'POST':
		if 'delete_token' in request.form:
			delete_token()
			return redirect('/')
		
		insert_token(request.form['input_token'])
		token = auth_token(get_token())
		send_msg(
			session=token,
			message=request.form['message'],
			users_id=request.form['list_id']
		)
		
	return redirect('/')