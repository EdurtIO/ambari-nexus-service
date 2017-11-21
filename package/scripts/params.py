#!/usr/bin/env python

'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from resource_management import *

# service config
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

# java config
java_sdk_home = config['configurations']['java.env']['java.home']

# nexus config (get config for `nexus.env.xml` file)
nexus_local_dir = config['configurations']['nexus.env']['nexus.local.dir']
nexus_home_dir = config['configurations']['nexus.env']['nexus.home.dir']
nexus_pid_dir = config['configurations']['nexus.env']['nexus.pid.dir']
nexus_log_dir = config['configurations']['nexus.env']['nexus.log.dir']
nexus_user = config['configurations']['nexus.env']['nexus.user']
nexus_group = config['configurations']['nexus.env']['nexus.group']
nexus_package_name = config['configurations']['nexus.env']['nexus.package.name']
nexus_package_download = config['configurations']['nexus.env']['nexus.package.download.path']
nexus_log_install_file = nexus_log_dir + config['configurations']['nexus.env']['nexus.log.install.file']
nexus_pid_file = nexus_pid_dir + config['configurations']['nexus.env']['nexus.pid.file']
