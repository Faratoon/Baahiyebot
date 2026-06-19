"""
handlers/start.py  –  /start, /help, /menu  — Single menu for merged bot
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.menus import main_menu_keyboard, main_inline_menu
from utils import firebase


WELCOME_TEXT = """\
🌟 *Ku soo dhawow {name}!*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 *Mfaratoon AI — All-in-One Bot*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📢 *Channel & Group Management*
📤 Broadcast, ✏️ Edit, 🗑️ Delete, ⏰ Schedule

🤖 *AI Assistant* (Somali / Arabic / English)

📚 *50+ Koorso FREE* — Raadi, daalaco, baro!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ Trial: `{trial_days}` days remaining
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👇 *Menu-ga hoose xulo:*
"""

HELP_TEXT = """\
📖 *Commands Guide*
━━━━━━━━━━━━━━━━━━━━━━━

🏠 *General:*
/start      → Menu ugu weyn
/help       → Commands-kan arag
/menu       → Inline menu fur
/profile    → Profile-kaaga

📢 *Channel & Group:*
/channels   → Channels maamul
/groups     → Groups maamul
/broadcast  → Dhammaan u dir
/schedule   → Post qorso

📚 *Courses:*
/courses    → 40+ koorso daalaco
/course     → Courses browser

🤖 *AI Models:*
/nano       → 💬 Nano Banana
/midjourney → 🎨 Midjourney
/sora       → 🖼️ Sora Images
/gpt_image  → 🤖 GPT Images
/flux       → 🎨 Flux Images
/veo        → 🎥 Veo3 Video

⚙️ *Settings:*
/settings   → Settings
/clear      → AI memory nadiifi
/admin      → Admin panel (admins)

━━━━━━━━━━━━━━━━━━━━━━━
💡 Buttons-ka hoose waa ugu fudud!
"""


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid  = user.id

    try:
        firebase.create_or_update_user(uid, {
            "user_id":    uid,
            "first_name": user.first_name or "",
            "last_name":  user.last_name  or "",
            "username":   user.username   or "",
        })
        trial_days = firebase.get_trial_days_left(uid)
    except Exception:
        trial_days = 30

    name = user.first_name or "Friend"
    text = WELCOME_TEXT.format(name=name, trial_days=trial_days)

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard()
    )
    # No duplicate inline menu — the reply keyboard has everything!


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.MARKDOWN)


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎛️ *Main Menu:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_inline_menu()
    )
