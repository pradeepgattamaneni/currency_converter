import requests

def convert_currency(from_currency, to_currency, amount):
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200 and "rates" in data:
            result = data["rates"].get(to_currency)
            if result:
                print(f"\n✅ {amount} {from_currency} = {result:.2f} {to_currency}")
            else:
                print(f"\n❌ Conversion rate for {to_currency} not found.")
        else:
            print("\n❌ Error fetching exchange rate.")
            print("Response:", data)
    except Exception as e:
        print("\n❌ Exception occurred:", e)

if __name__ == "__main__":
    print("💱 Currency Converter (Powered by frankfurter.app)")
    from_currency = input("From Currency (e.g., USD): ").strip().upper()
    to_currency = input("To Currency (e.g., EUR): ").strip().upper()

    try:
        amount = float(input("Amount: "))
        convert_currency(from_currency, to_currency, amount)
    except ValueError:
        print("❌ Please enter a valid number for the amount.")