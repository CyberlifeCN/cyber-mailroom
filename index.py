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
# --- refactored entry point for the application ---

import os.path
import ssl
import tornado.ioloop
from tornado.options import define, options
import tornado.web

# all the route config
import router


define("port", default=7020, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


def main():

    # router_ajax放在列表前面，保证优先获取规则
    app = tornado.web.Application(
        router.map(),
        # __TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__
        cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
        debug=options.debug,
        # login_url="/auth/api/unauthorized",
        # ssl_options={
        #    "certfile": os.path.join(os.path.abspath("."), "bike-forever.com.crt"),
        #    "keyfile": os.path.join(os.path.abspath("."), "bike-forever.com.key"),
        # }
    )
    # tornado.locale.load_gettext_translations(os.path.join(os.path.dirname(__file__), "locale"), "aplan")
    tornado.locale.set_default_locale("en_US")
    tornado.options.parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()