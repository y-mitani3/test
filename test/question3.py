#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import sys

def get_datetime(time):
  dt = datetime.strptime(time, '%Y%m%d%H%M%S')
  return dt


def update_last_m_list(ip_address,response_time,last_m_response:dict,m:int):
  time_list=[]
  if response_time=='-':
    response_time=999999
  if ip_address in last_m_response.keys():
    time_list=last_m_response[ip_address]
    time_list.append(int(response_time))
  else:
    time_list=[int(response_time)]
  m=min(len(time_list),m)
  #最後尾m個を抽出する
  last_m_response[ip_address]=time_list[-m:]


def isOverload(ip_address:str,last_m_response:dict,t):
  x = last_m_response[ip_address]
  return (sum(x)/len(x))>t


def question3(path='log.txt',m=2,t=5):
  last_m_response={}
  first_overload_dic={}
  result=[]#[(ip_address,過負荷期間]
  with open(path) as f:
    for line in f:
      time,ip_address,response_time=line.replace("\n","").split(',')
      update_last_m_list(ip_address,response_time,last_m_response,m)
      if isOverload(ip_address,last_m_response,t):
        first_overload_dic.setdefault(ip_address, time)
      else:#過負荷ではない時
        if ip_address in first_overload_dic.keys():
          start=get_datetime(first_overload_dic.pop(ip_address))
          end = get_datetime(time)
          dt=end-start
          result.append((ip_address,str(dt)))
  print(result)
  return result

def output(path,result):
  f=open(path, "w")
  for x in result:
    f.write(str(x)+'\n')
  f.close()

if __name__ == '__main__':
  args = sys.argv
  if len(args)==3:
    result=question3(path='data/question3_test.txt',m=int(args[1]),t=int(args[2]))
    output('result/result3.txt',result)
  else:
    print('引数m,tが必要\n例\npython3 question3.py m t')
    