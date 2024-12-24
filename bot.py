import logging
import asyncio
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher, F  # правильный импорт
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter
from handlers.start_handler import start_handler  # Импортируем саму функцию
from handlers.income_handler import IncomeState, add_income, income_category_selected, income_amount_entered, income_description_entered
from handlers.expense_handler import ExpenseState, add_expense, expense_category_selected, expense_amount_entered, expense_description_entered
from handlers.export_handler import export_data_step1, handle_start_year, handle_start_month, handle_end_selection

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем экземпляр бота
bot = Bot(token=BOT_TOKEN)

# Создаем хранилище состояний
storage = MemoryStorage()

# Создаем экземпляр диспетчера
dp = Dispatcher()

# Регистрируем обработчики с использованием фильтров
dp.message.register(start_handler, Command("start"))

# Обработчик для добавления дохода с фильтром текста
dp.message.register(add_income, F.text == "Добавить доход")
dp.callback_query.register(income_category_selected, F.data.startswith("income_"))
dp.message.register(income_amount_entered, StateFilter(IncomeState.income_amount))
dp.message.register(income_description_entered, StateFilter(IncomeState.income_description))

dp.message.register(add_expense, F.text == "Добавить расход")
dp.callback_query.register(expense_category_selected, F.data.startswith("expense_"))
dp.message.register(expense_amount_entered, StateFilter(ExpenseState.expense_amount))
dp.message.register(expense_description_entered, StateFilter(ExpenseState.expense_description))

dp.message.register(export_data_step1, F.text == "Экспорт данных")
dp.callback_query.register(handle_start_year, lambda c: c.data.startswith("start_year_"))
dp.callback_query.register(handle_start_month, lambda c: c.data.startswith("start_month_"))
dp.callback_query.register(handle_end_selection, lambda c: c.data.startswith("end_month_"))

async def main():
    # Запускаем polling
    await dp.start_polling(bot, storage=storage)

if __name__ == "__main__":
    asyncio.run(main())
