# 🛒 Telegram E-Commerce Price Tracker Bot

A multi-threaded Python backend application that allows users to track e-commerce product prices dynamically via a Telegram Bot. 

Users can send a product URL directly to the bot, set a custom target price, and the system will continuously monitor the web page in the background, sending an automated alert when the price drops below the threshold.

## 🚀 Features
* **Interactive Telegram Interface:** Communicates directly with users to capture product URLs and custom target prices.
* **Automated Background Scraping:** Utilizes Python's `threading` to check prices at scheduled intervals without interrupting the main bot instance.
* **Dynamic Web Parsing:** Uses `BeautifulSoup` to extract and sanitize pricing data from complex HTML structures.
* **Anti-Spam Logic:** Automatically halts tracking and clears memory for a specific item once the target price is successfully met.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Libraries:** `pyTelegramBotAPI`, `requests`, `BeautifulSoup4`
* **Concepts:** Multi-threading, DOM parsing, REST APIs, Configuration Management

## 💻 Installation & Setup

1. Clone this repository:
   ```bash
   git clone [https://github.com/sarvesh-y09/telegram-price-tracker.git](https://github.com/sarvesh-y09/telegram-price-tracker.git)
   cd telegram-price-tracker

2. Install the required dependencies:
Bash
pip install pyTelegramBotAPI requests beautifulsoup4

3. Create a config.py file in the root directory and add your Telegram Bot Token:
Python
TELEGRAM_TOKEN="your_bot_token_here"

4. Run the script:
Bash
python tracker.py




📸 **Usage**

1) Start the bot on Telegram and send a product URL (e.g., https://example.com/product/123).

2) The bot will prompt you for your target price. Reply with a number (e.g., 150.00).

3) The bot will verify the current price and begin background tracking.

4) Receive an instant alert with a purchase link once the price drops!
