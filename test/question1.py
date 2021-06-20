#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime


def get_datetime(time):
  dt = datetime.strptime(time, '%Y%m%d%H%M%S')
  return dt


def isTimeout(text: str)->bool:
  return text=='-'


#故障期間は最初にタイムアウトしたとき
def question1(path='log.txt'):
  first_timeout_dict={}#{ip_address: date_time}
  result=[]#[(ip_address,故障期間]
  
  with open(path) as f:
    for line in f:
      #時刻、IPアドレス、反応時間
      time,ip_address,response_time=line.replace("\n","").split(',')
      if isTimeout(response_time):
        #そのipアドレスで初めてタイムアウトした時間を辞書に保存  
        first_timeout_dict.setdefault(ip_address, time) 
      else:
        if ip_address in first_timeout_dict.keys():
          #タイムアウト後、直った場合は故障リストからそのipアドレスを削除
          start=get_datetime(first_timeout_dict.pop(ip_address))
          end = get_datetime(time)
          dt=end-start
          result.append((ip_address,str(dt)))
  print(result)
  return result


if __name__ == '__main__':
  question1(path='data/question1_test.txt')
