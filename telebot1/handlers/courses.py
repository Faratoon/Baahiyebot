"""
handlers/courses.py  –  Course browser — 40 cashar oo dhammaystiran
"""
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.menus import courses_main_menu, course_list_menu, back_button

# Load courses
COURSES_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "courses.json")
COURSES = []

def load_courses():
    global COURSES
    try:
        with open(COURSES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Flatten all lessons from all courses into one list
            all_lessons = []
            for course in data.get("courses", []):
                course_name = course.get("name", "Course")
                for lesson in course.get("lessons", []):
                    lesson["course_name"] = course_name
                    all_lessons.append(lesson)
            COURSES = all_lessons
    except Exception:
        COURSES = []

load_courses()

PAGE_SIZE = 10  # 10 lessons per page = 4 pages for 40 lessons


async def courses_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main courses menu."""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            "📚 *Courses* — Xulo:\n\n"
            "• 🔍 Raadi cashar\n"
            "• 📋 Daalaco dhammaan 40 cashar\n"
            "• 🤖 Weydii AI-ga koorsada",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=courses_main_menu()
        )
    else:
        await update.message.reply_text(
            "📚 *Courses* — Xulo:\n\n"
            "• 🔍 Raadi cashar\n"
            "• 📋 Daalaco dhammaan 40 cashar\n"
            "• 🤖 Weydii AI-ga koorsada",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=courses_main_menu()
        )


async def course_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show paginated course list."""
    query = update.callback_query
    await query.answer()

    # Get current page from callback or default 0
    page = 0
    if query.data.startswith("course_page_"):
        page = int(query.data.split("_")[2])

    if not COURSES:
        load_courses()
    if not COURSES:
        await query.edit_message_text(
            "❌ Courses not found. Please check data/courses.json",
            reply_markup=back_button("menu_courses")
        )
        return

    # Get courses for this page
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_courses = COURSES[start:end]

    text = f"📚 *Lessons {start+1}–{min(end, len(COURSES))} of {len(COURSES)}*\n\n"
    btn_rows = []

    for i, course_data in enumerate(page_courses):
        num = start + i + 1
        title = course_data.get("title", f"Lesson {num}")
        text += f"*{num}.* {title}\n"

    text += "\n🔽 Click a number below to view:"

    # Add number buttons in rows of 5
    num_buttons = []
    for i, course_data in enumerate(page_courses):
        idx = start + i
        num_buttons.append(
            InlineKeyboardButton(str(idx + 1), callback_data=f"course_view_{idx}")
        )
    # Group in rows of 5
    for i in range(0, len(num_buttons), 5):
        btn_rows.append(num_buttons[i:i + 5])

    # Prev/Next
    total_pages = (len(COURSES) + PAGE_SIZE - 1) // PAGE_SIZE
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"course_page_{page-1}"))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("➡️ Next", callback_data=f"course_page_{page+1}"))
    if nav_row:
        btn_rows.append(nav_row)

    btn_rows.append([InlineKeyboardButton("🔍 Search", callback_data="course_search")])
    btn_rows.append([InlineKeyboardButton("🔙 Courses Menu", callback_data="menu_courses")])

    await query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(btn_rows)
    )


async def course_view_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show a single lesson."""
    query = update.callback_query
    await query.answer()

    idx = int(query.data.split("_")[2])
    if not COURSES:
        load_courses()

    if idx >= len(COURSES):
        await query.edit_message_text("❌ Lesson not found.", reply_markup=back_button("menu_courses"))
        return

    lesson = COURSES[idx]
    num = idx + 1
    title = lesson.get("title", "No title")
    desc = lesson.get("description", "")
    link = lesson.get("link", "")
    course_name = lesson.get("course_name", "AI Automation Course")

    text = (
        f"📚 *Lesson {num}: {title}*\n\n"
        f"📖 *Course:* {course_name}\n"
        f"{'─' * 30}\n"
        f"{desc}\n\n"
        f"🔗 [👉 Watch Lesson {num} on YouTube]({link})"
    )

    btns = [
        [InlineKeyboardButton("▶️ Watch on YouTube", url=link)] if link else [],
        [InlineKeyboardButton("⬅️ Back to List", callback_data="course_list"),
         InlineKeyboardButton("🔙 Courses", callback_data="menu_courses")],
    ]
    btns = [row for row in btns if row]  # Remove empty rows

    await query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False,
        reply_markup=InlineKeyboardMarkup(btns)
    )


async def course_search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask user for search query."""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            "🔍 *Search Lessons*\n\n"
            "Waxaad raadinayso erayn qor:\n"
            "✏️ Tusaale: `chatbot`, `AI`, `n8n`, `Linux`\n\n"
            "Fadlan erayga qor hoos 👇",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Cancel", callback_data="menu_courses")]
            ])
        )
    context.user_data["awaiting_course_search"] = True


