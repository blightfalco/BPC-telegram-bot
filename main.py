#!/usr/bin/env python3
"""
BLACK PRO CYBER Bot - Full Featured Ethical Cybersecurity Bot
"""

import logging
import random
import re
import feedparser
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters,
)

# CONFIG
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_IDS = [123456789]

FB_PAGE  = "https://www.facebook.com/profile.php?id=61575453639998"
FB_GROUP = "https://facebook.com/groups/3489135951233643/"

RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.darkreading.com/rss.xml",
]

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

TIPS_BN = [
    "🔐 শক্তিশালী পাসওয়ার্ড ব্যবহার করুন — অক্ষর, সংখ্যা ও চিহ্ন মিলিয়ে কমপক্ষে ১২ অক্ষরের।",
    "📱 সব গুরুত্বপূর্ণ অ্যাকাউন্টে Two-Factor Authentication (2FA) চালু রাখুন।",
    "🌐 Public Wi-Fi ব্যবহার করার সময় VPN ব্যবহার করুন।",
    "🎣 Phishing email চেনার উপায়: অপরিচিত লিঙ্কে ক্লিক করবেন না।",
    "🔄 সফটওয়্যার ও OS নিয়মিত আপডেট করুন — security patch জরুরি।",
    "💾 গুরুত্বপূর্ণ ডেটার backup রাখুন — 3-2-1 rule মেনে চলুন।",
    "🔍 অজানা USB drive কম্পিউটারে কখনো সংযুক্ত করবেন না।",
    "🛡️ Antivirus ও Firewall সবসময় চালু রাখুন।",
    "🔑 একই পাসওয়ার্ড একাধিক সাইটে ব্যবহার করবেন না।",
    "👁️ সোশ্যাল মিডিয়ায় ব্যক্তিগত তথ্য শেয়ার করার আগে সতর্ক থাকুন।",
    "🧩 Browser extension ইনস্টল করার আগে permission যাচাই করুন।",
    "📧 অপরিচিত email-এর attachment কখনো open করবেন না।",
    "🔒 Screen lock সবসময় চালু রাখুন — PIN বা Fingerprint দিয়ে।",
    "☁️ Cloud storage-এ sensitive ফাইল রাখার আগে encrypt করুন।",
    "🌍 অপরিচিত ওয়েবসাইটে personal তথ্য দেওয়া থেকে বিরত থাকুন।",
]

TIPS_EN = [
    "🔐 Use strong passwords — mix uppercase, lowercase, numbers & symbols, 12+ chars.",
    "📱 Enable Two-Factor Authentication (2FA) on all important accounts.",
    "🌐 Always use a VPN when connected to public Wi-Fi networks.",
    "🎣 Spot phishing: Don't click unknown links, verify sender's email.",
    "🔄 Keep your software and OS updated — security patches are critical.",
    "💾 Backup your data using the 3-2-1 rule (3 copies, 2 media, 1 offsite).",
    "🔍 Never plug in an unknown USB drive into your computer.",
    "🛡️ Keep your Antivirus and Firewall always active.",
    "🔑 Never reuse passwords. Use a Password Manager like Bitwarden.",
    "👁️ Be careful about personal info you share on social media.",
    "🧩 Review browser extension permissions before installing.",
    "📧 Never open attachments from unknown senders.",
    "🔒 Always enable screen lock — PIN, pattern, or fingerprint.",
    "☁️ Encrypt sensitive files before storing in cloud storage.",
    "🌍 Avoid entering personal info on unfamiliar websites.",
]

