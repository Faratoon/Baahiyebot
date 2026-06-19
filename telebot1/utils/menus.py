"""
utils/menus.py  –  ONE BIG MAIN MENU — No more sub-menus!
Dhammaan featur-yada hal menu oo weyn ayay ku wada jiraan.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


# ── MAIN MENU (Reply Keyboard) — SIMPLE: 2 rows only ─────────────────────────
def main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton("📢 Channels/Groups"),
            KeyboardButton("📚 Courses"),
            KeyboardButton("🤖 AI Chat"),
        ],
        [
            KeyboardButton("👤 Profile"),
            KeyboardButton("📞 Support"),
            KeyboardButton("📌 Menu"),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


# ── SIMPLE INLINE MENU (for /menu command — same buttons) ────────────────────
def main_inline_menu() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("📢 Channels",  callback_data="menu_channels"),
            InlineKeyboardButton("👥 Groups",    callback_data="menu_groups"),
            InlineKeyboardButton("📤 Broadcast", callback_data="menu_broadcast"),
        ],
        [
            InlineKeyboardButton("⏰ Schedule", callback_data="menu_schedule"),
            InlineKeyboardButton("🤖 AI Chat",  callback_data="menu_ai"),
            InlineKeyboardButton("📚 Courses",  callback_data="menu_courses"),
        ],
        [
            InlineKeyboardButton("👤 Profile",  callback_data="menu_profile"),
            InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings"),
            InlineKeyboardButton("📞 Support",  callback_data="menu_support"),
        ],
        [
            InlineKeyboardButton("☘️ Learn AI",  callback_data="menu_learn"),
            InlineKeyboardButton("❓ Help",      callback_data="menu_info"),
            InlineKeyboardButton("🔄 Clear Mem", callback_data="set_clear_mem"),
        ],
        [
            InlineKeyboardButton("🌐 WebApp", url="https://webapp-zeta-flame-84.vercel.app"),
            InlineKeyboardButton("🌐 Website", url="https://hibomusic.com"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


# ── Channel ACTIONS (no sub-menu, just action buttons) ────────────────────────
def channel_actions() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Channel",  callback_data="ch_add"),
         InlineKeyboardButton("📋 My Channels", callback_data="ch_list")],
        [InlineKeyboardButton("📤 Post to All",  callback_data="ch_post_all"),
         InlineKeyboardButton("✏️ Edit Post",    callback_data="ch_edit")],
        [InlineKeyboardButton("🗑️ Delete Post", callback_data="ch_delete"),
         InlineKeyboardButton("🔙 Main Menu",    callback_data="menu_main")],
    ])


# ── Group ACTIONS ─────────────────────────────────────────────────────────────
def group_actions() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Group",   callback_data="grp_add"),
         InlineKeyboardButton("📋 My Groups",  callback_data="grp_list")],
        [InlineKeyboardButton("📤 Post to All", callback_data="grp_post_all"),
         InlineKeyboardButton("🎉 Welcome Msg", callback_data="grp_welcome")],
        [InlineKeyboardButton("🔙 Main Menu",   callback_data="menu_main")],
    ])


# ── BROADCAST (inline) ────────────────────────────────────────────────────────
def broadcast_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Channels", callback_data="bc_channels"),
         InlineKeyboardButton("👥 Groups",   callback_data="bc_groups")],
        [InlineKeyboardButton("🌐 All",      callback_data="bc_all")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")],
    ])


# ── AI MODELS ─────────────────────────────────────────────────────────────────
def ai_models_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("💬 Nano Banana",    callback_data="ai_nano"),
         InlineKeyboardButton("🎨 Midjourney",     callback_data="ai_midjourney")],
        [InlineKeyboardButton("🖼️ Sora Images",    callback_data="ai_sora"),
         InlineKeyboardButton("🤖 GPT Images",     callback_data="ai_gpt_image")],
        [InlineKeyboardButton("🎨 Flux Images",    callback_data="ai_flux"),
         InlineKeyboardButton("🎥 Veo3 Video",     callback_data="ai_veo")],
        [InlineKeyboardButton("💬 General Chat",   callback_data="ai_chat")],
        [InlineKeyboardButton("🔙 Main Menu",      callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(buttons)


# ── COURSES BROWSER ───────────────────────────────────────────────────────────
def courses_main_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("🔍 Search Lesson",    callback_data="course_search")],
        [InlineKeyboardButton("📋 All 40 Lessons",   callback_data="course_list")],
        [InlineKeyboardButton("🤖 Course AI Agent",  callback_data="course_ask")],
        [InlineKeyboardButton("🔙 Main Menu",        callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(buttons)


def course_list_menu(page: int = 0, total_pages: int = 4) -> InlineKeyboardMarkup:
    """Paginated course list with prev/next."""
    btns = []
    if page > 0:
        btns.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"course_page_{page-1}"))
    if page < total_pages - 1:
        btns.append(InlineKeyboardButton("➡️ Next", callback_data=f"course_page_{page+1}"))
    row = btns if btns else []
    buttons = [row] if row else []
    buttons.append([InlineKeyboardButton("🔍 Search", callback_data="course_search")])
    buttons.append([InlineKeyboardButton("🔙 Courses Menu", callback_data="menu_courses")])
    return InlineKeyboardMarkup(buttons)


# ── PROFILE ───────────────────────────────────────────────────────────────────
def profile_menu(is_prem: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("📊 My Stats",     callback_data="prof_stats")],
        [InlineKeyboardButton("📋 My Channels",   callback_data="prof_mychannels")],
        [InlineKeyboardButton("🗓️ Scheduled",    callback_data="prof_scheduled")],
    ]
    if not is_prem:
        buttons.append([InlineKeyboardButton("⭐ Upgrade to Premium", callback_data="prof_upgrade")])
    else:
        buttons.append([InlineKeyboardButton("👑 Premium Active ✅", callback_data="prof_premium_info")])
    buttons.append([InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)


# ── SETTINGS ──────────────────────────────────────────────────────────────────
def settings_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("🌐 Language",        callback_data="set_lang")],
        [InlineKeyboardButton("🔔 Notifications",   callback_data="set_notif")],
        [InlineKeyboardButton("🗑️ Clear AI Memory", callback_data="set_clear_mem")],
        [InlineKeyboardButton("📝 Welcome Message",  callback_data="set_welcome")],
        [InlineKeyboardButton("🔙 Main Menu",        callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(buttons)


# ── ADMIN PANEL ───────────────────────────────────────────────────────────────
def admin_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("📊 Stats",          callback_data="adm_stats")],
        [InlineKeyboardButton("📢 Broadcast",      callback_data="adm_broadcast")],
        [InlineKeyboardButton("⭐ Grant Premium",  callback_data="adm_premium")],
        [InlineKeyboardButton("🚫 Ban User",       callback_data="adm_ban")],
        [InlineKeyboardButton("🔙 Main Menu",      callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(buttons)


# ── CONFIRM / CANCEL ──────────────────────────────────────────────────────────
def confirm_cancel(confirm_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Confirm", callback_data=confirm_data),
         InlineKeyboardButton("❌ Cancel",  callback_data="action_cancel")],
    ])


def back_button(data: str = "menu_main") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Main Menu", callback_data=data)]])
