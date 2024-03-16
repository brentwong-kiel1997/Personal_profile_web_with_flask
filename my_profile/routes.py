from my_profile import app, email, db
from flask import render_template, request, flash, redirect
from my_profile.form import ContactForm
from my_profile.models import Contact
import yfinance as yf
import plotly.graph_objs as go
import json
import plotly

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
        email.send_email(subject=subject, message=message)
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
    return render_template('AI_language_school.html')


@app.route('/BTC_price', methods=['GET', 'POST'])
def BTC_price_page():
    data = yf.download(tickers='BTC-USD', interval='1m')

    fig = go.Figure(data=[
        go.Candlestick(x=data.index,
                       open=data['Open'],
                       high=data['High'],
                       low=data['Low'],
                       close=data['Close'],
                       increasing_line_color='#00CC96',  # Bright green
                       decreasing_line_color='#FF4136')  # Bright red
    ])

    # Add a line chart to connect the closing prices
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close', line=dict(color='yellow', width=2)))

    # Update layout with fixed x-axis range
    fig.update_xaxes(
        range=[data.index[0], data.index[-1]],
        rangeselector=dict(
            buttons=list([
                dict(count=15, label='15m', step='minute', stepmode='backward'),
                dict(count=45, label='45m', step='minute', stepmode='backward'),
                dict(step='all')
    ]), bgcolor='#333333'
        ),
        type='date'
    )

    fig.update_layout(
        title='BTC-USD Price Chart',
        title_x=0.5,
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False,
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#FFFFFF"
        )
    )

    # Convert the figure to HTML and JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('BTC_USD.html', graphJSON=graphJSON)

@app.route('/cv')
def cv_page():
    return