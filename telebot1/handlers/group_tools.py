"""
handlers/group_tools.py  –  Advanced Group Management
Soo dhaweyn, Sharciyo, Xaadirinta, Task-yada, Auto-reply
"""
import json
import os
from datetime import datetime, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from utils.menus import back_button
from utils import firebase

# ── States ────────────────────────────────────────────────────────────────────
WAITING_RULES       = 50
WAITING_TASK_NAME   = 51
WAITING_TASK_DESC   = 52
WAITING_AUTO_TRIGGER = 53
WAITING_AUTO_REPLY   = 54

# ── DATA FILE ─────────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

def _group_file(chat_id: int) -> str:
    return os.path.join(DATA_DIR, f"group_{chat_id}.json")

def _load_data(chat_id: int) -> dict:
    path = _group_file(chat_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"rules": "", "tasks": [], "auto_replies": {}, "attendance": {}}

def _save_data(chat_id: int, data: dict):
    with open(_group_file(chat_id), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# 📋 1. GROUP RULES (Sharciyada)
# ═══════════════════════════════════════════════════════════════════════════════
async def set_rules_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start setting group rules."""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            "📋 *Sharciyada Group-ka*\n\n"
            "Qor sharciyada group-kaaga:\n\n"
            "💡 *Tusaale:*\n"
            "1️⃣ ✨ Xushmad — Dhammaan xubnaha si xushmad leh ula dhaqan\n"
            "2️⃣ 🚫 Spam — Spam-ka waa mamnuuc\n"
            "3️⃣ 🔞 Xumo — Dadka xumeeyaan waa laga saari doonaa\n"
            "4️⃣ 🎯 Mawduuca — Ka hadal mawduucyada group-ka ku habboon\n"
            "5️⃣ 📢 Bot-ka — Bot-ka kale ha isticmaalin\n\n"
            "/cancel si aad joojiso",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_button("menu_groups")
        )
    return WAITING_RULES


async def receive_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save group rules."""
    chat_id = update.effective_chat.id
    data = _load_data(chat_id)
    data["rules"] = update.message.text.strip()
    _save_data(chat_id, data)

    await update.message.reply_text(
        "✅ *Sharciyada waa la kaydiyay!*\n\n"
        "Xubnaha cusub marka ay soo galaan, sharciyada ayaa toos u soo baxaya!",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_groups")
    )
    return ConversationHandler.END


async def show_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display group rules."""
    chat_id = update.effective_chat.id
    data = _load_data(chat_id)
    rules_text = data.get("rules", "")

    if not rules_text:
        text = "📋 *Sharci ma jiraan*\n\nWeli sharci lama dejin group-kan."
    else:
        text = (
            "📋 *📜 Sharciyada Group-ka*\n\n"
            f"{rules_text}"
        )

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ═══════════════════════════════════════════════════════════════════════════════
# 🎉 2. ADVANCED WELCOME (Soo dhaweyn + Sharciyo)
# ═══════════════════════════════════════════════════════════════════════════════
async def advanced_welcome_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """When new member joins: welcome + rules + sticker."""
    if not update.message or not update.message.new_chat_members:
        return

    chat = update.effective_chat
    data = _load_data(chat.id)
    rules_text = data.get("rules", "")

    for member in update.message.new_chat_members:
        if member.is_bot:
            continue

        name = member.first_name or "Friend"

        # Welcome text with GZ format
        welcome = (
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  ✨ 𝐊𝐔 𝐒𝐎𝐎 𝐃𝐇𝐀𝐖𝐎𝐖 ✨\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🖐 *Asalaamu Calaykum {name}!*\n\n"
            f"🌟 *Ka waran, group-keenna cusub!*\n"
            f"📢 Kanaal: @Farsamada\n"
            f"🎬 YouTube: MrFaraton\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
        )

        # Add rules if they exist
        if rules_text:
            welcome += (
                f"  📋 *SHARCIYADA*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{rules_text}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
            )

        welcome += (
            f"💡 *Fadlan ku raac:*\n"
            f"✅ Xushmad\n"
            f"✅ Ka qayb qaado\n"
            f"✅ Raac sharciyada\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"    𝐖𝐚𝐱𝐚𝐚𝐝 𝐤𝐮 𝐟𝐢𝐢𝐜𝐚𝐧! 🎉\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )

        await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN)

        # Send sticker (optional — try a welcome sticker)
        try:
            await context.bot.send_sticker(
                chat.id,
                "CAACAgIAAxkBAAEBGARm3sVaFBp8xTMfGJ_FyKvpUPQjUAACFgADW_7_FNYSIDy3_LDoNgQ"
            )
        except Exception:
            pass  # Sticker might not exist, ignore


# ═══════════════════════════════════════════════════════════════════════════════
# ✅ 3. ATTENDANCE (Xaadirinta)
# ═══════════════════════════════════════════════════════════════════════════════
ATTENDANCE_EMOJIS = ["✅", "❌", "⏳"]

async def attendance_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start attendance for today."""
    chat_id = update.effective_chat.id
    data = _load_data(chat_id)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if "attendance" not in data:
        data["attendance"] = {}

    if today not in data["attendance"]:
        data["attendance"][today] = {}

    _save_data(chat_id, data)

    btns = [
        [InlineKeyboardButton("✅ Joogaa", callback_data="att_yes"),
         InlineKeyboardButton("❌ Ma JoogO", callback_data="att_no")],
        [InlineKeyboardButton("⏳ Dambe", callback_data="att_later")],
    ]

    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "  📋 𝐗𝐀𝐀𝐃𝐈𝐑𝐈𝐍𝐓𝐀 𝐌𝐀𝐀𝐍𝐓𝐀\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📅 *{today}*\n\n"
        "Fadlan xulo xaadirintaada 👇",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(btns)
    )


