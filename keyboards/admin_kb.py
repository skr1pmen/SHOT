from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать группу"),
            KeyboardButton(text="Редактировать группу")
        ],
        [
            KeyboardButton(text="Отменить рассылку"),
            KeyboardButton(text="Удалить группу"),

        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)