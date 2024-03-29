from flask import Flask, render_template, redirect, session
from flask import request
from zenora import APIClient
from access import access

import threading
import login_config
import core

app = Flask(__name__)
app.config["SECRET_KEY"] = "verysecret"
client = APIClient(login_config.TOKEN, client_secret=login_config.CLIENT_SECRET)

discord_status = core.discord_status()

@app.route('/')
def default():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        current_guilds = bearer_client.users.get_my_guilds()
        return render_template('test.html', current_user=current_user, current_guilds=current_guilds, access=access, status=discord_status.get_status())
    return render_template('test.html', redirect_uri=login_config.OAUTH_URL, status=discord_status.get_status())


@app.route('/oauth/callback/')
def callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, login_config.REDIRECT_URI).access_token
    session['token'] = access_token
    return redirect('/')


@app.route('/admin')
def admin():
    # print(str(request.url))
    # print(str(request.endpoint))
    # print(str(request.path))
    # return redirect('/')
    return render_template('admin.html', redirect_uri=login_config.OAUTH_URL)


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


@app.route('/panel/', methods=['POST', 'GET'])
def panel():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        current_guilds = bearer_client.users.get_my_guilds()
        # if current_user.id in access:
        #     show = True
        return render_template('panel.html', current_user=current_user, current_guilds=current_guilds, access=access, status=discord_status.get_status())
    return render_template('panel.html', redirect_uri=login_config.OAUTH_URL, status=discord_status.get_status())


@app.route('/about/', methods=['POST', 'GET'])
def about():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        return render_template('about.html', current_user=current_user, access=access, status=discord_status.get_status())
    return render_template('about.html', redirect_uri=login_config.OAUTH_URL, status=discord_status.get_status())


if __name__ == '__main__':
    discord_status.run_check_status()
    app.run(host="37.230.114.133", port="8000")