async def attendance_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle attendance button clicks."""
    query = update.callback_query
    await query.answer()

    user = query.from_user
    chat_id = query.message.chat.id
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    data = _load_data(chat_id)
    if "attendance" not in data:
        data["attendance"] = {}
    if today not in data["attendance"]:
        data["attendance"][today] = {}

    status_map = {"att_yes": "✅ Joogaa", "att_no": "❌ Ma JoogO", "att_later": "⏳ Dambe"}
    emoji = query.data
    status = status_map.get(emoji, "✅ Joogaa")

    data["attendance"][today][str(user.id)] = {
        "name": user.full_name,
        "status": status,
        "time": datetime.now(timezone.utc).isoformat()
    }
    _save_data(chat_id, data)

    await query.edit_message_text(
        f"✅ *Waa la diiwaan geliyey!*\n\n"
        f"👤 {user.full_name}\n"
        f"📌 {status}\n"
        f"📅 {today}",
        parse_mode=ParseMode.MARKDOWN
    )


async def attendance_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show attendance stats."""
    chat_id = update.effective_chat.id
    data = _load_data(chat_id)

    if not data.get("attendance"):
        await update.message.reply_text(
            "📋 *Xaadirinta:*\n\nWeli qofna ma xaadirin.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    text = "━━━━━━━━━━━━━━━━━━━━━━\n"
    text += "  📊 𝐖𝐀𝐑𝐁𝐄𝐋𝐓𝐀 𝐗𝐀𝐀𝐃𝐈𝐑𝐈𝐍𝐓𝐀\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━\n\n"

    for date, members in sorted(data["attendance"].items(), reverse=True)[:7]:
        present = sum(1 for m in members.values() if m["status"] == "✅ Joogaa")
        absent = sum(1 for m in members.values() if m["status"] == "❌ Ma JoogO")
        total = len(members)
        text += f"📅 *{date}* — {total} qof\n"
        text += f"   ✅ Joogay: {present} | ❌ Ma Joogin: {absent}\n\n"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ═══════════════════════════════════════════════════════════════════════════════
# 📋 4. TASK MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
async def task_new_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a new task."""
    await update.message.reply_text(
        "📋 *Task Cusub*\n\n"
        "Magaca task-ka qor 👇\n"
        "/cancel si aad joojiso",
        parse_mode=ParseMode.MARKDOWN
    )
    return WAITING_TASK_NAME


async def task_receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive task name."""
    context.user_data["task_name"] = update.message.text.strip()
    await update.message.reply_text(
        f"📋 *Task:* `{context.user_data['task_name']}`\n\n"
        "Faahfaahinta task-ka qor (description) 👇\n"
        "/cancel si aad joojiso",
        parse_mode=ParseMode.MARKDOWN
    )
    return WAITING_TASK_DESC


async def task_receive_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive task description and save."""
    chat_id = update.effective_chat.id
    data = _load_data(chat_id)
    task = {
        "id": len(data["tasks"]) + 1,
        "name": context.user_data.get("task_name", "Task"),
        "desc": update.message.text.strip(),
        "created_by": update.effective_user.full_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "⚪ Cusub",
        "assigned_to": None,
    }
    data["tasks"].append(task)
    _save_data(chat_id, data)

    await update.message.reply_text(
        f"✅ *Task #{task['id']} waa la sameeyey!*\n\n"
        f"📋 `{task['name']}`\n"
        f"📝 {task['desc']}\n"
        f"👤 {task['created_by']}\n"
        f"📌 Status: {task['status']}\n\n"
        f"/task_list — dhammaan task-yada arag",
        parse_mode=ParseMode.MARKDOWN
    )
    return ConversationHandler.END


async def task_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all tasks."""
    chat_id = update.effective_chat.id
    data = _load_data(chat_id)

    if not data["tasks"]:
        await update.message.reply_text(
            "📋 *Task-yada:*\n\nWeli task ma jiraan.\n`/task_new` — task cusub samee",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    text = "━━━━━━━━━━━━━━━━━━━━━━\n"
    text += "  📋 𝐋𝐈𝐈𝐒𝐊𝐀 𝐓𝐀𝐒𝐊-𝐘𝐀𝐃𝐀\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━\n\n"

    for t in data["tasks"]:
        assign = f"👤 {t['assigned_to']}" if t['assigned_to'] else "❌ lama dhiibin"
        text += f"#{t['id']} *{t['name']}*\n"
        text += f"   📌 {t['status']} | {assign}\n"
        text += f"   📝 {t['desc'][:50]}...\n\n"

    text += "🔍 /task_done # — task dhammeystir\n"
    text += "👤 /task_assign # @username — qof u dhiib"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def task_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mark task as done."""
    try:
        args = update.message.text.split()
        task_id = int(args[1].lstrip("#"))
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Isticmaal: `/task_done #1`", parse_mode=ParseMode.MARKDOWN)
        return

    chat_id = update.effective_chat.id
    data = _load_data(chat_id)

    for t in data["tasks"]:
        if t["id"] == task_id:
            t["status"] = "✅ Dhammeystiran"
            _save_data(chat_id, data)
            await update.message.reply_text(
                f"✅ *Task #{task_id} waa la dhammeystiray!* 🎉",
                parse_mode=ParseMode.MARKDOWN
            )
            return

    await update.message.reply_text(f"❌ Task #{task_id} lama helin.", parse_mode=ParseMode.MARKDOWN)


# ═══════════════════════════════════════════════════════════════════════════════
# 💬 5. AUTO-REPLY
# ═══════════════════════════════════════════════════════════════════════════════
async def auto_reply_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set up auto-reply trigger word."""
    await update.message.reply_text(
        "💬 *Auto-Reply Setup*\n\n"
        "Erayga kicinaya (trigger) qor:\n"
        "💡 *Tusaale:* `salaan`, `waa maxay`, `hello`\n\n"
        "/cancel si aad joojiso",
        parse_mode=ParseMode.MARKDOWN
    )
    return WAITING_AUTO_TRIGGER


async def auto_reply_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save trigger word."""
    context.user_data["auto_trigger"] = update.message.text.strip().lower()
    await update.message.reply_text(
        f"🔑 Trigger: `{context.user_data['auto_trigger']}`\n\n"
        "Hadda jawaabta qor:\n"
        "💡 *Tusaale:* `Wa calaykum salaam! 👋`\n\n"
        "/cancel si aad joojiso",
        parse_mode=ParseMode.MARKDOWN
    )
    return WAITING_AUTO_REPLY


async def auto_reply_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save auto-reply pair."""
    chat_id = update.effective_chat.id
    data = _load_data(chat_id)
    trigger = context.user_data.get("auto_trigger", "")
    reply = update.message.text.strip()

    if "auto_replies" not in data:
        data["auto_replies"] = {}

    data["auto_replies"][trigger] = reply
    _save_data(chat_id, data)

    await update.message.reply_text(
        f"✅ *Auto-Reply waa la kaydiyay!*\n\n"
        f"🔑 Marka qof qoro: `{trigger}`\n"
        f"💬 Bot-ku wuxuu ku jawaabayaa: _{reply}_",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_button("menu_groups")
    )
    return ConversationHandler.END


async def auto_reply_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if message triggers auto-reply."""
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    data = _load_data(chat_id)
    text = update.message.text.strip().lower()

    for trigger, reply in data.get("auto_replies", {}).items():
        if trigger in text:
            await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
            return


# ═══════════════════════════════════════════════════════════════════════════════
# 📋 6. GROUP RULES MENU
# ═══════════════════════════════════════════════════════════════════════════════
def group_tools_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 Sharciyo Dejin", callback_data="grp_rules"),
         InlineKeyboardButton("📋 Task-yada",      callback_data="grp_tasks")],
        [InlineKeyboardButton("✅ Xaadirinta",     callback_data="grp_attendance"),
         InlineKeyboardButton("💬 Auto-Reply",     callback_data="grp_autoreply")],
        [InlineKeyboardButton("🎉 Soo dhaweyn",    callback_data="grp_welcome"),
         InlineKeyboardButton("📋 Task List",      callback_data="grp_task_list")],
        [InlineKeyboardButton("🔙 Main Menu",      callback_data="menu_main")],
    ])


async def group_tools_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show group advanced tools menu."""
    query = update.callback_query
    if query:
        await query.answer()
        target = query
    else:
        target = update.message

    text = (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "  🛠 𝐆𝐑𝐎𝐔𝐏 𝐀𝐃𝐕𝐀𝐍𝐂𝐄𝐃 𝐓𝐎𝐎𝐋𝐒\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📜 *Sharciyada* — Dejin + soo bandhig\n"
        "✅ *Xaadirinta* — Maanta yaa joogaa?\n"
        "📋 *Task-yada* — Samee, qaybi, dhammeystir\n"
        "💬 *Auto-Reply* — Erayo gaar ah jawaab toos\n"
        "🎉 *Soo dhaweyn* — Xubnaha cusub soo dhaweyn\n\n"
        "👇 Xulo hawsha:"
    )
    if hasattr(target, 'edit_message_text'):
        await target.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=group_tools_menu())
    else:
        await target.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=group_tools_menu())
