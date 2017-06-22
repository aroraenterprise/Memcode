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

import rumps

from coding import Coding

coding = Coding()
app = rumps.App('Memcode', menu=['Start Coding', 'Take Screenshot', 'Snap Camera'])

@rumps.clicked("Start Coding")
def toggle_coding(sender):
    if coding.toggle(): # returns true then coding
        app.title = "Monkey Coding..."
        sender.title = 'Stop Coding'
    else:
        app.title = "Memcode"
        sender.title = 'Start Coding'


@rumps.clicked('Take Screenshot')
def screenshot(sender):
    coding.take_screenshot()

@rumps.clicked('Snap Camera')
def screenshot(sender):
    coding.snap_camera()

if __name__ == "__main__":
    app.run()