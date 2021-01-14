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
    s = os.popen(shell).read()
    return s


def latency_shell(community,src_ip,num):
    shell1 = """
    snmpwalk -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.12.{num}
    """.format(community=community,src_ip=src_ip,num=num)
    s1 = os.popen(shell1).read()
    try:
        ss = s1.split(":")
        return int((ss[1]).strip())
    except:
        return ""


def loss_shell(community,src_ip,num):
    shell2 = """
    snmpwalk -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.9.{num}
    """.format(community=community,src_ip=src_ip,num=num)
    s2 = os.popen(shell2).read()
    shell3 = """
    snmpwalk -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.10.{num}
    """.format(community=community,src_ip=src_ip,num=num)
    s3 = os.popen(shell3).read()
    try:
        sent_packet = s2.split(":")
        receive_packet = s3.split(":")
        data_loss = ((int(sent_packet[1])-int(receive_packet[1]))/int(sent_packet[1]))
        return data_loss
    except:
        return ""


def test_shell(community,src_ip,dst_ip_16,num):
    shell1="""
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.16.{num} integer 6
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.16.{num} integer 5
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.15.{num} s "devops"
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.2.{num} integer 1
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.3.{num} x "{dst_ip}"
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.4.{num} integer 20
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.5.{num} integer 64
    snmpset -v 2c -c {community} {src_ip} .1.3.6.1.4.1.9.9.16.1.1.1.16.{num} integer 1
    """.format(community=community,src_ip=src_ip,num=num,dst_ip=dst_ip_16)
    s1 = os.popen(shell1).read()
    print(s1)
    time.sleep(30)
    data_latency = latency_shell(community,src_ip,num)
    data_loss = loss_shell(community,src_ip,num)
    print("---",data_loss)
    del_snmp = del_shell(community,src_ip,num)
    print("del shell:",del_snmp)
    return data_latency, data_loss
    

def deal_data_latency(ping_time,data,src_ip,dst_ip,src_site,dst_site):
    final = {}
    final['type'] = "Metric"
    final[metric] = "net.latency"
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


def deal_data_loss(ping_time,data,src_ip,dst_ip,src_site,dst_site):
    final = {}
    final['type'] = "Metric"
    final[metric] = "net.loss"
    final[value] = data
    final["tags"] = {
        tagkey1: src_ip,
        tagkey2: dst_ip,
        tagkey3: src_site,
        tagkey4: dst_site,
    }
    final['timestamp'] = ping_time
    # kafka_proxy.kafka_producer(final)
    print (final)
    return

if __name__ == "__main__":
    import time
    import sys
    ping_time = int(time.time())
    # src_ip = sys.argv[1]
    # dst_ip = sys.argv[2]
    # num = sys.argv[3]
    # community="Cds@QAZXSWedc"
    community="devopstest"
    num = "330"
    # src_ip = "114.112.76.117"
    src_ip = "114.112.72.14"
    # dst_ip = "139.159.48.236"
    dst_ip = "8.8.8.8"
    src_site = "test switch"
    dst_site = "google"
    dst_ip_16 = base_conversion(dst_ip)
    data_latency, data_loss = test_shell(community,src_ip,dst_ip_16,num)
    deal_data_latency(ping_time,data_latency,src_ip,dst_ip,src_site,dst_site)
    deal_data_loss(ping_time,data_loss,src_ip,dst_ip,src_site,dst_site)