from flask import Flask, request, render_template, jsonify
import requests

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)
#Allows tracing HTTP requests made by the requests library
RequestsInstrumentor().instrument()

def convert_currency(from_currency, to_currency, amount):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("ConvertCurrency") as span:
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            return data["rates"].get(to_currency)
        except:
            return None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("convert") as span:
        data = request.get_json()
        from_currency = data.get("from_currency", "").upper()
        to_currency = data.get("to_currency", "").upper()
        amount = data.get("amount")

        try:
            amount = float(amount)
            result = convert_currency(from_currency, to_currency, amount)
            if result:
                return jsonify({"result": round(result, 2)})
            else:
                return jsonify({"error": "Conversion failed"}), 500
        except:
            return jsonify({"error": "Invalid input"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
