#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Takuma Yagi <yagi@ks.cs.titech.ac.jp>
#
# Distributed under terms of the MIT license.

import os
import errno
import datetime
from logging import getLogger, StreamHandler, FileHandler, Formatter, INFO
from arghelper import save_args_as_json


class MLLogger(object):
    """
    General logger for machine learning experiment.
    Usage:
        from mllogger import MLLogger
        logger = MLLogger("outputs", "latest_log.txt")
        logger.info("Test message")
        save_dir = logger.get_savedir()
    """
    def __new__(self, root_dir=None,
            tmplog_name="latest_log.txt", level=INFO, init=True):
        if not hasattr(self, "__instance__"):
            self.__instance__ = super(MLLogger, self).__new__(self)
            self.level = level
            self.tmplog_name = tmplog_name
            self.logger = getLogger('main')
            self.root_dir = root_dir

            if init:
                self.initialize(self.__instance__, root_dir)
        return self.__instance__

    def initialize(self, root_dir=None, dir_name=None):
        if self.root_dir is None and root_dir is not None:
            self.root_dir = root_dir
        elif self.root_dir is None and root_dir is None:
            self.root_dir = "outputs"
        date = datetime.datetime.now()

        # Use current date as default output folder name
        self.dir_name = date.strftime('%y%m%d_%H%M%S') if dir_name is None else dir_name
        self.save_dir = os.path.join(self.root_dir, self.dir_name)

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        self.log_fn = os.path.join(self.save_dir, 'log_{}.txt'.format(self.dir_name))
        self.logger.setLevel(self.level)

        # CONSOLE
        sh = StreamHandler()
        sh.setLevel(self.level)
        self.logger.addHandler(sh)

        # FILE
        fh = FileHandler(self.log_fn, 'w')
        fh.setFormatter(Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        fh.setLevel(self.level)
        self.logger.addHandler(fh)

        # Create symlink: if exists, remove old symlink
        try:
            os.symlink(self.log_fn, self.tmplog_name)
        except OSError, e:
            if e.errno == errno.EEXIST:
                os.remove(self.tmplog_name)
                os.symlink(self.log_fn, self.tmplog_name)

    def set_level(self, level):
        self.level = level
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def get_savedir(self):
        return self.save_dir

    def save_args(self, args):
        save_args_as_json(args, os.path.join(self.save_dir, "args.json"))
