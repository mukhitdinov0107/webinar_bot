import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = '7370103571:AAE9kt4y05R78V0dH5il63rojLZ6RyqQWiE'  # Replace with your bot's API token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Channel usernames or IDs the user needs to subscribe to
required_channels = ['@najmitdinm']  # Replace with your channel usernames

async def is_user_subscribed(user_id: int, channel: str) -> bool:
    """Check if a user is subscribed to a channel."""
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Error checking subscription status: {e}")
        return False

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    """Send a welcome message with a check button."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Check Subscription", callback_data="check_subscription")
    await message.answer("Welcome! Please subscribe to the following channels: https://t.me/addlist/Ao4HOwz7M_JkNDk6", reply_markup=keyboard.as_markup())

@dp.callback_query(lambda call: call.data == "check_subscription")
async def check_subscription(callback_query: types.CallbackQuery):
    """Check if the user is subscribed to all required channels."""
    user_id = callback_query.from_user.id
    non_subscribed_channels = []

    # Check subscription status for each channel
    for channel in required_channels:
        if not await is_user_subscribed(user_id, channel):
            non_subscribed_channels.append(channel)

    if non_subscribed_channels:
        # Send channel links if not subscribed
        channels_list = '\n'.join([f"<a href='https://t.me/{channel[1:]}'>Subscribe to {channel}</a>" for channel in non_subscribed_channels])
        await callback_query.message.answer(f"You need to subscribe to the following channels:\n{channels_list}", parse_mode="HTML")
    else:
        await callback_query.message.answer("Thank you for subscribing to all channels! Join our webinar channel: https://t.me/+A-saUI88E1xkNDU6")

if __name__ == '__main__':
    dp.run_polling(bot)