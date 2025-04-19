import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ContentType
from aiogram.client.default import DefaultBotProperties

# === 🔧 Настройки ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHAT_ID = int(os.getenv("SOURCE_CHAT_ID", "-1002429690404"))

# Теги и подтемы
TAG_CHAT_MAPPING = {
    "УЛК Ленинского Комсомола пр-кт 7": {
        "group_id": -1002187630843,
        "subtopics": [14235]
    },
    "УЛК Репина 4": {
        "group_id": -1002040185724,
        "subtopics": [6231]
    },
    "УЛК Туполева 15": {
        "group_id": -1002260078936,
        "subtopics": [3557]
    },
    "УЛК Генерала Тюленева 40": {
        "group_id": -1002117038361,
        "subtopics": [12978]
    },
    "УЛК Ульяновский пр-кт 19пом1": {
        "group_id": -1002104898038,
        "subtopics": [21649]
    },
    "УЛК Кирова 54": {
        "group_id": -1002186031434,
        "subtopics": [6]
    },
    "УЛК Юности 51": {
        "group_id": -1002266923861,
        "subtopics": [3793]
    },
    "УЛК Генерала Тюленева пр-кт 6Б": {
        "group_id": -1002037195030,
        "subtopics": [15297]
    },
}

# === 🔍 Логирование ===
logging.basicConfig(level=logging.INFO)

# Используем default=DefaultBotProperties(...)
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()


@dp.message(F.chat.id == SOURCE_CHAT_ID)
async def handle_all_messages(message: types.Message):
    content_text = message.text or message.caption
    if not content_text:
        return

    for tag, chat_info in TAG_CHAT_MAPPING.items():
        if tag in content_text:
            complaint_text = f"⚠️ Внимание! Поступила жалоба! Примите меры! ⚠️\n\n{content_text}"

            for topic_id in chat_info["subtopics"]:
                try:
                    # Текст
                    if message.content_type == ContentType.TEXT:
                        await bot.send_message(
                            chat_id=chat_info["group_id"],
                            text=complaint_text,
                            message_thread_id=topic_id
                        )
                    # Медиа: фото, видео, документ, и т.д.
                    elif message.content_type in [
                        ContentType.PHOTO,
                        ContentType.VIDEO,
                        ContentType.DOCUMENT,
                        ContentType.VOICE,
                        ContentType.AUDIO,
                        ContentType.STICKER,
                        ContentType.ANIMATION,
                        ContentType.VIDEO_NOTE
                    ]:
                        await message.copy_to(
                            chat_id=chat_info["group_id"],
                            message_thread_id=topic_id,
                            caption=complaint_text if message.caption or message.text else None
                        )
                    # Остальные типы
                    else:
                        await message.copy_to(
                            chat_id=chat_info["group_id"],
                            message_thread_id=topic_id
                        )

                    logging.info(f"✅ Жалоба с тегом '{tag}' отправлена в подтему {topic_id}")

                except Exception as e:
                    logging.error(f"❌ Ошибка при пересылке в подтему {topic_id}: {e}")


# === 🚀 Запуск бота ===
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
