# -*- coding: utf-8 -*-
from constant import WORK_PATH, SYSTEM_CONFIG
from utils import check_file
import json
import os


class SystemConfig(object):
    config_parameter_name_list = [key for key in SYSTEM_CONFIG]  # 配置文件中会用到的变量

    def __init__(self):
        self.system_config_file = None

        self.check_sys_config_file_creation()
        self.read_sys_config_file()

    def get(self, key):
        """
            根据key获取配置文件中的参数
            如果key不存在,会报异常
        """
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError("配置文件中没有该参数 key='{}'".format(str(key)))

    def getAll(self):
        """
            获取配置文件中所有参数
        """
        config = {}
        for key in self.config_parameter_name_list:
            config[key] = self.get(key)
        return config

    def set(self, key, value):
        """
            根据key 设置配置文件中的参数,并且更新配置文件
            如果key不存在,会报异常
        """
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError("配置文件中没有该参数 key='{}'".format(str(key)))
        self.write_sys_config_file()

    def check_sys_config_file_creation(self):
        """
            检查配置文件是否创建,没有则生成
        """
        if not check_file(self._get_system_config_file_path()):
            self.create_sys_config_file()

    def create_sys_config_file(self):
        """
            新建配置文件
        """
        data = json.dumps(SYSTEM_CONFIG)
        with open(self._get_system_config_file_path(), 'x') as f:
            f.write(data)

    def read_sys_config_file(self):
        """
            读取配置文件,更新类中的参数
        """
        with open(self._get_system_config_file_path(), 'r') as f:
            data = json.loads(f.read())

        for key in self.config_parameter_name_list:
            # 根据SYSTEM_CONFIG里进行遍历
            if data.get(key) is None:
                # 如果配置文件中没有这个值,则使用默认的配置
                setattr(self, key, SYSTEM_CONFIG.get(key))
            else:
                setattr(self, key, data.get(key))

    def write_sys_config_file(self):
        config = {}
        for key in self.config_parameter_name_list:
            if self.get(key) is None:
                # 如果参数为空,则使用默认的配置
                config[key] = SYSTEM_CONFIG.get(key)
            else:
                config[key] = self.get(key)
        data = json.dumps(config)
        with open(self._get_system_config_file_path(), 'w') as f:
            f.write(data)

    def _get_system_config_file_path(self):
        """
            获取配置文件路径
        """
        if self.system_config_file is None:
            return SYSTEM_CONFIG['system_config_file']
        else:
            return self.system_config_file
