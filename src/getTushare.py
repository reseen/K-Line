import tushare as ts 

pro = ts.pro_api('4e5e2d7fbf14185d371c9a5e78d178882d2b91436a0de40599a29ece')

# 获取所有股票名称
data = pro.stock_basic(exchange = '', list_status = '', fields = 'ts_code, symbol, name, area, industry, fullname, enname, market, exchange, curr_type, list_status, list_date, delist_date')


print(type(data))
print(len(data))

print(data.ts_code[0])

print("OK")



# 获取日线
# df = pro.daily(ts_code='000001.SZ', start_date='20180101', end_date='')
# print(df)

# 获取数字货币名称
# df = pro.coinlist(start_date='20170101', end_date='')
# print(df)

# 获取每日行情
# df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='daily', start_date='20190501', end_date='')