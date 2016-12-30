#!/usr/bin/python
#_*_coding:utf-8 _*_

import urllib,urllib2
import json
import sys
import simplejson
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')

def gettoken(corpid, corpsecret):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
    #print  gettoken_url
    try:
        token_file = urllib2.urlopen(gettoken_url)
    except urllib2.HTTPError as e:
        print e.code
        print e.read().decode("utf8")
        sys.exit()
    token_data = token_file.read().decode('utf-8')
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json['access_token']
    return token

def senddata(access_token, user, subject, content):
    try:
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
        send_values = {
                "touser":"%s" %user,    #企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
                #"toparty":"7",    #企业号中的部门id。
                "msgtype":"text", #消息类型。
                "agentid":"9",    #企业号中的应用id。
                "text":{
                "content":subject + '\n' + content
                },
                "safe":"0"
                }
        send_data = simplejson.dumps(send_values, ensure_ascii=False).encode('utf-8')
        send_request = urllib2.Request(send_url, send_data)
        response = json.loads(urllib2.urlopen(send_request).read())
        #print str(response)
        if response['errmsg'] == 'ok':
                print "Send Messages Success!"
        else:
                with open('/tmp/Wechat.log','a+') as f:
                        f.write(user)
                        f.write(' ')
                        f.write(str(response))
                        f.write('\n')
    except:
        print "except in senddata:%s" % traceback.format_exc()

  
if __name__ == '__main__':
    user = str(sys.argv[1])     #zabbix传过来的第一个参数
    subject = str(sys.argv[2])  #zabbix传过来的第二个参数
    content = str(sys.argv[3])  #zabbix传过来的第三个参数
    
    corpid =  ''   #CorpID是企业号的标识
    corpsecret = ''  #corpsecretSecret是管理组凭证密钥
    accesstoken = gettoken(corpid, corpsecret)
    senddata(accesstoken, user, subject, content)
    
    
 -----------------------------------------------------------------------------
{
   "touser": "UserID1|UserID2|UserID3",
   "toparty": " PartyID1 | PartyID2 ",
   "totag": " TagID1 | TagID2 ",
   "msgtype": "text",
   "agentid": 1,
   "text": {
       "content": "Holiday Request For Pony(http://xxxxx)"
   },
   "safe":0
}
