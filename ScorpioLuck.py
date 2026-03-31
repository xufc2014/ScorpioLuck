import requests
from datetime import datetime

# ===================== 配置 =====================
# 聚合官方给你的接口（你已经有了）
apiUrl = 'http://web.juhe.cn/constellation/getAll'
apiKey = '459259e223c118bff6c1659bebe9e12d'

# 【必填】你的钉钉机器人 Webhook
DING_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=8a6b89739a039e2accb1245f1f8dff96aa083e8503bb6178d4ddddcb36d5c22e"
# ===================== 配置结束 =====================

def get_horoscope():
    requestParams = {
        'key': apiKey,
        'consName': '天蝎座',
        'type': 'today',
    }
    response = requests.get(apiUrl, params=requestParams)

    if response.status_code == 200:
        data = response.json()
        if data.get("error_code") != 0:
            return f"运势获取失败：{data.get('reason')}"

        res = data["result"]
        today = datetime.now().strftime("%Y年%m月%d日")
        
        # 组装好看的消息
        msg = f"📅 {today} 天蝎座今日运势\n\n"
        msg += f"🌟 综合运势：{res.get('summary', '无')}\n"
        msg += f"❤️ 爱情：{res.get('love', '无')}\n"
        msg += f"💼 事业：{res.get('career', '无')}\n"
        msg += f"💰 财富：{res.get('money', '无')}\n"
        msg += f"🧘 健康：{res.get('health', '无')}\n\n"
        msg += f"✨ 幸运色：{res.get('color', '无')}\n"
        msg += f"✨ 幸运数字：{res.get('number', '无')}"
        return msg
    else:
        return "请求异常"

def send_ding(msg):
    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }
    requests.post(DING_WEBHOOK, json=data)

if __name__ == "__main__":
    msg = get_horoscope()
    print(msg)
    send_ding(msg)
