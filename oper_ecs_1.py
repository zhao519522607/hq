#! /usr/bin/env python
# -*- coding: utf8 -*-
import time,json,datetime
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
        "创建实例"
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_accept_format('json')

        request.set_InstanceType('ecs.c2.medium');
        request.set_InstanceName('quick-recovery-');
        request.set_InternetMaxBandwidthOut(1);
        request.set_ZoneId('cn-hangzhou-c');
        request.set_DataDisk1Size(200);
        request.set_HostName('hd1-ip');
        request.set_ImageId('');
        request.set_InternetChargeType('PayByBandwidth');
        request.set_InternetMaxBandwidthIn(200);
        request.set_SecurityGroupId('');
        request.set_Password('');
        request.set_DataDisk1Category('cloud');
        request.set_InstanceChargeType('PostPaid');
        #request.set_ClientToken('2N');
        #request.set_IoOptimized('optimized');

        response = self.client.do_action_with_exception(request)
        #print json.loads(response)["InstanceId"]
        return json.loads(response)["InstanceId"]

    def public_ip(self, insid):
        "给实例分配公网ip"
        request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
        request.set_accept_format('json')

        request.set_InstanceId(insid);

        response = self.client.do_action_with_exception(request)
        print "IP: %s" %json.loads(response)["IpAddress"]

    def start(self, insid):
        "启动实例"
        request = StartInstanceRequest.StartInstanceRequest()
        request.set_accept_format('json')

        request.set_InstanceId(insid);
        
    response = self.client.do_action_with_exception(request)
        print response

    def stop(self, insid):
        "停止实例"
        request = StopInstanceRequest.StopInstanceRequest()
        request.set_accept_format('json')

        request.set_InstanceId(insid);

        response = self.client.do_action_with_exception(request)
        print response

    def reboot(self, insid):
        "重启实例"
        request = RebootInstanceRequest.RebootInstanceRequest()
        request.set_accept_format('json')

        request.set_InstanceId(insid);

        response = self.client.do_action_with_exception(request)
        print response

    def delete(self, insid):
        "删除实例"
        request = DeleteInstanceRequest.DeleteInstanceRequest()
        request.set_accept_format('json')

        request.set_InstanceId(insid);

        response = self.client.do_action_with_exception(request)
        print response
        
    def del_image(self, imgid):
        "删除镜像文件"
        request = DeleteImageRequest.DeleteImageRequest()
        request.set_accept_format('json')

        request.set_ImageId(imgid);

        response = self.client.do_action_with_exception(request)
        print response

    def del_shapshot(self, shapID):
        "删除磁盘快照文件"
        request = DeleteSnapshotRequest.DeleteSnapshotRequest()
        request.set_accept_format('json')

        request.set_SnapshotId(shapID);

        response = self.client.do_action_with_exception(request)
        print response


if __name__ == '__main__':
    try:
        d1 = datetime.datetime.now()
        for ae in areas:
            INS = operation_ecs(ae)
            INS_ID = INS.create()
            INS.public_ip(INS_ID)
            INS.start(INS_ID)
        d2 = datetime.datetime.now()
        d = d2 - d1
        print "执行时间为%s秒" %d.seconds
            #INS.stop('i-bp1diw9y2w5p2r8uatz6')
            #time.sleep(40)
            #INS.delete('i-bp1diw9y2w5p2r8uatz6')
    except:
        print "Except Error:%s" % traceback.format_exc()
