import requests
import os
from datetime import datetime

# 从环境变量读取敏感信息
apiUrl = "http://web.juhe.cn/constellation/getAll"
apiKey = os.getenv("JUHE_API_KEY")
DING_WEBHOOK = os.getenv("DING_WEBHOOK")

def get_horoscope(consName="天蝎座", type_="today"):
    """获取指定类型的运势"""
    params = {
        "key": apiKey,
        "consName": consName,
        "type": type_
    }
    try:
        response = requests.get(apiUrl, params=params, timeout=10)
        if response.status_code != 200:
            return f"❌ {type_}运势请求失败：网络异常"
        data = response.json()
        if data.get("error_code") != 0:
            return f"❌ {type_}运势获取失败：{data.get('reason')}"
        return data
    except Exception as e:
        return f"❌ {type_}运势请求异常：{str(e)}"

def format_today_msg(data):
    """格式化今日运势消息"""
    today = data["datetime"]
    name = data["name"]
    summary = data["summary"]
    work = data["work"]
    love = data["love"]
    money = data["money"]
    health = data["health"]
    color = data["color"]
    number = data["number"]

    msg = f"📅 {today} {name} 今日运势\n\n"
    msg += f"🌟 综合：{summary}\n\n"
    msg += f"💼 事业：{work} 分\n"
    msg += f"❤️ 爱情：{love} 分\n"
    msg += f"💰 财运：{money} 分\n"
    msg += f"🧘 健康：{health} 分\n\n"
    msg += f"✨ 幸运色：{color}\n"
    msg += f"✨ 幸运数字：{number}"
    return msg

def format_week_msg(data):
    """格式化本周运势消息"""
    name = data["name"]
    week_date = f"{data['date'][:4]}年{data['date'][4:6]}月{data['date'][6:8]}日 起一周"
    summary = data["summary"]
    work = data["work"]
    love = data["love"]
    money = data["money"]
    health = data["health"]
    color = data["color"]
    number = data["number"]

    msg = f"\n\n📅 {week_date} {name} 本周运势\n\n"
    msg += f"🌟 综合：{summary}\n\n"
    msg += f"💼 事业：{work} 分\n"
    msg += f"❤️ 爱情：{love} 分\n"
    msg += f"💰 财运：{money} 分\n"
    msg += f"🧘 健康：{health} 分\n\n"
    msg += f"✨ 幸运色：{color}\n"
    msg += f"✨ 幸运数字：{number}"
    return msg

def send_ding(msg):
    """推送消息到钉钉"""
    if not DING_WEBHOOK:
        print("❌ 未配置钉钉Webhook")
        return
    data = {
        "msgtype": "text",
        "text": {"content": msg}
    }
    try:
        requests.post(DING_WEBHOOK, json=data, timeout=10)
        print("✅ 钉钉推送成功")
    except Exception as e:
        print(f"❌ 钉钉推送失败：{e}")

if __name__ == "__main__":
    # 判断今天是周几（周一=0，周日=6）
    today_weekday = datetime.now().weekday()
    is_monday = (today_weekday == 0)

    # 获取今日运势
    today_data = get_horoscope(type_="today")
    if isinstance(today_data, dict):
        today_msg = format_today_msg(today_data)
    else:
        today_msg = today_data  # 错误信息

    # 周一额外获取本周运势
    if is_monday:
        week_data = get_horoscope(type_="week")
        if isinstance(week_data, dict):
            week_msg = format_week_msg(week_data)
        else:
            week_msg = f"\n\n❌ {week_data}"
        full_msg = today_msg + week_msg
    else:
        full_msg = today_msg

    print(full_msg)
    send_ding(full_msg)



