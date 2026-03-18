from flask import Flask, render_template, request
from vector_search import load_all_lemma_files, search_one_query 

app = Flask(__name__)
tf_idf, idf = load_all_lemma_files()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            results = search_one_query(query, tf_idf, idf)

    return render_template("index.html", query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True)

