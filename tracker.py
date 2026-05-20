import os
import time
import threading
import requests
import telebot
from bs4 import BeautifulSoup
import config

TELEGRAM_TOKEN = config.TELEGRAM_TOKEN
bot = telebot.TeleBot(TELEGRAM_TOKEN)


tracked_item = {
    "url": None,
    "target_price": 0.0,
    "chat_id": None
}

PRICE_SELECTOR = "span.a-price-whole" 

def fetch_current_price(url, selector):
    """Fetches the page and extracts the numeric price."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        price_element = soup.select_one(selector)
        
        if price_element:
            price_str = price_element.text.strip()
            clean_price = "".join(char for char in price_str if char.isdigit() or char == '.')
            return float(clean_price)
        return None
    except Exception as e:
        print(f"Scraping failed: {e}")
        return None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🤖 Welcome to Price Tracker Bot!\n\nJust paste an e-commerce product URL here, and I will help you set up tracking.")

@bot.message_handler(func=lambda message: message.text.startswith('http'))
def handle_incoming_url(message):
    """Step 1: Catch the URL and ask for the price."""
    tracked_item["url"] = message.text
    tracked_item["chat_id"] = message.chat.id
    
    
    msg = bot.reply_to(message, "🔗 URL received!\n\nWhat is your target price? (Just type a number, e.g. `200` or `150.50`)", parse_mode="Markdown")
    

    bot.register_next_step_handler(msg, process_target_price)

def process_target_price(message):
    """Step 2: Save the price and start tracking."""
    try:
        
        target = float(message.text)
        tracked_item["target_price"] = target
        
        bot.send_message(message.chat.id, f"🎯 Target price set to **Rs.{target:.2f}**. Checking current price...", parse_mode="Markdown")
        
       
        current_price = fetch_current_price(tracked_item["url"], PRICE_SELECTOR)
        
        if current_price:
            bot.send_message(
                message.chat.id, 
                f"✅ **Tracking Started!**\n\nCurrent price: **Rs.{current_price:.2f}**\nTarget price: **Rs. {target:.2f}**\n\nI will notify you automatically if it drops!",
                parse_mode="Markdown"
            )
        else:
            bot.send_message(message.chat.id, "❌ I couldn't find the price on that page. Please check the URL or update the PRICE_SELECTOR in your code.")
            
    except ValueError:
   
        bot.reply_to(message, "⚠️ That doesn't look like a valid number. Please send the URL again to restart.")



def automated_price_checker():
    """Runs continuously in the background"""
    while True:
        if tracked_item["url"] and tracked_item["chat_id"] and tracked_item["target_price"] > 0:
            print(f"Checking background price for: {tracked_item['url']}")
            
            current_price = fetch_current_price(tracked_item["url"], PRICE_SELECTOR)
            
            if current_price and current_price <= tracked_item["target_price"]:
                alert_msg = (
                    f"🚨 *PRICE DROP ALERT!* 🚨\n\n"
                    f"The price dropped to **Rs.{current_price:.2f}** (Target was Rs.{tracked_item['target_price']:.2f})!\n"
                    f"🔗 [Buy It Here]({tracked_item['url']})"
                )
                bot.send_message(tracked_item["chat_id"], alert_msg, parse_mode="Markdown")
                
                
                tracked_item["url"] = None 
        
        time.sleep(3600)

if __name__ == "__main__":
    checker_thread = threading.Thread(target=automated_price_checker)
    checker_thread.daemon = True 
    checker_thread.start()
    
    print("🤖 Bot is running with dynamic pricing! Open Telegram to test it.")
    bot.infinity_polling()
