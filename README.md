# 📈 Trading Bot for Binance

A bot for automated cryptocurrency trading on the **Binance** exchange.
Implements asset filtering, buying, and selling based on defined rules by performing a multithreaded process.

>⚠️ Important Notice : This bot currently does not perform real trades on the exchange. 
It simulates trading decisions and logs imaginary deals based on market data. 
It is intended for testing, learning, and strategy development.

---

## 🧠 Description

This trading bot analyzes the cryptocurrency market on **Binance**, gets a list 
of coins that are traded only to USDT and grew by more than X% over the past day
and then:
- **Loads a dataframe of a coin (ticker) candle interval for a 
specified period (lookback)**
- **Checks if market condition for the coin satisfies strategy**
- **Adds suitable assets to the portfolio**
- **Buys coins at current prices**
- **Constantly in the background checks if target or stop loss level met**
- **Sells them on stop-loss or take-profit**
- **Logs all actions to a file and console**
- **Records each trade in an Excel file**

The bot runs **in real-time** and supports **multithreading**, allowing it to simultaneously:
- Search for new assets
- Check buy conditions
- Monitor sell conditions

---

## ✅ Features

| Feature | Description                                                        |
|--------|--------------------------------------------------------------------|
| 🔍 Asset Filtering Strategy | Selects coins with rising price and increased trading volume       |
| 💵 Buy Execution | Buys coins if they match the strategy criteria                     |
| 🚨 Sell Conditions | Sells when stop-loss or take-profit levels are reached             |
| 📦 Portfolio Management | Adds/removes assets safely using thread locking (`threading.Lock`) |
| 📁 Logging | Detailed logging to file and output to console                     |
| 📎 Trade Recording | All trades are saved to an Excel file using thread locking for analysis                |
| ⚙️ Environment Configuration | API keys and settings are stored in `.env`                         |
| 📦 Virtual Environment Support | Easily run in isolation using `venv`                               |
| 🚀 Installation Script | Comes with a script to install dependencies and launch the bot     |

---

## 🧩 Project Structure

```
my_trading_bot/
│
├── main.py              # Entry point
├── strategy.py          # Buy/sell logic
├── client.py            # Binance API interaction
├── utils.py             # Helper functions (df_download, asset_list)
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── .env.example         # Your secret keys
├── install_and_run.sh   # Setup and run script
├── logs/                # Log files directory
└── trades.xlsx          # Trade history file. Created after first run
```

---

## 🛠️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your_username/my_trading_bot.git
cd my_trading_bot
```

### 2. Create virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Set up secrets

Create a `.env` file from the example:

```bash
cp .env.example .env
nano .env
```

Fill in your credentials:

```
MY_KEY=your_api_key
MY_PASS=your_api_secret
```

### 4. Run the bot

```bash
chmod +x install_and_run.sh
./install_and_run.sh
```

---

## 📄 Trade History

All completed trades are saved into the `trades.xlsx` file, created automatically in the project root.

Each row contains:
- Timestamp
- Ticker name (e.g., `BTCUSDT`)
- Trade type (`BUY` / `SELL`)
- Amount
- Buy/sell price
- Position size (after BUY)
- Profit (for SELL)

---

## 📋 Requirements

- Python 3.8+
- Binance API Key and Secret
- Libraries: `pandas`, `python-binance`, `openpyxl`, `python-dotenv`, `datetime`

---

## 📌 Example Output

```
[INFO] Strategy started
[INFO] New asset added: BTCUSDT
[INFO] Bought BTCUSDT at 62000.0
[INFO] Sold BTCUSDT at 62500.0 | Profit: 500.0
```

---

## ❤️ Support

If you like this project — a GitHub star is the best way to say thanks!

---

## 📬 Contact

📧 For collaboration or improvements:
kostyukovkg@yahoo.com

🌐 Check my website and more projects:
https://kkgweb.streamlit.app
