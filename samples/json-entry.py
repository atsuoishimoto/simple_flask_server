@app.route('/sample-api', methods=["POST"])
def post1():
    print(dict(request.json))
    return {"hello":"world"}

