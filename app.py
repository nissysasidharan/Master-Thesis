from flask import Flask, render_template, request, redirect


@app.route('/')
def index():
    return render_template('questionaire.html')



if __name__ == '__main__':
    app.run(debug=True)
