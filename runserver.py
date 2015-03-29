from BiznessWeb import app

if app.config['DEBUG'] is True:
    app.run(debug=True)

