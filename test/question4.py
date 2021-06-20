#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import ipaddress
import sys


def get_datetime(time):
  dt = datetime.strptime(time, '%Y%m%d%H%M%S')
  return dt


def get_network_address(host_address):
  net4 = ipaddress.ip_network(host_address, strict=False)
  return str(net4)


#ホスト台数は2^x-2
#ネットワークアドレスとブロードキャストアドレスを引く
def get_host_list(host_address):
  suffix = host_address.split('/')[1]
  net4 = ipaddress.ip_network(host_address, strict=False)
  result= [str(x)+'/'+suffix for x in net4.hosts()]
  return result


def get_timeout_count_dict(host_list):
  return {x:0 for x in host_list}


def isTimeout(text: str)->bool:
    return text=='-'


def plus_timeout_counter(host_address: str,network_address: str,timeout_counter: dict):
  if host_address in timeout_counter[network_address].keys():#カウンターに存在する場合 
    timeout_counter[network_address][host_address]+=1
  else:
    timeout_counter[network_address][host_address]=1


def is_n_times_timeout(host_address: str,network_address :str,timeout_counter: dict,n: int)->bool:
  return timeout_counter[network_address][host_address]>=n


def is_network_timeout(network_address: str,host_timeout_count_dict: dict,n: int):
  x=host_timeout_count_dict[network_address]
  #ネットワークのホスト全てのカウントがn以上の時にTrue
  keys = [k for k, v in x.items() if v >= n]
  return len(x)==len(keys)


#サブネット内のホストが全てタイムアウトしたときにサブネットの故障とする。
#サブネット毎にまとめて結果を出力する
def question4(path='log.txt',n=2):
  timeout_counter={} #{network_address:{host_address: 連続タイムアウト回数}}
  first_timeout_dict={} #{network_address:{host_address: date_time}}
  n_timeout_dic={} #{network_address:{host_address: n回以上タイムアウトしたときの最初の日時}}
  result={} #{network_address:[(host_address,故障期間]}
  with open(path) as f:
    for line in f:
      #時刻、IPアドレス、反応時間
      time,host_address,response_time=line.replace("\n","").split(',')
      network_address=get_network_address(host_address)
      if network_address not in timeout_counter:
        timeout_counter.setdefault(network_address,  get_timeout_count_dict(get_host_list(host_address)))
      first_timeout_dict.setdefault(network_address, {})
      n_timeout_dic.setdefault(network_address, {})
      result.setdefault(network_address, [])

      if isTimeout(response_time):
        first_timeout_dict[network_address].setdefault(host_address, time)
        plus_timeout_counter(host_address,network_address,timeout_counter)

        if is_n_times_timeout(host_address,network_address,timeout_counter,n):
          n_timeout_dic[network_address].setdefault(host_address, first_timeout_dict[network_address][host_address])

          if is_network_timeout(network_address,timeout_counter,n):
            print('host timeout')      

      else:
        timeout_counter[network_address][host_address]=0
        first_timeout_dict[network_address].pop(host_address,0)

        if host_address in n_timeout_dic[network_address].keys():
          start=get_datetime(n_timeout_dic[network_address].pop(host_address))
          end=get_datetime(time)
          dt = end-start
          result[network_address].append((host_address,str(dt)))
  print(result)
  return result

if __name__ == '__main__':
  args = sys.argv
  if len(args)==2:
    question4(path='data/question4_test.txt',n=int(args[1]))
  else:
    print('引数nが必要\n例\npython3 question4.py n')