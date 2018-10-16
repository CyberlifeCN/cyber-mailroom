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

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat

import requests
from tornado_swagger import swagger


@swagger.model()
class SendMailReq:
    def __init__(self, fromEmail, fromName, toEmail, subject, content):
        self.fromEmail = fromEmail
        self.fromName = fromName
        self.toEmail = toEmail
        self.subject = subject
        self.content = content


# /mailroom/api/email
class ApiSendMailXHR(tornado.web.RequestHandler):
    @swagger.operation(nickname='post')
    def post(self):
        """
            @description: 发送email

            @param body:
            @type body: C{SendMailReq}
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

        params = {
            "apiUser": SEND_CLOUD_API_USER,  # 使用api_user和api_key进行验证
            "apiKey": SEND_CLOUD_API_KEY,
            "to": ";".join(data["toEmail"]),  # 收件人地址, 用正确邮件地址替代, 多个地址用';'分隔
            "from": data["fromEmail"],  # 发信人, 用正确邮件地址替代
            "fromName": data["fromName"],
            "subject": data["subject"],
            "html": data["content"]
        }

        try:
            resp = requests.post(SEND_CLOUD_EMAIL_API_URL, params)
            logging.info("%r", resp.text)
            resp = JSON.loads(resp.text)

            if resp["statusCode"] == 200 and resp["result"] is True:
                logging.info("Success[200]: send email=[%r]", params)
                self.set_status(200) # Success
                self.write(JSON.dumps({"errCode":200,"errMsg":"Success"}))
                self.finish()
            else:
                logging.error("Server Error[500]: send email=[%r] error=[%r]", params, resp["message"])
                self.set_status(200) # Server Error
                self.write(JSON.dumps({"errCode":500,"errMsg":resp["message"]}))
                self.finish()
        except Exception as e:
            logging.error("Server Error[500]: send email=[%r] error=[%r]", params, repr(e))
            self.set_status(200) # Server Error
            self.write(JSON.dumps({"errCode":500,"errMsg":repr(e)}))
            self.finish()