QUIZ_QUESTIONS = [
    {
        "q": "🧠 *কোনটি সবচেয়ে শক্তিশালী Authentication পদ্ধতি?*\n\nWhich is the strongest authentication method?",
        "options": ["A) Password only", "B) 2FA (Two-Factor Auth)", "C) Security Question", "D) PIN"],
        "answer": "B",
        "explain": "✅ *সঠিক উত্তর: B) 2FA*\n2FA দুটি স্তরে যাচাই করে — password + OTP/Authenticator। এটি সবচেয়ে নিরাপদ।",
    },
    {
        "q": "🧠 *Phishing Attack কীভাবে কাজ করে?*\n\nHow does a Phishing Attack work?",
        "options": ["A) Software vulnerability exploit", "B) Fake emails/sites to steal info", "C) Network packet sniffing", "D) Brute force password"],
        "answer": "B",
        "explain": "✅ *সঠিক উত্তর: B*\nPhishing-এ নকল email বা ওয়েবসাইট দিয়ে ব্যবহারকারীর তথ্য চুরি করা হয়।",
    },
    {
        "q": "🧠 *VPN কী কাজ করে?*\n\nWhat does a VPN do?",
        "options": ["A) Speeds up internet", "B) Blocks all viruses", "C) Encrypts traffic & hides IP", "D) Removes ads"],
        "answer": "C",
        "explain": "✅ *সঠিক উত্তর: C*\nVPN আপনার ইন্টারনেট ট্র্যাফিক এনক্রিপ্ট করে এবং আসল IP লুকিয়ে রাখে।",
    },
    {
        "q": "🧠 *Ransomware কী?*\n\nWhat is Ransomware?",
        "options": ["A) A type of firewall", "B) Malware that encrypts files for ransom", "C) A VPN protocol", "D) A password manager"],
        "answer": "B",
        "explain": "✅ *সঠিক উত্তর: B*\nRansomware ভাইরাস আপনার ফাইল এনক্রিপ্ট করে এবং মুক্তিপণ দাবি করে।",
    },
    {
        "q": "🧠 *SQL Injection কোন ধরনের attack?*\n\nSQL Injection is what type of attack?",
        "options": ["A) Network Attack", "B) Social Engineering", "C) Web Application Attack", "D) Physical Attack"],
        "answer": "C",
        "explain": "✅ *সঠিক উত্তর: C*\nSQL Injection ওয়েব অ্যাপের database-এ ক্ষতিকর SQL কোড ঢুকিয়ে দেয়।",
    },
    {
        "q": "🧠 *HTTPS এবং HTTP-এর পার্থক্য কী?*\n\nWhat's the difference between HTTPS and HTTP?",
        "options": ["A) HTTPS is faster", "B) HTTPS encrypts data (SSL/TLS)", "C) HTTP is more secure", "D) No difference"],
        "answer": "B",
        "explain": "✅ *সঠিক উত্তর: B*\nHTTPS SSL/TLS দিয়ে data এনক্রিপ্ট করে, HTTP করে না। সবসময় HTTPS ব্যবহার করুন।",
    },
    {
        "q": "🧠 *Man-in-the-Middle (MitM) attack কী?*\n\nWhat is a Man-in-the-Middle attack?",
        "options": ["A) Hacking a server directly", "B) Intercepting communication between two parties", "C) Flooding a server with requests", "D) Guessing passwords"],
        "answer": "B",
        "explain": "✅ *সঠিক উত্তর: B*\nMitM attack-এ হ্যাকার দুই পক্ষের মাঝে বসে তাদের যোগাযোগ আড়িপাতে বা পরিবর্তন করে।",
    },
    {
        "q": "🧠 *DDoS attack মানে কী?*\n\nWhat does DDoS stand for?",
        "options": ["A) Data Driven Operating System", "B) Distributed Denial of Service", "C) Dynamic DNS over SSL", "D) Dual Domain Security"],
        "answer": "B",
        "explain": "✅ *সঠিক উত্তর: B*\nDDoS মানে Distributed Denial of Service। অনেক device থেকে একসাথে আক্রমণ করে সার্ভার বন্ধ করে দেওয়া হয়।",
    },
]

