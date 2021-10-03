from binance.spot import Spot
from bot.models import ProfileSettings

def client(user_id):
    api_key = ProfileSettings.objects.get(external_id=user_id).api_key
    secret_key = ProfileSettings.objects.get(external_id=user_id).secret_key
    client = Spot(key=api_key, secret=secret_key)
    return client

def account_status(user_id):
    bc=client(user_id)
    try:
        status = bc.account_status().get('data')
        return status
    except:
        return 'error'

def info_workers(algo, user_id):
    bc = client(user_id)
    userName=ProfileSettings.objects.get(external_id=user_id).pool_username
    base_list = bc.mining_worker_list(algo=algo, userName=userName)
    numbers = len(base_list["data"]["workerDatas"])
    workers_data = base_list["data"]["workerDatas"][0:numbers]
    worker_status=[]
    for numbers, workers_data in enumerate(workers_data):
        worker_list = workers_data
        if worker_list["status"] == 1:
            active_workers=worker_list["workerName"]
            status_worker=active_workers + " работает"
            worker_status.append(status_worker)
        else:
            non_active=worker_list["workerName"]
            status_non_worker=non_active + " не работает"
            worker_status.append(status_non_worker)
    return worker_status

def get_profitability(user_id):
    bc = client(user_id)
    pool_login = ProfileSettings.objects.get(external_id=user_id).pool_username
    user_status_sha=bc.mining_earnings_list(algo="sha256", userName=pool_login)
    day_hash_rate_sha=user_status_sha["data"]["accountProfits"][0]["dayHashRate"]
    profit_amount_sha=user_status_sha["data"]["accountProfits"][0]["profitAmount"]
    profitability_sha=float(profit_amount_sha)/float(day_hash_rate_sha)

    user_status_ethash = bc.mining_earnings_list(algo="ethash", userName=pool_login)
    day_hash_rate_ethash = user_status_ethash["data"]["accountProfits"][0]["dayHashRate"]
    profit_amount_ethash = user_status_ethash["data"]["accountProfits"][0]["profitAmount"]
    profitability_ethash = float(profit_amount_ethash) / float(day_hash_rate_ethash)
    return "Доходност монет за единицу hash:\n" + str(format(profitability_sha*10**12, '.8f')) + " BTC за 1 THash \n" + str(format(profitability_ethash*10**6, '.8f')) + " ETH за 1 MHash"

def today_profit(user_id):
    bc = client(user_id)
    pool_login = ProfileSettings.objects.get(external_id=user_id).pool_username
    profit_btc = bc.mining_earnings_list(algo="sha256", userName=pool_login)
    profit_amount_btc = profit_btc["data"]["accountProfits"][0]["profitAmount"]
    price_btc=get_price(symbol="BTCUSDT", user_id=user_id)
    profit_btc_on_usdt=float(price_btc["price"]) * float(profit_amount_btc)
    profit_eth=bc.mining_earnings_list(algo="ethash", userName=pool_login)
    profit_amount_eth = profit_eth["data"]["accountProfits"][0]["profitAmount"]
    price_eth = get_price(symbol="ETHUSDT", user_id=user_id)
    profit_eth_on_usdt = float(price_eth["price"]) * float(profit_amount_eth)
    totаl_profit_on_usdt=profit_eth_on_usdt+profit_btc_on_usdt

    return"Доход за сегодняшний день составил:\n" + str(format(profit_amount_btc, '.6f')) + " BTC или "\
          + str(format(profit_btc_on_usdt, '.2f')) + " USDT\n"\
          + str(format(profit_amount_eth, '.6f')) + " ETH или "\
          + str(format(profit_eth_on_usdt, '.2f')) + " USDT\n"\
          + "Итоговый доход: " + str(format(totаl_profit_on_usdt, '.2f')) + " USDT\n"

def balance(user_id):
    bc = client(user_id)
    email=ProfileSettings.objects.get(external_id=user_id).subaccount_email
    balance=bc.sub_account_assets(email=email).get('balances')
    numbers=len(balance)
    for numbers, balance in enumerate(balance):
        if balance["free"] !=0:
            asset=balance["asset"]
            amount=balance["free"]
            return "На счету доступно: " + str(amount) + " " + str(asset)

def get_price(symbol, user_id):
    bc = client(user_id)
    price=bc.ticker_price(symbol=symbol)
    return price

def get_address_usdt(user_id):
    bc = client(user_id)
    email = ProfileSettings.objects.get(external_id=user_id).subaccount_email
    address=bc.sub_account_deposit_address(email=email, coin="USDT", network="trx")
    return(address['address'])

def get_subaccount_address(user_id):
    bc = client(user_id)
    emails=bc.sub_account_list().get("subAccounts")
    numbers=len(emails)
    emails_data=emails[0:numbers]
    emails=[]
    for numbers, emails_data in enumerate(emails_data):
        if emails_data["isFreeze"]==False:
            emails.append(emails_data["email"])
    return emails

def get_pool_address(user_id, username):
    bc = client(user_id)
    try:
        emails=bc.mining_account_list(algo='sha256', userName=username).get('code')
        if emails==0:
            return 'ok'
        else:
            return 'error'
    except:
        return 'error'

