from workout_tracker.constans import BOT_TOKEN
from workout_tracker.db.database import init_db
from workout_tracker.request_handler.training_plan_request_handler import add_training_plan_handlers
from telegram.ext import Application
from telegram import Update


if __name__ == '__main__':
    init_db()
    application = Application.builder().token(BOT_TOKEN).build()
    add_training_plan_handlers(application)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