LEARNING_RESOURCES = (
    "📚 *Ethical Cybersecurity — Learning Resources*\n\n"
    "*Free Platforms:*\n"
    "• [TryHackMe](https://tryhackme.com)\n"
    "• [HackTheBox](https://hackthebox.com)\n"
    "• [OverTheWire](https://overthewire.org)\n"
    "• [Cybrary](https://cybrary.it)\n"
    "• [OWASP](https://owasp.org)\n\n"
    "*CTF Platforms:*\n"
    "• [PicoCTF](https://picoctf.org)\n"
    "• [CTFtime](https://ctftime.org)\n\n"
    "*Certifications:*\n"
    "• CompTIA Security+\n"
    "• CEH (Certified Ethical Hacker)\n"
    "• OSCP (Advanced)\n\n"
    "*আমাদের Community:*\n"
    "• [Facebook Page](https://www.facebook.com/profile.php?id=61575453639998)\n"
    "• [Facebook Group](https://facebook.com/groups/3489135951233643/)"
)

verified_users = set()
news_cache = []


def join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📘 Facebook Page Follow করুন", url=FB_PAGE)],
        [InlineKeyboardButton("👥 Facebook Group-এ Join করুন", url=FB_GROUP)],
        [InlineKeyboardButton("✅ Join করেছি — Verify করুন", callback_data="verify")],
    ])


def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📰 Latest News", callback_data="news"),
            InlineKeyboardButton("🛡️ Daily Tips", callback_data="tips_menu"),
        ],
        [
            InlineKeyboardButton("🧠 Cyber Quiz", callback_data="quiz"),
            InlineKeyboardButton("🔐 Password Check", callback_data="passcheck"),
        ],
        [
            InlineKeyboardButton("📚 Learning Resources", callback_data="learn"),
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
        ],
        [
            InlineKeyboardButton("👥 Facebook Community", callback_data="community"),
        ],
    ])


def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")]
    ])


def fetch_news(limit=4):
    global news_cache
    articles = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:4]:
                articles.append({
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", ""),
                    "source": feed.feed.get("title", "Unknown"),
                })
        except Exception as e:
            logging.error("RSS error: %s", e)
    if articles:
        random.shuffle(articles)
        news_cache = articles
        logging.info("News cache updated: %d articles", len(news_cache))
    return news_cache[:limit] if news_cache else []


async def scheduled_news_fetch(context: ContextTypes.DEFAULT_TYPE):
    logging.info("Scheduled news fetch running...")
    fetch_news()
    logging.info("News cache refreshed.")


