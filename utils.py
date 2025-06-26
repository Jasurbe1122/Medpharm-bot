
from telegram import ChatMemberAdministrator, ChatMemberOwner

def get_username(user):
    return user.username or user.first_name or f"user{user.id}"

async def is_admin(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    member = await context.bot.get_chat_member(chat_id, user_id)
    return isinstance(member, (ChatMemberAdministrator, ChatMemberOwner))
