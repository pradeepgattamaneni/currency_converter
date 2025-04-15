from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def convert_currency(from_currency, to_currency, amount):
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200 and "rates" in data:
            result = data["rates"].get(to_currency)
            if result:
                return result
            else:
                return "Conversion rate not found"
        else:
            return "Error fetching exchange rate"
    except Exception as e:
        return f"Exception occurred: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        from_currency = request.form["from_currency"].upper()
        to_currency = request.form["to_currency"].upper()
        amount = float(request.form["amount"])

        result = convert_currency(from_currency, to_currency, amount)
        return render_template("index.html", result=result, from_currency=from_currency, to_currency=to_currency, amount=amount)

    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)