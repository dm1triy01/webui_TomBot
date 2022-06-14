from flask import Flask, render_template, redirect, session
from flask import request
from zenora import APIClient
from access import access

import login_config

app = Flask(__name__)
app.config["SECRET_KEY"] = "verysecret"
client = APIClient(login_config.TOKEN, client_secret=login_config.CLIENT_SECRET)


@app.route('/')
def default():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        return render_template('test.html', current_user=current_user)
    return render_template('test.html', redirect_uri=login_config.OAUTH_URL)


@app.route('/oauth/callback/')
def callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, login_config.REDIRECT_URI).access_token
    session['token'] = access_token
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    print(str(request.url))
    print(str(request.endpoint))
    print(str(request.path))
    return redirect('/')


# @app.route('/selected/', methods=['GET', 'POST'])
# def select_func():
#     var = request.form.get('var')
#     if var == 'Hola':
#         select = 'Hola'
#         return render_template('selected.html', select=select)
#     elif var == 'Halo':
#         select = 'Halo'
#         return render_template('selected.html', select=select)
#     elif var == 'secret':
#         select = '$Серёга Gay$'
#         return render_template('selected.html', select=select)


@app.route('/ru/', methods=['POST', 'GET'])
def default_ru():
    return render_template('test_ru.html')


# @app.route('/ru/about/', methods=['POST', 'GET'])
# def about_ru():
#     return render_template('about_ru')


@app.route('/panel/', methods=['POST', 'GET'])
def panel():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        if current_user.id in access:
            show = True
        return render_template('panel.html', current_user=current_user, show=show)
    return render_template('panel.html', redirect_uri=login_config.OAUTH_URL)


@app.route('/about/', methods=['POST', 'GET'])
def about():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        return render_template('about.html', current_user=current_user)
    return render_template('about.html', redirect_uri=login_config.OAUTH_URL)


if __name__ == '__main__':
    app.run()
