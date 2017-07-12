#! /usr/bin/env python
# -*- coding: utf8 -*-
from aliyunsdkcore.client import AcsClient
import json
import time
#from aliyunsdkcore.acs_exception.exceptions import ClientException
#from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest

#areas = ["cn-beijing","cn-hangzhou","cn-hongkong","us-west-1","ap-southeast-1"]
areas = ["cn-beijing"]

def main(area):
    client = AcsClient("","",area)
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')
    request.set_PageSize(100)

    response = client.do_action_with_exception(request)
    #print response
    for ins in json.loads(response)["Instances"]["Instance"]:
        print '\t'.join(ins['PublicIpAddress']['IpAddress']),ins['InstanceType'],ins['Memory']/1024,ins['ZoneId'],ins['InternetMaxBandwidthOut'],ins['ImageId']

if __name__ == '__main__':
    try:
        for ae in areas:
            main(ae)
    except:
        time.sleep(30)
        for ae in areas:
            main(ae)
