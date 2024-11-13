import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Установите ключ API для OpenAI и Telegram
OPENAI_API_KEY = "ваш_ключ_openai"
TELEGRAM_API_KEY = "ваш_ключ_telegram"

# Инициализация OpenAI API
openai.api_key = OPENAI_API_KEY

# Этапы опроса
STAGE_ONE, STAGE_TWO, STAGE_THREE = range(3)

# Промты для каждого этапа
prompts = [
    "Пожалуйста, расскажите немного о себе. Как вас зовут и чем вы занимаетесь?",
    "Какие у вас интересы и хобби?",
    "Какие у вас профессиональные цели и амбиции?"
]


# Функция запроса к GPT
def get_gpt_response(prompt, user_response):
    combined_prompt = f"{prompt}\nПользователь: {user_response}\nGPT:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=combined_prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()


# Стартовая команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я ваш ассистент. Давайте начнем с первого вопроса.\n" + prompts[0]
    )
    return STAGE_ONE


# Первый этап
async def stage_one(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.message.text
    response = get_gpt_response(prompts[0], user_response)
    await update.message.reply_text(f"GPT: {response}\n\nТеперь следующий вопрос:\n" + prompts[1])
    return STAGE_TWO


# Второй этап
async def stage_two(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.message.text
    response = get_gpt_response(prompts[1], user_response)
    await update.message.reply_text(f"GPT: {response}\n\nИ последний вопрос:\n" + prompts[2])
    return STAGE_THREE


# Третий этап
async def stage_three(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.message.text
    response = get_gpt_response(prompts[2], user_response)
    await update.message.reply_text(f"GPT: {response}\n\nСпасибо за участие в опросе!")
    return ConversationHandler.END


# Основная функция для запуска бота
def main():
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    # Определение структуры диалога
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            STAGE_ONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, stage_one)],
            STAGE_TWO: [MessageHandler(filters.TEXT & ~filters.COMMAND, stage_two)],
            STAGE_THREE: [MessageHandler(filters.TEXT & ~filters.COMMAND, stage_three)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)

    print("Бот запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()
