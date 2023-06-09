from secret_stuff import bot_token, github_repo_url
from user_info import UserInfo, KnownUserManager
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

known_users = KnownUserManager('known_users.json')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = UserInfo(update.effective_user.id, update.effective_user.full_name)

    if not known_users.is_known_user(user):
        known_users.add_user(user)
        
        text = f"Ciao _{user.name}_\."
    else: 
        text = f"Bentornato _{user.name}_\."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='MarkdownV2')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = f"Ciao _{update.effective_user.full_name}_\.\nSono _MovList_ e ti aiuterò a gestire film e serie TV che hai intenzione di guardare\."
    inline_keyboard = [
        [InlineKeyboardButton("Lista completa dei comandi", callback_data='comandi_spiegazione')],
        [InlineKeyboardButton("Lista delle features in arrivo", callback_data='nuove_features')],
        [InlineKeyboardButton("Repository GitHub", url=github_repo_url)]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=about_text, 
        parse_mode='MarkdownV2',
        reply_markup=InlineKeyboardMarkup(inline_keyboard)
    )

async def command_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    await query.delete_message()

    if query.data == "comandi_spiegazione":        
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Lista completa dei comandi")

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="_/start_: Manda un saluto all'utente;\n_/about_: Presentazione\.",
            parse_mode='MarkdownV2'
        )
    elif query.data == "nuove_features":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Al momento non c'è nulla in programma")


if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()
    
    start_handler = CommandHandler('start', start)
    about_handler = CommandHandler('about', about)
    command_list_handler = CallbackQueryHandler(command_list)

    application.add_handler(start_handler)
    application.add_handler(about_handler)
    application.add_handler(command_list_handler)

    application.run_polling()