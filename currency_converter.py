from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_currency():
    data = request.get_json()
    from_currency = data.get('from_currency', '').upper()
    to_currency = data.get('to_currency', '').upper()
    amount = data.get('amount')

    if not from_currency or not to_currency or not amount:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200 and "rates" in data:
            result = data["rates"].get(to_currency)
            if result:
                return jsonify({'result': round(result, 2)})
            else:
                return jsonify({'error': f'Conversion rate for {to_currency} not found'}), 404
        else:
            return jsonify({'error': 'Error fetching exchange rate', 'details': data}), 500
    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
