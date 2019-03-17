from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

# Configure Falsk-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] =465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'marchenko.alexander@gmail.com'
app.config['MAIL_PASSWORD'] = 'qjpccuxlfvqujddq'
app.config['MAIL_DEFAULT_SENDER'] = 'marchenko.alexander@gmail.com'

mail = Mail(app)

@app.route('/send_email')
def send_email():
	# Initialise the instance of Mail
	msg = Message("Hello",
		recipients=['marchenko.alexander@me.com']
		)
	msg.body = "TEST"
	# Send the email
	mail.send(msg)
	return ""


# Run the MailApp
if __name__ == "__main__":
	app.run()

