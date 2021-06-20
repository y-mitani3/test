#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import sys

def get_datetime(time):
  dt = datetime.strptime(time, '%Y%m%d%H%M%S')
  return dt


def isTimeout(text: str)->bool:
    return text=='-'


def plus_timeout_counter(ip_address: str,timeout_counter: dict):
  if ip_address in timeout_counter.keys():#カウンターに存在する場合 
    timeout_counter[ip_address]+=1
  else:
    timeout_counter[ip_address]=1
  

def is_n_times_timeout(ip_address: str,timeout_counter: dict,n: int)->bool:
  return timeout_counter[ip_address]>=n


def question2(path='log.txt',n=2):
  timeout_counter={}#{ip_address: 連続タイムアウト回数}
  n_timeout_dic={}#{ip_address: n回以上タイムアウトしたときの最初の日時}
  first_timeout_dict={}#{ip_address: date_time}
  result=[]#[(ip_address,故障期間]
  with open(path) as f:
    for line in f:
      #時刻、IPアドレス、反応時間
      time,ip_address,response_time=line.replace("\n","").split(',')
      #ログがタイムアウト時、時刻とカウントをする
      if isTimeout(response_time):
        first_timeout_dict.setdefault(ip_address, time)
        plus_timeout_counter(ip_address,timeout_counter)
        #タイムアウト時、n回以上かどうか
        if is_n_times_timeout(ip_address,timeout_counter,n):
          n_timeout_dic.setdefault(ip_address, first_timeout_dict[ip_address])
      else:
        timeout_counter[ip_address]=0#通常の場合は連続タイムアウトカウンターを0にする
        first_timeout_dict.pop(ip_address,0)#時刻を削除
        if ip_address in n_timeout_dic.keys():#IPがn回連続故障リストに含まれる場合
          start=get_datetime(n_timeout_dic.pop(ip_address))
          end = get_datetime(time)
          dt=end-start
          result.append((ip_address,str(dt)))
  print(result)
  return result


if __name__ == '__main__':
  args = sys.argv
  if len(args)==2:
    question2('data/question2_test.txt',n=int(args[1]))
  else:
    print('引数nが必要\n例\npython3 question2.py n')