#! /usr/bin/env python
# -*- coding: utf8 -*-
import time,json
import traceback
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import AllocatePublicIpAddressRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkecs.request.v20140526 import RebootInstanceRequest
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest

#areas = ["cn-beijing","cn-hangzhou","cn-hongkong","us-west-1","ap-southeast-1"]
areas = ["cn-hangzhou"]

class operation_ecs(object):

    def __init__(self, area):
        self.client = AcsClient("","",area)

    def create(self):
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_accept_format('json')

        request.set_InstanceType('ecs.t1.small');
        request.set_InstanceName('test-apicreate');
        request.set_InternetMaxBandwidthOut(1);
        request.set_ZoneId('cn-hangzhou-c');
        request.set_DataDisk1Size(200);
        request.set_HostName('hd1-test-1');
        request.set_ImageId('m-bp1eh9ld1ff');
        request.set_InternetChargeType('PayByBandwidth');
        request.set_InternetMaxBandwidthIn(200);
        request.set_SecurityGroupId('G175845184');
        request.set_Password('');
        request.set_DataDisk1Category('cloud');
        request.set_InstanceChargeType('PostPaid');
        #request.set_ClientToken('Isl2Na0');
        #request.set_IoOptimized('optimized');

        response = self.client.do_action_with_exception(request)
        #print json.loads(response)["InstanceId"]
        return json.loads(response)["InstanceId"]

    def public_ip(self, insid):
        request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
        request.set_accept_format('json')

        request.set_InstanceId(insid);

        response = self.client.do_action_with_exception(request)
        print "IP: %s" %json.loads(response)["IpAddress"]
    
    def start(self, insid):
        request = StartInstanceRequest.StartInstanceRequest()
        request.set_accept_format('json')

        request.set_InstanceId(insid);

        response = self.client.do_action_with_exception(request)
        print response

    def stop(self, insid):
        request = StopInstanceRequest.StopInstanceRequest()
        request.set_accept_format('json')

        request.set_InstanceId(insid);

        response = self.client.do_action_with_exception(request)
        print response
    
    def reboot(self, insid):
        request = RebootInstanceRequest.RebootInstanceRequest()
        request.set_accept_format('json')

        request.set_InstanceId(insid);

        response = self.client.do_action_with_exception(request)
        print response

    def delete(self, insid):
        request = DeleteInstanceRequest.DeleteInstanceRequest()
        request.set_accept_format('json')

        request.set_InstanceId(insid);

        response = self.client.do_action_with_exception(request)
        print response

if __name__ == '__main__':
    try:
        for ae in areas:
            INS = operation_ecs(ae)
            #INS_ID = INS.create()
            #INS.public_ip(INS_ID)
            #INS.start(INS_ID)
            #INS.stop('i-bp1diw9y2w5p2r8uatz6')
            #time.sleep(40)
            #INS.delete('i-bp1diw9y2w5p2r8uatz6')
    except:
        print "Except Error:%s" % traceback.format_exc()
