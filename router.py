#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2018 cyber-life.cn
# thomas@cyber-life.cn
# @2018/05/3
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
#
# genral application route config:
# simplify the router config by dinamic load class

import sys
import os
import tornado.web

from foo import comm
from foo import base_handler
from foo import api_mailroom
from foo import web


def map():

    config = [

        (r'/mailroom/api/email', getattr(api_mailroom, 'ApiSendMailXHR')),
        (r'/mailroom/web/index', getattr(web, 'WebMailroomIndexHandle')),
        (r'/smsbox/web/index', getattr(web, 'WebSmsboxIndexHandle')),
        (r'/', getattr(web, 'WebMailroomIndexHandle')),

        # comm
        ('.*', getattr(base_handler, 'UrlNotFoundXHR'))

    ]

    return config
