#! /usr/bin/env python
# -*- coding: utf8 -*-
import os,sys
import json
import traceback
import salt.client
import smtplib
from email.mime.text import MIMEText
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerAttributeRequest

client = AcsClient("","","cn-qd")
mailto_list = [""]
mail_host = "smtp.com"
mail_user = ""
mail_pass = ""
forbid_list = ['1.1.1.1','2.2.2.2','3.3.3.3']
slb_id = []
ecs_dict = {}
slb_dict = {}
add_dict = {}
del_dict = {}
mail_cotent = []

reload(sys)
sys.setdefaultencoding('utf8')

def ecs_list():
    try:
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        request.set_PageSize(100)

        response = client.do_action_with_exception(request)
        for ins in json.loads(response)["Instances"]["Instance"]:
            ecs_dict[ins["InstanceId"]] = "".join(ins['PublicIpAddress']['IpAddress'])
    except:
        print "Except Error in ecs_list:%s" % traceback.format_exc()

def slb_list():
    try:
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        request.set_accept_format('json')

        response = client.do_action_with_exception(request)
        for INS in json.loads(response)["LoadBalancers"]["LoadBalancer"]:
            if INS["Address"].startswith('100.'):
                slb_id.append(INS["LoadBalancerId"])
    except:
         print "Except Error in slb_list:%s" % traceback.format_exc()

def store_data(data):
    try:
        with open('/tmp/slb_dict.json', 'w+') as file_name:
            file_name.write(json.dumps(data))
    except:
        print "Except Error in store_data:%s" % traceback.format_exc()

def load_data():
    try:
        with open('/tmp/slb_dict.json', 'r+') as file_name:
            data = json.load(file_name)
            return data
    except:
        print "Except Error in load_data:%s" % traceback.format_exc()

def slb_diff(old_data,new_data):
    try:
        old_data_key = old_data.keys()
        new_data_key = new_data.keys()
        diff_1 = list(set(old_data_key) ^ set(new_data_key))
        comm_1 = list(set(old_data_key) & set(new_data_key))
        if diff_1:
            for l in diff_1:
                if l in old_data_key:
                    for i in old_data[l]:
                        #print "执行删除: %s: %s" %(str(i),str(l))
                        del_dict[str(i)] = str(l)
                elif l in new_data_key:
                    for i in new_data[l]:
                        #print "执行添加: %s: %s" %(str(i),str(l))
                        add_dict[str(i)] = str(l)
            for l1 in comm_1:
                diff_2 = list(set(old_data[l1]) ^ set(new_data[l1]))
                if diff_2:
                    for l2 in diff_2:
                        if l2 in old_data[l1]:
                            #print "执行删除1: %s: %s" %(str(l2),str(l1))
                            del_dict[str(l2)] = str(l1)
                        elif l2 in new_data[l1]:
                            #print "执行添加1: %s: %s" %(str(l2),str(l1))
                            add_dict[str(l2)] = str(l1)
        else:
            for l in comm_1:
                diff_2 = list(set(old_data[l]) ^ set(new_data[l]))
                if diff_2:
                    for l2 in diff_2:
                        if l2 in old_data[l]:
                            #print "执行删除2: %s: %s" %(str(l2),str(l))
                            del_dict[str(l2)] = str(l)
                        elif l2 in new_data[l]:
                            #print "执行添加2: %s: %s" %(str(l2),str(l))
                            add_dict[str(l2)] = str(l)
    except:
        print "Except Error in slb_diff:%s" % traceback.format_exc()

def one_slb_detailed(LBID):
    try:
        request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(LBID)

        response = client.do_action_with_exception(request)
        BKS_ip = []
        #print json.loads(response)["Address"]
        for bk in json.loads(response)["BackendServers"]["BackendServer"]:
            bk_ip = ecs_dict[bk["ServerId"]]
            BKS_ip.append(bk_ip)
        slb_dict[json.loads(response)["Address"]] = BKS_ip
    except:
        print "Except Error in one_slb_detailed:%s" % traceback.format_exc()

