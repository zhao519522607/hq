#! /usr/bin/env python
# -*- coding: utf8 -*-
import time,json
import traceback
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DeleteImageRequest
from aliyunsdkecs.request.v20140526 import DeleteSnapshotRequest
from aliyunsdkecs.request.v20140526 import CreateSnapshotRequest
from aliyunsdkecs.request.v20140526 import CreateDiskRequest
from aliyunsdkecs.request.v20140526 import DeleteDiskRequest

areas = ["cn-hangzhou"]

class ali_disk(object):

    def __init__(self, area):
        self.client = AcsClient("","",area)

    def del_image(self, imgid):
        "删除镜像文件"
        try:
            request = DeleteImageRequest.DeleteImageRequest()
            request.set_accept_format('json')
            request.set_ImageId(imgid);

            response = self.client.do_action_with_exception(request)
            print response
        except:
            print "Except Error in del_image:%s" % traceback.format_exc()

    def del_shapshot(self, shapID):
        "删除磁盘快照文件"
        try:
            request = DeleteSnapshotRequest.DeleteSnapshotRequest()
            request.set_accept_format('json')
            request.set_SnapshotId(shapID);

            response = self.client.do_action_with_exception(request)
            print response
        except:
            print "Except Error in del_shapshot:%s" % traceback.format_exc()

    def create_shot(self, disk_id, shot_name):
        "创建磁盘快照"
        try:
            request = CreateSnapshotRequest.CreateSnapshotRequest()
            request.set_accept_format('json')
            request.add_query_param('DiskId', disk_id)
            request.add_query_param('SnapshotName', shot_name)

            response = self.client.do_action_with_exception(request)
            print response
        except:
            print "Except Error in create_shot:%s" % traceback.format_exc()

    def create_disk(self, shot_id):
        "创建磁盘"
        try:
            request = CreateDiskRequest.CreateDiskRequest()
            request.set_accept_format('json')
            request.add_query_param('SnapshotId', shot_id)
            request.add_query_param('ZoneId', 'cn-hangzhou-d')
            request.add_query_param('Size', 40)

            response = self.client.do_action_with_exception(request)
            print response
        except:
            print "Except Error in create_disk:%s" % traceback.format_exc()

    def delete_disk(self, disk_id):
        "删除磁盘"
        try:
            request = DeleteDiskRequest.DeleteDiskRequest()
            request.set_accept_format('json')
            request.add_query_param('DiskId', disk_id)

            response = self.client.do_action_with_exception(request)
            print response
        except:
            print "Except Error in delete_disk:%s" % traceback.format_exc()

if __name__ == '__main__':
    try:
        for ae in areas:
            INS = ali_disk(ae)
            INS.delete_disk('d-')
            #INS.create_shot('d-231', 'test-30')
            #INS.del_image('m-bp15q5cv7l31gch8vcel')
            #INS.del_shapshot('s-bp17kgbuvah0r2q5wnpg')
            #time.sleep(40)
    except:
        print "Except Error:%s" % traceback.format_exc()
