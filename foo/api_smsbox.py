#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016-2017 7x24hs.com
# thomas@7x24hs.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.web
import logging
import time
import sys
import os
import json as JSON # 启用别名，不会跟方法里的局部变量混淆

from comm import *
from global_const import *
from base_handler import *
from foo.config import Config
CONF_FILE = "/etc/cyberlife/mailroom.conf"

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat

import requests
from tornado_swagger import swagger


@swagger.model()
class SendSmsReq:
    def __init__(self, smsUser, templateId, phone, fromName, content):
        self.smsUser = smsUser
        self.templateId = templateId
        self.phone = phone
        self.fromName = fromName
        self.content = content


# /smsbox/api/sms
class ApiSendSmsXHR(tornado.web.RequestHandler):
    @swagger.operation(nickname='post')
    def post(self):
        """
            @description: 发送短信

            @param body:
            @type body: C{SendSmsReq}
            @in body: body
            @required body: True

            @rtype: L{Resp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        logging.info("POST %r", self.request.uri)
        logging.debug("body %r", self.request.body)

        try:
            data = json_decode(self.request.body)
        except:
            logging.warn("Bad Request[400]: generate qrcode req_body=[%r]", self.request.body)

            self.set_status(200) # Bad Request
            self.write(JSON.dumps({"errCode":400,"errMsg":"Bad Request"}))
            self.finish()
            return

        # parse conf file
        conf = Config(CONF_FILE)
        conf.load_conf()

        param = {
            'smsUser': conf.get_sms_api_user(),
            'templateId' : data["templateId"],
            'msgType': 0,
            'phone' : data["phone"],
            'vars' : '{"%content%":data["content"]}'
        }

        param_keys = list(param.keys())
        param_keys.sort()

        param_str = ""
        for key in param_keys:
            param_str += key + '=' + str(param[key]) + '&'
        param_str = param_str[:-1]

        sign_str = conf.get_sms_api_key() + '&' + param_str + '&' + conf.get_sms_api_key()
        sign = generate_md5(sign_str)

        param['signature'] = sign

        try:
            resp = requests.post(conf.get_sms_api_url(), param)
            resp = JSON.loads(resp.text)
            logging.debug("%r", resp)

            if resp["statusCode"] == 200 and resp["result"] is True:
                logging.info("Success[200]: send sms=[%r]", param)
                self.set_status(200) # Success
                self.write(JSON.dumps({"errCode":200,"errMsg":"Success"}))
                self.finish()
            else:
                logging.error("Server Error[500]: send sms=[%r] error=[%r]", param, resp["message"])
                self.set_status(200) # Server Error
                self.write(JSON.dumps({"errCode":500,"errMsg":resp["message"]}))
                self.finish()
        except Exception as e:
            logging.error("Server Error[500]: send sms=[%r] error=[%r]", param, repr(e))
            self.set_status(200) # Server Error
            self.write(JSON.dumps({"errCode":500,"errMsg":repr(e)}))
            self.finish()
