from flask import Flask, request, Response


'''
petite app pour tester les webhook POST
'''

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def test_slash():
    if request.method == 'POST':
        print(f"@app.route('/' : {request.form}")

    return Response(f"Okay FLASK : {request.form}", status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()
