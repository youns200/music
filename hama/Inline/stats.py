from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

stats1 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="ئاماری System", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="ئاماری Storage", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری Bot", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="MongoDB ئاماری", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری Assistant", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="ئاماری گشتی", callback_data=f"gen_stats"
            ),
            InlineKeyboardButton(
                text="ئاماری خەزنکردن", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری بۆت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="ئاماری سرێڤەر", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری یارمەتی دەر", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats3 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="ئاماری سیستەم", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="ئاماری گشتی", callback_data=f"gen_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری بۆت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="ئاماری سرێڤەر", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری یارمەتی دەر", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats4 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="ئاماری سیستەم", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="ئاماری خەزنکردن", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری گشتی", callback_data=f"gen_stats"
            ),
            InlineKeyboardButton(
                text="ئاماری سرێڤەر", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری یارمەتی دەر", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats5 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="ئاماری سیستەم", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="ئاماری خەزنکردن", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری بۆت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="ئاماری گشتی", callback_data=f"gen_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری یارمەتی دەر", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats6 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="ئاماری سیستەم", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="ئاماری خەزنکردن", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری بۆت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="ئاماری سرێڤەر", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ئاماری گشتی", callback_data=f"gen_stats"
            )
        ],
    ]
)


stats7 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="بەدەستهێنانی ئاماری گشتی....",
                callback_data=f"wait_stats",
            )
        ]
    ]
)
