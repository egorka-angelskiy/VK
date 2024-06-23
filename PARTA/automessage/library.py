from flask import Flask, render_template, request, redirect
import sqlite3
import vk
import datetime
import traceback
from prettytable import from_db_cursor
import time
import webbrowser
import os

dict_vk_error = {
	'902': '',
	'7': '',
	'4': ''
}