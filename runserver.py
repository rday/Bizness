from BiznessWeb import app


if __name__ == '__main__':
    if app.config['DEBUG'] is True:
        app.run(debug=True)

