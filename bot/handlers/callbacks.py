from aiogram import Router, types, F
router = Router()

@router.callback_query(F.data.startswith("lang_"))
async def language_handler(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    pass