###############################################################################
# A simple EDMC plugin to automatically transmit CodexEntry data from the
# CMDR journal to the Intergalactic Astronomical Union for record keeping,
# and scientific purposes.
#
# Version 1.29 is no longer maintained.
# Please upgrade to EDMarketConnector 3.50 and ATEL-EDMC version 1.3x
#
###############################################################################

import sys
import os
import json
import requests
import urllib2
import Tkinter as tk
import ttk
from ttkHyperlinkLabel import HyperlinkLabel
import myNotebook as nb
import time
import re

this = sys.modules[__name__]	# For holding module globals
this.status = tk.StringVar()
this.edsm_setting = None
this.app_name = 'ATEL-EDMC'
this.installed_version = '1.29'
this.api = "https://ddss70885k.execute-api.us-west-1.amazonaws.com/Prod"
PADX = 10  # formatting

def plugin_start(plugin_dir):
    return 'ATEL'

def plugin_prefs(parent, cmdr, is_beta):
    frame = nb.Frame(parent)
    frame.columnconfigure(5, weight=1)
    nb.Label(frame, text="This release of ATEL-EDMC is no longer supported.").grid(columnspan=2, padx=PADX, sticky=tk.W)
    nb.label(frame, text="Please upgrade to EDMC 3.50 and ATEL-EDMC 1.3x.").grid(columnspan=2, padx=PADX, sticky=tk.W)
    HyperlinkLabel(frame, text='EDMC GitHub', background=nb.Label().cget('background'), url='https://github.com/Marginal/EDMarketConnector/releases\n', underline=True).grid(padx=PADX, sticky=tk.W)
    HyperlinkLabel(frame, text='ATEL-EDMC GitHub', background=nb.Label().cget('background'), url='https://github.com/Elite-IGAU/ATEL-EDMC/releases\n', underline=True).grid(padx=PADX, sticky=tk.W)
    return frame

def dashboard_entry(cmdr, is_beta, entry):
    this.cmdr = cmdr

def plugin_app(parent):
    this.parent = parent
    this.frame = tk.Frame(parent)
    this.frame.columnconfigure(2, weight=1)
    this.lblstatus = tk.Label(this.frame, anchor=tk.W, textvariable=status, wraplengt=255)
    this.lblstatus.grid(row=0, column=1, sticky=tk.W)
    this.status.set("Waiting for Codex discovery data...")
    return this.frame

def journal_entry(cmdr, is_beta, system, station, entry, state):

    if entry['event'] == 'CodexEntry':
        # Define variables to be passed along to submit ATEL Function
        this.timestamp=(format(entry['timestamp']))
        this.cmdr = cmdr
        entry['commanderName'] = cmdr
        this.entryid=(format(entry['EntryID']))
        this.name=(format(entry['Name']))
        this.name_stripped=(re.sub(";|\$|_Name", "", this.name))
        this.name_lower = str.lower(this.name_stripped)
        this.name_localised=(format(entry['Name_Localised']))
        this.system=(format(entry['System']))
        this.systemaddress=(format(entry['SystemAddress']))
        # do this the old fashioned way (version 1.08) with artisinal, hand-crafted JSON BS.
        CODEX_DATA = '{{ "timestamp":"{}", "EntryID":"{}", "Name":"{}", "Name_Localised":"{}", "System":"{}", "SystemAddress":"{}", "App_Name":"{}", "App_Version":"{}"}}'.format(entry['timestamp'], entry['EntryID'], this.name_lower, entry['Name_Localised'], entry['System'], entry['SystemAddress'], this.app_name, this.installed_version,)
        API_POST = requests.post(url = this.api, data = CODEX_DATA)
        # ATEL Button disabled in release 1.29
        this.status.set("Codex discovery data sent.\n "+this.name)
        # The print statements below can be uncommented to debug data transmission issues.
        # Log file located at: \user_name\AppData\Local\Temp\EDMarketConnector.log
        #print(str(this.api))
        #print(str(CODEX_DATA))
        #print(str(API_POST.request.body))
        #print(str(API_POST.text))
    else:
        # FSDJump happens often enough to clear the status window
        if entry['event'] == 'FSDJump':
                this.cmdr = cmdr
                entry['commanderName'] = cmdr
                this.system=(format(entry['StarSystem']))
                this.timestamp=(format(entry['timestamp']))
                this.status.set("Waiting for Codex discovery data...")

def plugin_stop():
    sys.stderr.write("Shutting down.")
