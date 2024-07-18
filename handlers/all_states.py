from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# general_router, admin_router, oait_manager_router, oait_router, retail_router) #
# ----------------------------------------------------------------------------------------------------------------------



# -------------------------------------------------- general_router
# class StartUser(StatesGroup):
#     """
#     """
#
#     hi = State()


class InputUser(StatesGroup):

    hi = State()
    get_city = State()
    get_city_trigger = State()