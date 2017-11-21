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

import grp
import pwd
from resource_management import *


class NexusServer(Script):
    """
    Contains the interface definitions for methods like install,
    start, stop, status, etc. for the Nexus Server
    """

    # install process
    def install(self, env):
        # Import properties
        import params
        env.set_params(params)
        self.install_packages(env)
        # group
        try:
            grp.getgrnam(params.nexus_group)
        except KeyError:
            Group(group_name=params.nexus_group)
        # user
        try:
            pwd.getpwnam(params.nexus_user)
        except KeyError:
            # generate nexus user
            User(username=params.nexus_user,
                 gid=params.nexus_group,
                 groups=[params.nexus_group],
                 ignore_failures=True)

        # generate dir
        Directory([params.nexus_log_dir, params.nexus_pid_dir, params.nexus_home_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.nexus_user,
                  group=params.nexus_group)

        # log file
        File(params.nexus_log_install_file,
             mode=0644,
             owner=params.nexus_user,
             group=params.nexus_group,
             content='')

        # get install file command
        Execute(
            'cd ' + params.nexus_local_dir + ';' +
            'wget ' + params.nexus_package_download +
            ' -O ' + params.nexus_package_name + ' -a ' + params.nexus_log_install_file)

        # decompression install file, delete source file
        Execute('cd {0}; tar -zxvf {1} -C {2}; rm -rf {1}'.format(params.nexus_local_dir,
                                                                 params.nexus_package_name,
                                                                 params.nexus_home_dir))

        Execute('cd {0}; mv nexus-* nexus'.format(params.nexus_home_dir))

        # chown nexus home
        Execute('chown -R {0}:{1} {2}'.format(params.nexus_user, params.nexus_group, params.nexus_home_dir))

        # set java home
        Execute(format("sed -i '1i\JAVA_HOME={java_sdk_home}' {nexus_home_dir}/nexus/bin/nexus"), user=params.nexus_user)
        Logger.info("Nexus Install is Completed")

    # configure process
    def configure(self, env):
        import params
        env.set_params(params)

    # start process
    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        self.stop(env)
        File(params.nexus_pid_file,
             mode=0644,
             owner=params.nexus_user,
             group=params.nexus_group,
             content='')
        # start nexus server
        Execute(format("{nexus_home_dir}/nexus/bin/nexus start 2>&1 &"), user=params.nexus_user)
        # add pid to pid file
        Execute(
            'ps -ef | grep nexus | grep nexus | grep -v grep | awk \'{print $2}\' > ' + params.nexus_pid_file,
            user=params.nexus_user)

    # stop process
    def stop(self, env):
        import params
        env.set_params(params)
        # Kill the process of Nexus
        Execute ('ps -ef | grep nexus | grep -v grep | awk  \'{print $2}\' | xargs kill -9',
                 user=params.nexus_user, ignore_failures=True)
        File(params.nexus_pid_file,
             action = "delete",
             owner = params.nexus_user)

if __name__ == "__main__":
    NexusServer().execute()
