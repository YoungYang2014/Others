# -*- coding: utf-8 -*-
from inf_http import WebDownloader
from datetime import datetime, date, timedelta
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class GetAbnormal():
    """考勤爬虫"""
    def __init__(self):
        self.url = "http://171.221.203.127:8009"
        self.http = WebDownloader()

    def login(self, usr, pwd):
        url = "%s/iclock/accounts/login/" % self.url
        post_data = {
                    "username": usr,
                    "password": pwd,
                    "logintype": "employee"
                    }
        code, res = self.http.http_post(url, post_data)
        if code:
            if json.loads(res)["ret"] == 2:
                return True
        return False

    def get_error(self):
        """获取考勤异常"""
        # 获取最近15天考勤异常数据
        enddate = date.today().strftime('%Y-%m-%d')
        startdate = (date.today()-timedelta(days=15)).strftime('%Y-%m-%d')
        url = "http://171.221.203.127:8009/iclock/staff/abnormite/?starttime=%s&endtime=%s" %(startdate, enddate)
        code, res = self.http.http_post(url, {})
        clock_list = json.loads(res)
        new_list = []
        for clock in clock_list:
            try:
                if "".join(clock[-4:]) != "":
                    weekday = self.get_week_day(clock)
                    clock.insert(3, weekday)
                    new_list.append(clock)
            except:
                weekday = self.get_week_day(clock)
                clock.insert(3, weekday)
                new_list.append(clock)
        return new_list

    def get_history(self):
        clock_list_ok = []
        clock_list = []
        enddate = date.today().strftime('%Y-%m-%d')
        startdate_1 = (date.today() - timedelta(days=90)).strftime('%Y-%m-%d')
        startdate_2 = (date.today() - timedelta(days=60)).strftime('%Y-%m-%d')
        datelist = [startdate_1, startdate_2, enddate]
        for i in range(2):
            url = "http://171.221.203.127:8009/iclock/staff/attshifts/?starttime=%s&endtime=%s"%(datelist[i], datelist[i+1])
            code, res = self.http.http_post(url, {})
            dates = json.loads(res)
            dates.sort()
            dates = dates[:-1]
            clock_list = clock_list+dates
        clock_list.sort()
        for i in clock_list:
            if i[7] > "19:00:00":
                i = [i[0],i[1],i[2],i[6],i[7], self.getTimeDiff(i[7], "19:00:00")]
                clock_list_ok.append(i)
                continue
            if ("周六" in i[2] or "周日" in i[2]) and i[7] != "":
                i = [i[0], i[1], i[2], i[6], i[7], self.getTimeDiff(i[7], i[6])-90]
                clock_list_ok.append(i)
        return clock_list_ok

    def get_week_day(self, clock):
        """获取日期为星期几"""
        week_day_dict = {
                            0: '星期一',
                            1: '星期二',
                            2: '星期三',
                            3: '星期四',
                            4: '星期五',
                            5: '星期六',
                            6: '星期天',
                        }
        day = datetime.strptime(clock[2], "%Y-%m-%d %H:%M:%S").weekday()
        return week_day_dict[day]

    def getTimeDiff(self, timeStra, timeStrb):
        """计算分钟差"""
        timeStra = str(timeStra)
        timeStrb = str(timeStrb)
        if timeStra <= timeStrb:
            return 0
        ta = time.strptime(timeStra, "%H:%M:%S")
        tb = time.strptime(timeStrb, "%H:%M:%S")
        y, m, d, H, M, S = ta[0:6]
        dataTimea = datetime(y, m, d, H, M, S)
        y, m, d, H, M, S = tb[0:6]
        dataTimeb = datetime(y, m, d, H, M, S)
        secondsDiff = (dataTimea - dataTimeb).seconds
        return int(secondsDiff/60)

if __name__ == "__main__":
    pass