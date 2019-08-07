import requests
import json



response = requests.get('https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_NG2011_6_20=/GlobalFuturesService.getGlobalFuturesDailyKLine?symbol=NG')

lts = response.text.find('(')
rts = response.text.find(')')
jss = response.text[lts + 1: rts]



jes = json.loads(jss)

print(type(jes))

