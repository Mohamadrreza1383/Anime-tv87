from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime

# -------------------------
# 🔹 تنظیمات ربات
# -------------------------
BOT_TOKEN = "7968574879:AAFHH7bUWOjXc2heXVuBjtNT19XO9MZgp3E"  # ← اینجا توکن رباتتو قرار بده
ARCHIVE_CHANNEL_ID = -1003114976286  # ← اینجا آیدی کانال خصوصی (عدد بزرگ و منفی)
ADMIN_IDS = [5131647245]  # ← آیدی تلگرام خودت برای دسترسی حذف پیام


# -------------------------
# /start
# -------------------------
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "سلام 🎬 من پیام‌ها و فایل‌ها رو تو کانال خصوصی ذخیره می‌کنم.\n"
        "متن، ویدیو، عکس، فایل، صدا و استیکر بفرست."
    )


# -------------------------
# آرشیو پیام‌ها
# -------------------------
def save_to_channel(update: Update, context: CallbackContext):
    msg = update.message
    caption = f"فرستنده: {msg.from_user.full_name}\nتاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    sent = None
    try:
        if msg.text:
            sent = context.bot.send_message(chat_id=ARCHIVE_CHANNEL_ID, text=f"{caption}\n\n{msg.text}")
        elif msg.photo:
            photo_file = msg.photo[-1].file_id
            sent = context.bot.send_photo(chat_id=ARCHIVE_CHANNEL_ID, photo=photo_file, caption=caption)
        elif msg.video:
            sent = context.bot.send_video(chat_id=ARCHIVE_CHANNEL_ID, video=msg.video.file_id, caption=caption)
        elif msg.document:
            sent = context.bot.send_document(chat_id=ARCHIVE_CHANNEL_ID, document=msg.document.file_id, caption=caption)
        elif msg.audio:
            sent = context.bot.send_audio(chat_id=ARCHIVE_CHANNEL_ID, audio=msg.audio.file_id, caption=caption)
        elif msg.voice:
            sent = context.bot.send_voice(chat_id=ARCHIVE_CHANNEL_ID, voice=msg.voice.file_id, caption=caption)
        elif msg.sticker:
            sent = context.bot.send_sticker(chat_id=ARCHIVE_CHANNEL_ID, sticker=msg.sticker.file_id)

        if sent:
            # لینک پیام برای کانال خصوصی
            link = f"https://t.me/c/{str(ARCHIVE_CHANNEL_ID)[4:]}/{sent.message_id}"
            msg.reply_text(f"✅ ذخیره شد.\nلینک پیام: {link}")
    except Exception as e:
        msg.reply_text(f"❌ خطا در ذخیره پیام: {e}")


# -------------------------
# حذف پیام
# -------------------------
def delete_from_channel(update: Update, context: CallbackContext):
    if update.message.from_user.id not in ADMIN_IDS:
        update.message.reply_text("❌ اجازه ندارید پیام‌ها را حذف کنید.")
        return
    if not context.args:
        update.message.reply_text("بعد از /delete شناسه پیام را وارد کنید.")
        return
    try:
        msg_id = int(context.args[0])
        context.bot.delete_message(chat_id=ARCHIVE_CHANNEL_ID, message_id=msg_id)
        update.message.reply_text("❌ پیام حذف شد.")
    except Exception as e:
        update.message.reply_text(f"خطا در حذف پیام: {e}")


# -------------------------
# اجرای ربات
# -------------------------
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("delete", delete_from_channel))
    dp.add_handler(MessageHandler(Filters.all & ~Filters.command, save_to_channel))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
