#! /usr/bin/env python
# -*- coding: utf8 -*-
import json
import traceback
import salt.client
import smtplib
from email.mime.text import MIMEText
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerAttributeRequest

client = AcsClient("","","cn-hangzhou")
mailto_list = [""]
mail_host = "smtp.exmail.qq.com"
mail_user = ""
mail_pass = ""
slb_id = []
ecs_dict = {}
slb_dict = {}
mail_cotent = []

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

def main():
    try:
        slb_list()
        ecs_list()
        for s_id in slb_id:
            one_slb_detailed(s_id)
        for s in slb_dict:
            if s != '100.31' and s != '100.213' and s != '100.97':
                for i in slb_dict[s]:
                    salt_custom(s,i)
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
    main()
    if mail_cotent:
        send_mail(mailto_list,"slb domain server and client conflict!",str(mail_cotent))
