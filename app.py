from application import create_app

# Use DevelopmentConfig for running the server; tests will pass TestingConfig explicitly
app = create_app('DevelopmentConfig')

if __name__ == '__main__':
    app.run(debug=True)
