from aiogram.fsm.state import StatesGroup, State

class Utils(StatesGroup):
    group = State()
    message = State()