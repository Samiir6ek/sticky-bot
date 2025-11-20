# Explanation for Samir:
# This file holds all the text for the bot in different languages.
# Using a file like this for text makes the bot easier to manage.
# If you want to change a message, you only have to change it here, not in the main bot.py code.
#
# How it works:
# - 'TEXT' is a big dictionary.
# - The first level of keys are the language codes: 'en' (English), 'uz' (Uzbek), 'ru' (Russian).
# - The second level of keys are identifiers for each message, like 'welcome' or 'ask_nickname'.
# - The bot will look up the text like this: TEXT[user_language][message_key]

TEXT = {
    'en': {
        'welcome': "👋 Hello! I'm the official bot of the _Sticky_Online_Store_.\n\n" \
                   "To celebrate our launch, we're giving away a **FREE** tribe sticker to every student at school 21!\n\n" \
                   "Please select your language to continue.",
        'lang_selected': "Language set to **English**.",
        'ask_subscribe': "Great! To get your free sticker, you first need to be a member of our channel. " \
                         "Please subscribe and then click the button below to confirm.",
        'channel_button': "Go to Channel",
        'confirm_button': "✅ I have subscribed",
        'not_subscribed': "⚠️ You haven't subscribed to the channel yet. Please subscribe to proceed.",
        'already_registered': "You have already registered for a free sticker! Your order is being prepared.",
        'ask_nickname': "✅ Subscription confirmed!\n\nLet's get you registered. What is your **nickname/login** at school 21?:",
        'invalid_nickname': "⚠️ **Invalid Nickname**\n\nWe couldn't find the nickname `{nickname}` in the school's database. Please check for typos and try again.",
        'ask_real_name': "✅ Nickname `{nickname}` verified!\n\nNow, please enter your **name** (e.g., John): This will be used to verify your identity when you pick up the sticker.",
        'ask_stage': "Got it, `{nickname}`! Now, please select your **stage**.",
        'intensive_button': "🚀 Intensive",
        'core_button': "🌱 Core",
        'ask_tribe': "Perfect! Now select your **tribe**.",
        'registration_complete': "🎉 **Registration Complete!**\n\nYou're all set. Now you can choose the logo for your free sticker.",
        # Sticker placeholder
        'sticker_placeholder_after_reg': "STICKER_PLACEHOLDER_YAY",
        'ask_logo_stage': "Which stage's logos would you like to choose from?",
        'ask_logo_tribe': "Please choose a logo for your sticker.",
        'order_complete': "✅ **Order Confirmed!**\n\nYour `{chosen_logo}` sticker is confirmed. " \
                        "The order will be available in volunteers room from 26th november and you can pick it up from there any time you want!\n\n" \
                        "Thank you for participating!",
        'admin_notification': "🔔 **New Sticker Order**\n\n" \
                              "**User ID:** `{user_id}`\n" \
                              "**Username:** @{username}\n" \
                              "**Language:** `{lang}`\n\n" \
                              "--- Registration ---\n" \
                              "**Nickname:** `{nickname}`\n" \
                              "**Real Name:** `{real_name}`\n" \
                              "**Stage:** `{stage}`\n" \
                              "**Tribe:** `{tribe}`\n\n" \
                              "--- Order ---\n" \
                              "**Chosen Logo:** `{chosen_logo}`",
        'advertisement': "🔥 **Want a sticker with YOUR nickname on it?** 🔥\n\n" \
                         "It's the ultimate custom sticker that no one else has!\n\n" \
                         "**SPECIAL OFFER:**\n" \
                         "➡️ Buy **10** custom stickers of your choice, and get **1** FREE nickname sticker.\n" \
                         "➡️ Buy **20** custom stickers, and get **2** FREE nickname stickers!\n\n" \
                         "Just send me the 10-20 images you want, tell me the sizes, and I'll handle the rest.\n\n" \
                         "You can also get an **EXTRA FREE** sticker by sharing a post from our channel to your story! " \
                         "Click the buttons below to start a custom order or get your bonus sticker.",
        'contact_me_button': "💬 Contact Samir",
        'get_bonus_button': "✨ Get Bonus Sticker",
        'fallback_message': "Sorry, I didn't understand that. Please use the buttons or follow the instructions.",
        'bonus_instructions': "Great! To get an extra FREE sticker, share *any* post from our @sticky_online_store channel to your Telegram (or Instagram) story for 24 hours. Once it's live, **download the image of your story** and send it back to me here as proof!",
        'bonus_confirmation': "Thank you for sharing! We've received your story proof. Your special bonus sticker has been added to your order! 🎉",
        'admin_bonus_caption': "✅ **Bonus Sticker Proof**\n\nUser: @{username}\nNickname/Login: {nickname}\nName: {real_name}\n\nPlease verify their story."
    },
    'uz': {
        'welcome': "👋 Salom! Men **sticky_online_store**'ning rasmiy botiman.\n\n" \
                   "Ochilishimiz munosabati bilan biz 21-maktabning har bir o'quvchisiga **BEPUL** tribe stikerini sovg'a qilamiz!\n\n" \
                   "Davom etish uchun, iltimos, tilingizni tanlang.",
        'lang_selected': "Til **O'zbekcha** qilib o'rnatildi.",
        'ask_subscribe': "Ajoyib! Bepul stikeringizni olish uchun avval bizning kanalimizga a'zo bo'lishingiz kerak. " \
                         "Iltimos, obuna bo'ling va tasdiqlash uchun quyidagi tugmani bosing.",
        'channel_button': "Kanalga o'tish",
        'confirm_button': "✅ Obuna bo'ldim",
        'not_subscribed': "⚠️ Siz hali kanalga obuna bo'lmagansiz. Davom etish uchun obuna bo'ling.",
        'already_registered': "Siz allaqachon bepul stiker uchun ro'yxatdan o'tgansiz! Buyurtmangiz tayyorlanmoqda.",
        'ask_nickname': "✅ Obuna tasdiqlandi!\n\nKeling, sizni ro'yxatdan o'tkazamiz. 21-maktabdagi **nikneym/login** nima?:",
        'invalid_nickname': "⚠️ **Noto'g'ri Nikneym**\n\n`{nickname}` nikneymi maktab ma'lumotlar bazasidan topilmadi. Iltimos, xatoliklarni tekshiring va qaytadan urunib ko'ring.",
        'ask_real_name': "✅ `{nickname}` nikneymi tasdiqlandi!\n\nEndi, iltimos, **ismingizni** kiriting (masalan, Aziz): Bu ma'lumot stikerni olayotganingizda shaxsingizni tasdiqlash uchun ishlatiladi.",
        'ask_stage': "Tushunarli, `{nickname}`! Endi, iltimos, o'z **bosqichingizni** tanlang.",
        'intensive_button': "🚀 Intensive",
        'core_button': "🌱 Core",
        'ask_tribe': "A'lo! Endi o'z **qabilangizni** tanlang.",
        'registration_complete': "🎉 **Ro'yxatdan o'tish yakunlandi!**\n\nEndi bepul stikeringiz uchun logotipni tanlashingiz mumkin.",
        'sticker_placeholder_after_reg': "STICKER_PLACEHOLDER_YAY_UZ",
        'ask_logo_stage': "Qaysi bosqich trayb logotiplaridan tanlamoqchisiz?",
        'ask_logo_tribe': "Iltimos, stikeringiz uchun logotip tanlang.",
        'order_complete': "✅ **Buyurtma tasdiqlandi!**\n\nSizning `{chosen_logo}` stikeringiz tasdiqlandi. " \
                        "Buyurtma 26-noyabrdan boshlab volonterlar xonasida bo'ladi va uni xohlagan vaqtda olib ketishingiz mumkin!\n\n" \
                        "Ishtirokingiz uchun rahmat!",
        'admin_notification': "🔔 **Yangi stiker buyurtmasi**\n\n" \
                              "**Foydalanuvchi ID'si:** `{user_id}`\n" \
                              "**Username:** @{username}\n" \
                              "**Til:** `{lang}`\n\n" \
                              "--- Ro'yxatdan o'tish ---\n" \
                              "**Nikneym:** `{nickname}`\n" \
                              "**Haqiqiy Ism:** `{real_name}`\n" \
                              "**Bosqich:** `{stage}`\n" \
                              "**Qabila:** `{tribe}`\n\n" \
                              "--- Buyurtma ---\n" \
                              "**Tanlangan logo:** `{chosen_logo}`",
        'advertisement': "🔥 **O'Z nikneymingiz tushirilgan stiker xohlaysizmi?** 🔥\n\n" \
                         "Bu hech kimda yo'q, noyob stiker!\n\n" \
                         "**MAXSUS TAKLIF:**\n" \
                         "➡️ O'zingiz tanlagan **10** ta stikerga buyurtma bering va **1** ta BEPUL nikneym stikerini qo'lga kiriting.\n" \
                         "➡️ **20** ta stikerga buyurtma bering va **2** ta BEPUL nikneym stikerini oling!\n\n" \
                         "Menga 10-20 ta xohlagan rasmingizni yuboring, o'lchamlarini ayting, qolganini o'zim hal qilaman.\n\n" \
                         "Shuningdek, kanalimizdan biror postni hikoyangizda ulashib, **QO'SHIMCHA BEPUL** stiker olishingiz mumkin! " \
                         "Maxsus buyurtma berish yoki bonus stikerni olish uchun quyidagi tugmalarni bosing.",
        'contact_me_button': "💬 Samir bilan bog'lanish",
        'get_bonus_button': "✨ Bonus stikerini olish",
        'fallback_message': "Kechirasiz, men buni tushunmadim. Iltimos, tugmalardan foydalaning yoki ko'rsatmalarga amal qiling.",
        'bonus_instructions': "Ajoyib! Qo'shimcha BEPUL stiker olish uchun, @sticky_online_store kanalimizdagi *istalgan* xabarni 24 soat davomida Telegram (yoki Instagram) hikoyangizda ulashing. U nashr qilingandan so'ng, **hikoyangiz rasmini yuklab oling** va menga dalil sifatida yuboring!",
        'bonus_confirmation': "Ulashingiz uchun rahmat! Hikoyangiz tasdig'ini oldik. Maxsus bonus stikeringiz buyurtmangizga qo'shildi! 🎉",
        'admin_bonus_caption': "✅ **Bonus stiker tasdig'i**\n\nFoydalanuvchi: @{username}\nNikneym/Login: {nickname}\nIsm: {real_name}\n\nIltimos, hikoyasini tekshiring."
    },
    'ru': {
        'welcome': "👋 Привет! Я официальный бот **sticky_online_store**.\n\n" \
                   "В честь нашего запуска мы дарим **БЕСПЛАТНЫЙ** стикер с логотипом твоего трайба каждому студенту школы 21!\n\n" \
                   "Пожалуйста, выберите ваш язык для продолжения.",
        'lang_selected': "Язык установлен на **Русский**.",
        'ask_subscribe': "Отлично! Чтобы получить бесплатный стикер, вам нужно быть участником нашего канала. " \
                         "Пожалуйста, подпишитесь, а затем нажмите кнопку ниже для подтверждения.",
        'channel_button': "Перейти на канал",
        'confirm_button': "✅ Я подписался",
        'not_subscribed': "⚠️ Вы еще не подписались на канал. Пожалуйста, подпишитесь, чтобы продолжить.",
        'already_registered': "Вы уже зарегистрировались на получение бесплатного стикера! Ваш заказ готовится.",
        'ask_nickname': "✅ Подписка подтверждена!\n\nДавайте вас зарегистрируем. Какой у вас **никнейм/логин** в школе 21?:",
        'invalid_nickname': "⚠️ **Неверный Никнейм**\n\nНикнейм `{nickname}` не найден в базе данных школы. Пожалуйста, проверьте правильность написания и попробуйте снова.",
        'ask_real_name': "✅ Никнейм `{nickname}` подтвержден!\n\nТеперь, пожалуйста, введите ваше **имя** (например, Иван): Это имя будет использоваться для подтверждения вашей личности при получении стикера.",
        'ask_stage': "Понял, `{nickname}`! Теперь, пожалуйста, выберите ваш **этап**.",
        'intensive_button': "🚀 Интенсив",
        'core_button': "🌱 Основа",
        'ask_tribe': "Прекрасно! Теперь выберите ваш **трайб**.",
        'registration_complete': "🎉 **Регистрация завершена!**\n\nТеперь вы можете выбрать логотип для вашего бесплатного стикера.",
        'sticker_placeholder_after_reg': "STICKER_PLACEHOLDER_YAY_RU",
        'ask_logo_stage': "Логотипы какого этапа вы бы хотели выбрать?",
        'ask_logo_tribe': "Пожалуйста, выберите логотип для вашего стикера.",
        'order_complete': "✅ **Заказ подтвержден!**\n\nВаш стикер «{chosen_logo}» подтвержден. " \
                        "Заказ будет доступен в комнате волонтеров с 26 ноября, и вы сможете забрать его оттуда в любое удобное для вас время!\n\n" \
                        "Спасибо за участие!",
        'admin_notification': "🔔 **Новый заказ на стикер**\n\n" \
                              "**ID пользователя:** `{user_id}`\n" \
                              "**Имя пользователя:** @{username}\n" \
                              "**Язык:** `{lang}`\n\n" \
                              "--- Регистрация ---\n" \
                              "**Никнейм:** `{nickname}`\n" \
                              "**Полное Имя:** `{real_name}`\n" \
                              "**Этап:** `{stage}`\n" \
                              "**Трайб:** `{tribe}`\n\n" \
                              "--- Заказ ---\n" \
                              "**Выбранный логотип:** `{chosen_logo}`",
        'advertisement': "🔥 **Хотите стикер с ВАШИМ никнеймом?** 🔥\n\n" \
                         "Это уникальный кастомный стикер, которого нет больше ни у кого!\n\n" \
                         "**СПЕЦИАЛЬНОЕ ПРЕДЛОЖЕНИЕ:**\n" \
                         "➡️ Купите **10** любых стикеров на ваш выбор и получите **1** БЕСПЛАТНЫЙ стикер с никнеймом.\n" \
                         "➡️ Купите **20** стикеров и получите **2** БЕСПЛАТНЫХ стикера с никнеймом!\n\n" \
                         "Просто пришлите мне 10-20 изображений, которые вы хотите, укажите размеры, а я займусь остальным.\n\n" \
                         "Вы также можете получить **ДОПОЛНИТЕЛЬНЫЙ БЕСПЛАТНЫЙ** стикер, поделившись постом из нашего канала в своей истории! " \
                         "Нажмите кнопки ниже, чтобы начать индивидуальный заказ или получить бонусный стикер.",
        'contact_me_button': "💬 Связаться с Самиром",
        'get_bonus_button': "✨ Получить бонусный стикер",
        'fallback_message': "Извините, я не понял. Пожалуйста, используйте кнопки или следуйте инструкциям.",
        'bonus_instructions': "Отлично! Чтобы получить дополнительный БЕСПЛАТНЫЙ стикер, поделитесь *любым* постом из нашего канала @sticky_online_store в своей истории Telegram (или Instagram) на 24 часа. Как только он будет опубликован, **скачайте изображение вашей истории** и отправьте его мне сюда в качестве подтверждения!",
        'bonus_confirmation': "Спасибо за то, что поделились! Мы получили подтверждение вашей истории. Ваш специальный бонусный стикер добавлен к вашему заказу! 🎉",
        'admin_bonus_caption': "✅ **Подтверждение бонусного стикера**\n\nПользователь: @{username}\nНикнейм/Логин: {nickname}\nИмя: {real_name}\n\nПожалуйста, проверьте его историю."
    }
}

# Explanation for Samir:
# These are the names of the tribes for each stage.
# We define them here so we can easily use them to create buttons in the bot.
TRIBES = {
    'intensive': ['Ayiq', 'Jayron', 'Laylak', 'Qoplon'],
    'core': ['Pegasus', 'Phoenix', 'Minotaur', 'Dragon']
}