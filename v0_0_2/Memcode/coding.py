#!/usr/bin/env python
"""
/* Copyright (C) YoYoDyne Systems, Inc - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Sajal Arora <saj.arora24@gmail.com>, June, 2017
 */
 
Project: Memcode
Author: sajarora
Date: 2017-06-21
Description:
"""
import os
import time

import rumps
import sqlite3

from os.path import expanduser


class Coding(object):
    INTERVAL = 5 * 60 * 60 # every 5 minutes for now

    def __init__(self):
        self.is_coding = False
        self.timer = rumps.Timer(self.make_record, Coding.INTERVAL)
        home = expanduser("~")
        self.folder = os.path.join(home, "Development", "Memcode", "data")
        self.make_dir(self.folder)
        self.session_id = None

        db_path = os.path.join(self.folder, 'database.db')
        self.conn = sqlite3.connect(db_path)
        self.setup_db()


    def setup_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS screenshots
                     (id integer primary key autoincrement, timestamp int, screen1Path text, screen2Path text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS camera
                             (id integer primary key autoincrement, timestamp int, cameraPath text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sessions
                                 (id integer primary key autoincrement, startTimestamp int, endTimestamp int)''')
        self.conn.commit()

    def toggle(self):
        if self.is_coding:
            self.stop_coding()
        else:
            self.start_coding()
        return self.is_coding

    def stop_coding(self):
        self.is_coding = False
        self.timer.stop()

        cursor = self.conn.cursor()
        cursor.execute('''UPDATE sessions SET `endTimestamp` = ? WHERE id = ?''', (int(time.time()), self.session_id))
        self.conn.commit()

    def start_coding(self):
        self.is_coding = True
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO sessions VALUES (NULL, ?, ?)", (int(time.time()), 0))
        self.session_id = cursor.lastrowid
        self.conn.commit()

        self.timer.start()

    def take_screenshot(self, timestamp=None):
        timestamp, path = self.prepare_timestamp_path(timestamp)
        pic_path1 = os.path.join(path, 'screen1.png') if path else 'screen1.png'
        pic_path2 = os.path.join(path, 'screen2.png') if path else 'screen2.png'
        os.system("screencapture %s %s" % (pic_path1, pic_path2))
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO screenshots VALUES (NULL, ?, ?, ?)", (timestamp, pic_path1, pic_path2))
        self.conn.commit()

    def snap_camera(self, timestamp=None):
        timestamp, path = self.prepare_timestamp_path(timestamp)
        pic_path = os.path.join(path, 'camera.png') if path else 'camera.png'
        os.system("imagesnap %s" % pic_path)
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO camera VALUES (NULL, ?, ?)", (timestamp, pic_path))
        self.conn.commit()

    def make_record(self, _):
        timestamp = int(time.time())
        # record time and screenshots into a directory
        path = os.path.join(self.folder, str(timestamp))
        self.make_dir(path)
        self.snap_camera(timestamp)
        self.take_screenshot(timestamp)

    def prepare_timestamp_path(self, timestamp=None):
        timestamp = timestamp or int(time.time())
        path = os.path.join(self.folder, str(timestamp))
        self.make_dir(path)
        return timestamp, path

    def make_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