async def course_search_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle search query text and show results."""
    query_text = update.message.text.lower()
    if not COURSES:
        load_courses()

    matches = []
    for i, lesson in enumerate(COURSES):
        title = lesson.get("title", "").lower()
        desc = lesson.get("description", "").lower()
        if query_text in title or query_text in desc:
            matches.append((i, lesson))

    if not matches:
        await update.message.reply_text(
            f"❌ Waxba looma helin '{query_text}'.\n\n"
            f"Erayo kale isku day: `chatbot`, `n8n`, `AI`, `Linux`, `WhatsApp`, `Bot`",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_button("menu_courses")
        )
        return

    text = f"🔍 *Search Results for '{query_text}'* ({len(matches)} found)\n\n"
    btns = []
    for idx, lesson in matches:
        num = idx + 1
        title = lesson.get("title", f"Lesson {num}")
        text += f"*{num}.* {title}\n"
        btns.append([InlineKeyboardButton(f"📖 {num}. {title[:30]}", callback_data=f"course_view_{idx}")])

    btns.append([InlineKeyboardButton("🔙 Courses Menu", callback_data="menu_courses")])

    await update.message.reply_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(btns)
    )


async def course_ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set AI mode to course-specific."""
    query = update.callback_query
    if query:
        await query.answer()

    context.user_data["ai_model"] = "meta-llama/llama-3.1-8b-instruct:free"
    context.user_data["ai_model_name"] = "📚 Course AI"
    context.user_data["ai_mode"] = True

    text = (
        "🤖 *Course AI Agent Active!*\n\n"
        "Wax kasta oo ku saabsan koorsooyinka weydii:\n"
        "• \"Chatbot-ka maxaan ka bari karaa?\"\n"
        "• \"n8n casharka sidee buu u yahay?\"\n"
        "• \"Casharka 15 waa maxay?\"\n"
        "• \"Waxa baro AI Automation\"\n\n"
        "Wax kasta oo aad waydid, bot-ku wuxuu ku tusayaa casharka ugu habboon! 🔍"
    )

    if query:
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def support_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        target = query
    else:
        target = update.message

    text = (
        "👨‍💻 *Talk to a Person / Support*\n\n"
        "📞 Telegram: @Mfaratoon\n"
        "🌐 Website: https://hibomusic.com\n"
        "📺 YouTube: https://m.youtube.com/user/MrFaraton\n"
        "📢 Telegram: https://t.me/Farsamada\n\n"
        "⏰ Response time: Usually within a few hours\n"
        "🌍 Languages: Somali, Arabic, English"
    )
    if hasattr(target, 'edit_message_text'):
        await target.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_button())
    else:
        await target.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_button())


async def info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        target = query
    else:
        target = update.message

    text = (
        "❓ *Bot Information*\n\n"
        "🤖 *Mfaratoon AI Bot — All-in-One*\n\n"
        "📢 **Features:**\n"
        "• Multi-channel & group management\n"
        "• AI assistant (Somali/Arabic/English)\n"
        "• 40+ FREE AI courses\n"
        "• Schedule & auto-post\n"
        "• Welcome messages\n\n"
        "📞 Support: @Mfaratoon\n"
        "📺 YouTube: MrFaraton\n\n"
        "💡 /help si aad dhammaan commands-ka u aragto"
    )
    if hasattr(target, 'edit_message_text'):
        await target.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_button())
    else:
        await target.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_button())