def salt_custom(slb_ip,ins_ip):
    try:
        salt_client = salt.client.LocalClient()
        ret = salt_client.cmd(ins_ip, 'cmd.run', ['grep "%s" /etc/hosts' %slb_ip])
        if ret[ins_ip] != '':
            #salt_client.cmd(ins_ip, 'cmd.run', ['sed -i "s/%s/127.0.0.1/g" /etc/hosts' %slb_ip])
            mail_cotent.append(ret)
    except:
        print "Except Error in salt_custom:%s" % traceback.format_exc()
        
def salt_iptable(ins_ip,slb_ip,action):
    try:
        salt_client = salt.client.LocalClient()
        if action == "del":
            print "%s -- iptables -D OUTPUT -p tcp -o eth0 -d %s -j DROP" %(ins_ip,slb_ip)
            #salt_client.cmd(ins_ip,'cmd.run', ['iptables -D OUTPUT -p tcp -o eth0 -d %s -j DROP' %slb_ip])
        elif action == "add":
            print "%s -- iptables -I OUTPUT -p tcp -o eth0 -d %s -j DROP" %(ins_ip,slb_ip)
            #ret = salt_client.cmd(ins_ip,'cmd.run', ['iptables-save |grep -- "-A OUTPUT -d %s/32 -o eth0 -p tcp -j DROP"' %slb_ip])
            #if ret[ins_ip] == '':
            #    salt_client.cmd(ins_ip,'cmd.run', ['iptables -I OUTPUT -p tcp -o eth0 -d %s -j DROP' %slb_ip])
            #else:
                #print "%s drop %s规则已经存在" %(ins_ip,slb_ip)
            #    mail_cotent.append("%s drop %s规则已经存在" %(ins_ip,slb_ip))
        elif action == "all":
            print "%s -- iptables -I OUTPUT -p tcp -o eth0 -d %s -j DROP" %(ins_ip,slb_ip)
            #ret = salt_client.cmd(ins_ip,'cmd.run', ['iptables-save |grep -- "-A OUTPUT -d %s/32 -o eth0 -p tcp -j DROP"' %slb_ip])
            #if ret[ins_ip] == '':
            #    salt_client.cmd(ins_ip,'cmd.run', ['iptables -I OUTPUT -p tcp -o eth0 -d %s -j DROP' %slb_ip])
            #else:
                #print "%s drop %s规则已经存在" %(ins_ip,slb_ip)
            #    mail_cotent.append("%s drop %s规则已经存在" %(ins_ip,slb_ip))
        else:
            print "执行动作不合法"
    except:
        print "Except Error in salt_iptable:%s" % traceback.format_exc()

def main(choice):
    try:
        slb_list()
        ecs_list()
        for s_id in slb_id:
            one_slb_detailed(s_id)
        if choice == "iptable":
            if os.path.exists('/tmp/slb_dict.json'):
                if os.path.getsize('/tmp/slb_dict.json'):
                    old_dict = load_data()
                else:
                    print "slb文件为空"
                    sys.exit()
            else:
                print "slb存储文件不存在"
            store_data(slb_dict)
            slb_diff(old_dict,slb_dict)
            if add_dict:
                for l3 in add_dict:
                    if add_dict[l3] not in forbid_list:
                        salt_iptable(l3,add_dict[l3],"add")
            if del_dict:
                for l4 in del_dict:
                    if del_dict[l4] not in forbid_list:
                        salt_iptable(l4,del_dict[l4],"del")
            #if slb_dict:
            #    for l5 in slb_dict:
            #        if l5 not in forbid_list:
            #            for i in slb_dict[l5]:
            #                salt_iptable(i,l5,"all")
        elif choice == "host":
            for s in slb_dict:
                if s not in forbid_list:
                    for i in slb_dict[s]:
                        salt_custom(s,i)
        else:
            print "参数不合法"
    except:
        print "Except Error in main:%s" % traceback.format_exc()

def send_mail(to_list,sub,content):
    me="Slb_Notice"+"<"+mail_user+">"
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
    except:
        print "except in send_mail:%s" % traceback.format_exc()

if __name__ == '__main__':
    try:
        arg = sys.argv[1]
        main(arg)
    except:
        print "Except Error in: %s" % traceback.format_exc()
    if mail_cotent:
        send_mail(mailto_list,"slb domain server and client conflict!",str(mail_cotent))
