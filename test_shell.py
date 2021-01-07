import os
import time
import re
# import kafka_proxy

metric = 'metric'
value = 'value'
tagkey1 = 'source_ip'
tagkey2 = 'destination_ip'
tagkey3 = 'source_site'
tagkey4 = 'destination_site'


def base_conversion(dst_ip):
    a = dst_ip.split(".")
    list1 = []
    for i in a:
        x = (hex(int(i))[2:]).upper()
        if len(x) == 1:
            x = "0"+x
        list1.append(x)
    return "".join(list1)

def del_shell(community,src_ip,num):
    shell = """
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.16.{num} integer 6
    """.format(community=community,src_ip=src_ip,num=num)
    os.popen(shell)
    s = os.popen(shell).read()
    return s

def test_shell(community,src_ip,dst_ip_16,num):
    shell1="""
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.16.{num} integer 6
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.16.{num} integer 5
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.15.{num} s "devops"
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.2.{num} integer 1
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.3.{num} x "{dst_ip}"
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.6.{num} integer 1000
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.4.{num} integer 10
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.5.{num} integer 64
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.16.{num} integer 1
    """.format(community=community,src_ip=src_ip,num=num,dst_ip=dst_ip_16)
    os.popen(shell1)
    s1 = os.popen(shell1).read()
    print(s1)
    time.sleep(10)


    shell = """
    snmpwalk -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.12.{num}
    """.format(community=community,src_ip=src_ip,num=num)
    os.popen(shell)
    s = os.popen(shell).read()
    xxx = del_shell(community,src_ip,num)
    print("del shell:",xxx)
    try:
        ss = s.split(":")
        return int((ss[1]).strip())
    except:
        return ""
#     print((ss[1]).strip())
#     for i in ss[:-1]:
#         print((i.split(":"))[0])
#         print((i.split(":"))[1])
#     print(s)


def deal_data_loss(ping_time,data,src_ip,dst_ip,src_site,dst_site):
    final = {}
    final['type'] = "Metric"
    final[metric] = "remoteping.loss"
    final[value] = data
    final["tags"] = {
        tagkey1: src_ip,
        tagkey2: dst_ip,
        tagkey3: src_site,
        tagkey4: dst_site,
    }
    final['timestamp'] = ping_time
    print (final)
    # kafka_proxy.kafka_producer(final)
    return

if __name__ == "__main__":
    import time
    community="devopstest"
    num = "330"
    src_ip = "114.112.72.14"
    dst_ip = "8.8.8.8"
    src_site = "test switch"
    dst_site = "google"
    dst_ip_16 = base_conversion(dst_ip)
    data = test_shell(community,src_ip,dst_ip_16,num)
    ping_time = int(time.time())
    deal_data_loss(ping_time,data,src_ip,dst_ip,src_site,dst_site)