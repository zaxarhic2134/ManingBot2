from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.models import Profile
from bot.models import ProfileSettings
from bot.management.commands import binanceapi

class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(
            token=settings.TOKEN
        )
        print(bot.get_me())

        @bot.message_handler(commands=['start'])
        def get_user_info(message):
            user_id = message.chat.id
            p, _= Profile.objects.get_or_create(
                external_id=user_id,
                defaults={
                    'name': message.from_user.username
                }
            )
            ProfileSettings.objects.get_or_create(
                external=p,
            )
            bot.send_message(message.chat.id, 'Для продолжения работы создайте API ключи Binance, '
                                              'только с включенным режимом чтения!\n'
                                              'Это необходимо для '
                                              'вашей безопасности!')
            msg=bot.send_message(message.chat.id,"Отправьте API ключ:")
            bot.register_next_step_handler(msg, get_api_key)

        def get_api_key(message):
            api_key=message.text
            user_id=message.chat.id
            ProfileSettings.objects.filter(external_id=user_id).update(api_key=api_key)
            msg=bot.send_message(message.chat.id,'Замечательно! Теперь пришлите мне секретный ключ:')
            bot.register_next_step_handler(msg, get_secret_api_key)

        def get_secret_api_key(message):
            secret_api_key=message.text
            user_id=message.chat.id
            ProfileSettings.objects.filter(external_id=user_id).update(secret_key=secret_api_key)
            status = binanceapi.account_status(user_id)
            if status=='Normal':
                bot.send_message(user_id, 'API-ключи успешно введены!'
                                          'Для продолжения введите /pool')
            else:
                markup = types.InlineKeyboardMarkup(row_width=2)
                again_button= types.InlineKeyboardButton(text='Попробовать снова', callback_data='again_main')
                markup.row(again_button)
                bot.send_message(message.chat.id,'Ошибка! Ключи введены не верно, попробуйте снова.',
                                 reply_markup=markup)

        @bot.message_handler(commands=['api'])
        def swap(message):
            msg = bot.send_message(message.chat.id, "Отправьте API ключ:")
            bot.register_next_step_handler(msg, get_api_key)

        @bot.message_handler(commands=['sub'])
        def choise_sub_account_address(message):
            user_id=message.chat.id
            emails = binanceapi.get_subaccount_address(user_id)
            numbers = len(emails)
            emails_data = emails[0:numbers]
            email_kb = InlineKeyboardMarkup()
            email_kb.row_width = 2
            for numbers, emails_data in enumerate(emails_data):
                email_kb.add(InlineKeyboardButton(text=emails_data, callback_data=emails_data))
            bot.send_message(message.chat.id, "Выбирите почту Суб-Аккаунта "
                                              "для доступа к некоторым функциям"
                                              " либо для смены аккаунта", reply_markup=email_kb)

        @bot.message_handler(commands=['profit'])
        def get_profit(message):
            user_id=message.chat.id
            try:
                bot.send_message(message.chat.id, binanceapi.today_profit(user_id))
            except:
                bot.send_message(message.chat.id, 'У вас нет доступа к данной команде, '
                                                  'поскольку не введены необходимые данные!')

        @bot.message_handler(commands=['balance'])
        def get_balance(message):
            try:
                if binanceapi.balance(message.chat.id)!='':
                    bot.send_message(message.chat.id, binanceapi.balance(message.chat.id))
                else:
                    bot.send_message(message.chat.id, 'На счету нет доступных средств.')
            except:
                bot.send_message(message.chat.id, 'У вас нет доступа к данной команде, '
                                                  'либо на счету отсутствуют средства!')

        @bot.message_handler(commands=['address'])
        def get_address(message):
            try:
                bot.send_message(message.chat.id, binanceapi.get_address_usdt())
            except:
                bot.send_message(message.chat.id, 'У вас нет доступа к данной команде, '
                                                  'поскольку не введены необходимые данные!')

        @bot.message_handler(commands=['profitability'])
        def get_profitability(message):
            user_id = message.chat.id
            try:
                bot.send_message(message.chat.id, binanceapi.get_profitability(user_id))
            except:
                bot.send_message(message.chat.id, 'У вас нет доступа к данной команде, '
                                                  'поскольку не введены необходимые данные!')

        @bot.message_handler(commands=['workers'])
        def get_workers(message):
            bot.send_message(message.chat.id, "Состояние каких воркеров вы хотите узнать:",
                             reply_markup=get_worker_keyboard())

        def get_worker_keyboard():
            markup = types.InlineKeyboardMarkup(row_width=2)
            eth_button = types.InlineKeyboardButton(text='ETH', callback_data='eth')
            btc_button = types.InlineKeyboardButton(text='BTC', callback_data='btc')
            return markup.row(eth_button, btc_button)

        @bot.message_handler(commands=['pool'])
        def pool(message):
            msg = bot.send_message(message.chat.id, 'Введите логин pool-аккаунта')
            bot.register_next_step_handler(msg, pool_check)


        def pool_check(message):
            username=message.text
            user_id=message.chat.id
            status = binanceapi.get_pool_address(user_id, username)
            if status=='ok':
                ProfileSettings.objects.filter(external_id=user_id).update(pool_username=username)
                bot.send_message(message.chat.id, 'Данные профиля введены верно'
                                                  'Для продолжения введите /sub')
            else:
                markup = types.InlineKeyboardMarkup(row_width=1)
                again_button = types.InlineKeyboardButton(text='Попробовать снова', callback_data='again_pool')
                markup.row(again_button)
                bot.send_message(message.chat.id, 'Ошибка! Данный аккаунт не найден в системе. '
                                                  'Попробуйте ввести снова', reply_markup=markup)


        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            if call.message:
                if call.data == "eth":
                    try:
                        worker_status = binanceapi.info_workers(algo="ethash", user_id=call.message.chat.id)
                        bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          text="Список майнеров и их состояния: \n"
                                               + '\n'.join(worker_status))
                    except:
                        bot.edit_message_text(chat_id=call.message.chat.id,
                                              message_id=call.message.message_id,
                                              text='Ошибка!Устройства не обнаружены')
                elif call.data == "btc":
                    try:
                        worker_status = binanceapi.info_workers(algo="sha256", user_id=call.message.chat.id)
                        bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          text="Список майнеров и их состояния: \n"
                                               + '\n'.join(worker_status))
                    except:
                        bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          text='Ошибка!Устройства не обнаружены')
                elif call.data == "again_main":
                    msg=bot.send_message(call.message.chat.id,'Введите API ключи:')
                    bot.register_next_step_handler(msg, get_api_key)
                elif call.data == "again_pool":
                    msg=bot.send_message(call.message.chat.id,'Введите логин вашего pool-аккаунта')
                    bot.register_next_step_handler(msg, pool_check)
                elif call.data in binanceapi.get_subaccount_address(call.message.chat.id):
                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          text='Изменения применены!')
                    ProfileSettings.objects.filter(external_id=call.message.chat.id).update(subaccount_email=call.data)

        bot.polling()
