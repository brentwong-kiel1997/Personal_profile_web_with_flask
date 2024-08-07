from my_profile import app, send_email, db, socketio
from flask import render_template, request, flash, redirect,session, url_for
from my_profile.form import ContactForm
from my_profile.models import Contact
import json
import plotly
from flask_socketio import emit
from my_profile.plotting import create_btc_usd_chart


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/education')
def education_page():
    return render_template('education.html')

@app.route('/experience')
def experience_page():
    return render_template('experience.html')

@app.route('/skills')
def skills_page():
    return render_template('skills.html')

@app.route('/showcase')
def showcase_page():
    return render_template('showcase.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = ContactForm()

    if form.validate_on_submit():
        subject = f'message from {form.name.data} with email {form.email.data}'
        message = form.message.data
        send_email.send_email(subject=subject, message=message)
        contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        flash('Message sent successfully, thank you for your interest.', category='success')
        with app.app_context():
            db.session.add(contact)
            db.session.commit()
        return redirect('/contact')

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with sending a message: {err_msg}', category='danger')

    return render_template('contact.html', form=form)

@app.route('/AI_language_school')
def AI_language_school_page():
    return redirect('https://bals-brentwong.pythonanywhere.com/')


@app.route('/BTC_price', methods=['GET', 'POST'])
def BTC_price_page():
    # Create the figure using the function from plotting.py
    fig = create_btc_usd_chart()
    # Convert the figure to HTML and JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('BTC_USD.html', graphJSON=graphJSON)




@app.route('/chat_login', methods=['GET', 'POST'])
def chat_login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('chat'))
    return render_template('chat_login.html')

@app.route('/chat')
def chat():
    username = session.get('username', '')
    if not username:
        return redirect(url_for('chat_login'))
    return render_template('chat.html', username=username)

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonymous')
    emit('message', {'username': username, 'msg': data['msg']}, broadcast=True)

@socketio.on('set username')
def handle_username(username):
    session['username'] = username
    emit('username set', username, broadcast=False)


if __name__ == '__main__':
    socketio.run(app)
