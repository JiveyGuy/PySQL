import csv
import sqlite3
import platform
import os
from tkinter import messagebox as msg_bx

# ==== globals 
DEBUG = True
DEFAULT_OUT_PATH = "output.csv"

# ==== funcs
def debug(msg):
	if DEBUG:
		print(f"DEBUG:: {msg}")

def err(msg):
	msg_bx.showerror(title="Errrrrr :(", message=msg)

def succ(msg):
	msg_bx.showinfo(title="Succc :)", message=msg)

def working_dir():
	return os.getcwd()

def default_output():
	# TODO add windows version
	path = os.getcwd()+"../output/"
	if not os.path.exists(path):
		debug("output not defined making dir")
		os.makedirs(path)
	return path


# from: https://stackoverflow.com/a/48706260
def get_os_download_dir():
		"""Returns the default downloads path for linux or windows"""
		if os.name == 'nt':
			import winreg
			sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
			downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
			with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
				location = winreg.QueryValueEx(key, downloads_guid)[0]
			return location
		else:
			return os.path.join(os.path.expanduser('~'), 'Downloads')

def load_cursor(state_db_path):
	conn = sqlite3.connect(state_db_path)
	cursor = conn.cursor()
	return (cursor, conn)

def do_sql( state_db_path,
	progress,
	cmd_str,
	output_file = DEFAULT_OUT_PATH ):
	debug("do_sql")
	progress.set(0)
	(cursor, conn) = load_cursor(state_db_path)
	progress.set(0.25)
	debug(f"load_cursor returned {(cursor, conn)}")
	cursor.execute(cmd_str)
	progress.set(0.50)
	with open(output_file, 'w', newline='') as csv_file:
		progress.set(0.60) 
		csv_writer = csv.writer(csv_file)
		progress.set(0.70)
		csv_writer.writerow([i[0] for i in cursor.description])
		progress.set(0.80) 
		csv_writer.writerows(cursor)
		progress.set(0.90)
	conn.close()
	progress.set(1)
	debug("execute done")