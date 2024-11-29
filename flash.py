import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)
import openai
from config import token_gpt, token_bot
from base_answers import culture_deck_answers, get_random_answer
from descriptions import culture_info, interview_process, hackathon_info
import random

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set up OpenAI API
openai.api_key = token_gpt

# Define states for ConversationHandler
TEST = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ['/about', '/culture'],
        ['/interview', '/hackathon'],
        ['/ask', '/test']
    ]
    await update.message.reply_text(
        "Я рад приветствовать Вас в LatokenAssistantBot – Вашем помощнике в мире Latoken. Что вы хотите знать?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вот список команд, которые вы можете использовать:\n"
                                    "/start - Запустите бота\n"
                                    "/help - Получение справки и списка команд\n"
                                    "/about - Подробнее о боте\n"
                                    "/culture - Узнайте больше о культуре Latoken\n"
                                    "/interview - Информация о процессе собеседования\n"
                                    "/hackathon - Узнайте больше о хакатоне в Latoken\n"
                                    "/test - Пройдите тест по культуре Latoken\n"
                                    "/ask - Задать вопрос боту")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("LatokenAssistantBot — это интеллектуальный помощник, созданный для того, чтобы помочь кандидатам узнать больше о работе в Latoken, процессе собеседования и культуре компании. Бот готов ответить на ваши вопросы, предоставить информацию о хакатоне и даже провести тесты для оценки ваших знаний. Присоединяйтесь и узнайте, почему Latoken — это место, где вы хотите работать!!")

async def culture_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(culture_info)

async def interview_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(interview_process)

async def hackathon_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(hackathon_info)

async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, задайте свой вопрос.")

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['unique_questions'] = set()
    questions = list(culture_deck_answers.keys())
    questions_str = "\n".join(questions)
    await update.message.reply_text(f"Пожалуйста, выберите один из следующих вопросов:\n{questions_str}")

async def ask_next_question(update, context):
    logging.info("Задать следующий вопрос")
    test_index = context.user_data.get('test_index', 0)
    if test_index < len(culture_deck_answers):
        question = list(culture_deck_answers.keys())[test_index]
        await update.message.reply_text(question)
    else:
        await update.message.reply_text("Тест завершен. Спасибо!")
        return ConversationHandler.END

async def answer_test(update, context):
    logging.info("Ответ на тестовый вопрос")
    test_index = context.user_data.get('test_index', 0)
    if test_index < len(culture_deck_answers):
        user_answer = update.message.text
        question = list(culture_deck_answers.keys())[test_index]
        correct_answer = get_random_answer(question)
        if user_answer.lower() in correct_answer.lower():
            await update.message.reply_text("Correct!")
        else:
            await update.message.reply_text(f"{correct_answer}")
        context.user_data['test_index'] += 1
        await ask_next_question(update, context)
        return TEST
    else:
        return ConversationHandler.END

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    unique_questions = context.user_data.get('unique_questions', set())

    if user_message in culture_deck_answers:
        # Add the question to the set of unique questions if it hasn't been asked before
        if user_message not in unique_questions:
            unique_questions.add(user_message)
            context.user_data['unique_questions'] = unique_questions

        # Send a random answer
        answer = random.choice(culture_deck_answers[user_message])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

        # Check if all unique questions have been asked
        if len(unique_questions) == len(culture_deck_answers):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Тест пройден. Ваш результат: лизун марок на почте")
            # Clear the set to stop the test
            context.user_data.pop('unique_questions', None)
    else:
        # Use GPT-4 to answer other questions
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response.choices[0].message.content
        )

def main():
    application = ApplicationBuilder().token(token_bot).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('about', about_command))
    application.add_handler(CommandHandler('culture', culture_command))
    application.add_handler(CommandHandler('interview', interview_command))
    application.add_handler(CommandHandler('hackathon', hackathon_command))
    application.add_handler(CommandHandler('ask', ask_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('test', test_command)],
        states={
            TEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_test)]
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    application.run_polling()

if __name__ == '__main__':
    main()