def check_password_strength(password: str) -> str:
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ কমপক্ষে ৮ অক্ষর হওয়া উচিত")

    if len(password) >= 12:
        score += 1
    else:
        feedback.append("⚠️ ১২+ অক্ষর হলে আরো শক্তিশালী হবে")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("❌ বড় হাতের অক্ষর (A-Z) নেই")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("❌ ছোট হাতের অক্ষর (a-z) নেই")

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("❌ সংখ্যা (0-9) নেই")

    if re.search(r'[!@#$%^&*()\[\],.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("❌ বিশেষ চিহ্ন (!@#$%) নেই")

    common = ["password", "123456", "qwerty", "admin", "letmein", "abc123"]
    if password.lower() in common:
        score = 0
        feedback.append("🚫 এটি একটি সাধারণ পাসওয়ার্ড — পরিবর্তন করুন!")

    if score <= 2:
        strength = "🔴 খুবই দুর্বল (Very Weak)"
    elif score == 3:
        strength = "🟠 দুর্বল (Weak)"
    elif score == 4:
        strength = "🟡 মাঝারি (Medium)"
    elif score == 5:
        strength = "🟢 শক্তিশালী (Strong)"
    else:
        strength = "💚 খুবই শক্তিশালী (Very Strong)"

    bar = "█" * score + "░" * (6 - score)
    result = "🔐 *Password Strength Checker*\n\n"
    result += "Strength: " + strength + "\n"
    result += "Score: [" + bar + "] " + str(score) + "/6\n\n"
    if feedback:
        result += "*উন্নতির পরামর্শ:*\n" + "\n".join(feedback)
    else:
        result += "✅ চমৎকার পাসওয়ার্ড! নিরাপদ।"
    result += "\n\n⚠️ _সতর্কতা: এই chat-এ কখনো real password পাঠাবেন না!_"
    return result


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in verified_users:
        await update.message.reply_text(
            "🔐 *স্বাগতম, " + user.first_name + "!*\n\n"
            "🖤 *BLACK PRO CYBER Bot*-এ আপনাকে স্বাগতম!\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ Bot ব্যবহার করতে হলে আমাদের\n"
            "📘 *Facebook Page* Follow করুন এবং\n"
            "👥 *Facebook Group*-এ Join করুন\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "👇 নিচের বোতামে ক্লিক করুন,\n"
            "তারপর *'Join করেছি'* বোতামে ক্লিক করুন।",
            parse_mode="Markdown",
            reply_markup=join_keyboard(),
        )
        return

    await update.message.reply_text(
        "🔐 *স্বাগতম আবার, " + user.first_name + "!*\n\n"
        "✅ আপনি আমাদের Community Member!\n\n"
        "নিচের মেনু থেকে বেছে নিন 👇",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "verify":
        verified_users.add(user_id)
        await query.edit_message_text(
            "✅ *Verification সফল! স্বাগতম!* 🎉\n\n"
            "আপনি এখন BLACK PRO CYBER Bot সম্পূর্ণ ব্যবহার করতে পারবেন!\n\n"
            "Ethical Cybersecurity শিখুন এবং community-তে সক্রিয় থাকুন। 💪\n\n"
            "নিচের মেনু থেকে শুরু করুন 👇",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
        return

    if user_id not in verified_users:
        await query.answer("⛔ আগে Join করুন এবং Verify করুন!", show_alert=True)
        await query.edit_message_text(
            "⛔ *Access Denied!*\n\n"
            "Bot ব্যবহার করতে আমাদের Facebook Community-তে Join করুন।",
            parse_mode="Markdown",
            reply_markup=join_keyboard(),
        )
        return

    if data == "news":
        await query.edit_message_text("⏳ সর্বশেষ Cybersecurity news আনছি...")
        articles = fetch_news(4)
        if not articles:
            text = "⚠️ এই মুহূর্তে news পাওয়া যাচ্ছে না। একটু পরে চেষ্টা করুন।"
        else:
            text = "📰 *Latest Cybersecurity News*\n━━━━━━━━━━━━━━━━━━\n\n"
            for i, a in enumerate(articles, 1):
                text += "*" + str(i) + ".* " + a["title"] + "\n"
                text += "📌 _" + a["source"] + "_\n"
                text += "[🔗 Read More](" + a["link"] + ")\n\n"
        await query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=back_menu(), disable_web_page_preview=True
        )

    elif data == "tips_menu":
        await query.edit_message_text(
            "🛡️ *Daily Security Tips*\n\nকোন ভাষায় tip চান?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🇧🇩 বাংলা Tip", callback_data="tip_bn"),
                    InlineKeyboardButton("🇬🇧 English Tip", callback_data="tip_en"),
                ],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")],
            ])
        )

    elif data == "tip_bn":
        tip = random.choice(TIPS_BN)
        await query.edit_message_text(
            "🛡️ *আজকের Security Tip*\n━━━━━━━━━━━━━━━━━━\n\n" + tip,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 আরেকটি Tip", callback_data="tip_bn")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")],
            ])
        )

    elif data == "tip_en":
        tip = random.choice(TIPS_EN)
        await query.edit_message_text(
            "🛡️ *Today's Security Tip*\n━━━━━━━━━━━━━━━━━━\n\n" + tip,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Another Tip", callback_data="tip_en")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")],
            ])
        )

    elif data == "quiz":
        q = random.choice(QUIZ_QUESTIONS)
        context.user_data["quiz_answer"] = q["answer"]
        context.user_data["quiz_explain"] = q["explain"]
        options_text = "\n".join(q["options"])
        await query.edit_message_text(
            q["q"] + "\n\n" + options_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("A", callback_data="ans_A"),
                    InlineKeyboardButton("B", callback_data="ans_B"),
                ],
                [
                    InlineKeyboardButton("C", callback_data="ans_C"),
                    InlineKeyboardButton("D", callback_data="ans_D"),
                ],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")],
            ])
        )

    elif data.startswith("ans_"):
        chosen = data.split("_")[1]
        correct = context.user_data.get("quiz_answer", "")
        explain = context.user_data.get("quiz_explain", "")
        if chosen == correct:
            result = "🎉 *সঠিক উত্তর!*\n\n" + explain
        else:
            result = "❌ *ভুল!* আপনি: " + chosen + "\n\n" + explain
        await query.edit_message_text(
            result, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 আরেকটি প্রশ্ন", callback_data="quiz")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")],
            ])
        )

    elif data == "passcheck":
        context.user_data["waiting_password"] = True
        await query.edit_message_text(
            "🔐 *Password Strength Checker*\n\n"
            "এখন test করতে চাওয়া password পাঠান।\n\n"
            "⚠️ _আসল password পাঠাবেন না! শুধু test password দিন।_",
            parse_mode="Markdown",
            reply_markup=back_menu()
        )

    elif data == "learn":
        await query.edit_message_text(
            LEARNING_RESOURCES, parse_mode="Markdown",
            reply_markup=back_menu(), disable_web_page_preview=True
        )

    elif data == "community":
        await query.edit_message_text(
            "👥 *আমাদের Facebook Community*\n━━━━━━━━━━━━━━━━━━\n\n"
            "📘 *Facebook Page* — Latest updates ও news পান\n"
            "👥 *Facebook Group* — প্রশ্ন করুন, আলোচনা করুন, শিখুন\n\n"
            "🤝 একসাথে শিখি, একসাথে বাড়ি!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📘 Facebook Page", url=FB_PAGE)],
                [InlineKeyboardButton("👥 Facebook Group", url=FB_GROUP)],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")],
            ])
        )

    elif data == "about":
        await query.edit_message_text(
            "ℹ️ *BLACK PRO CYBER Bot*\n━━━━━━━━━━━━━━━━━━\n\n"
            "*Features:*\n"
            "• 📰 Real-time security news (RSS)\n"
            "• 🛡️ Daily security tips (বাংলা + English)\n"
            "• 🧠 Cybersecurity quiz/MCQ\n"
            "• 🔐 Password strength checker\n"
            "• 📚 Learning resources\n"
            "• 👥 Facebook community links\n\n"
            "🚫 *এই bot কোনো অবৈধ কার্যক্রম সমর্থন করে না।*\n\n"
            "Made with love for BD Cyber Community",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📘 Facebook Page", url=FB_PAGE)],
                [InlineKeyboardButton("👥 Facebook Group", url=FB_GROUP)],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")],
            ])
        )

    elif data == "menu":
        await query.edit_message_text(
            "🖤 *BLACK PRO CYBER Bot — Main Menu*\n\nনিচের মেনু থেকে বেছে নিন 👇",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in verified_users:
        await update.message.reply_text(
            "⛔ Bot ব্যবহার করতে আমাদের Facebook Community-তে Join করুন।",
            reply_markup=join_keyboard()
        )
        return

    if context.user_data.get("waiting_password"):
        context.user_data["waiting_password"] = False
        result = check_password_strength(update.message.text)
        await update.message.reply_text(
            result, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 আরেকটি Check", callback_data="passcheck")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")],
            ])
        )
    else:
        await update.message.reply_text(
            "👋 /start লিখে মেনু খুলুন।",
            reply_markup=main_menu_keyboard()
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    fetch_news()

    app.job_queue.run_repeating(
        scheduled_news_fetch,
        interval=21600,
        first=21600,
        name="news_cache_refresh"
    )

    print("BLACK PRO CYBER Bot started!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
