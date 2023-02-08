#  /$$$$$$$             /$$$$$$   /$$$$$$  /$$      
# | $$__  $$           /$$__  $$ /$$__  $$| $$      
# | $$  \ $$ /$$   /$$| $$  \__/| $$  \ $$| $$      
# | $$$$$$$/| $$  | $$|  $$$$$$ | $$  | $$| $$      
# | $$____/ | $$  | $$ \____  $$| $$  | $$| $$      
# | $$      | $$  | $$ /$$  \ $$| $$/$$ $$| $$      
# | $$      |  $$$$$$$|  $$$$$$/|  $$$$$$/| $$$$$$$$
# |__/       \____  $$ \______/  \____ $$$|________/
#            /$$  | $$                \__/          
#           |  $$$$$$/                              
#            \______/ 
# 
# Jason Ivey 2022 & 2023 for USDA-FS-FIA + Purdue DataMine

# ==== local imports
	# removed to nuitka will work
# import funcs as 
# import 

# ==== standard imports
import csv
import sqlite3
import platform
import os
import customtkinter as ctk
import webbrowser
import tkinter as tk
from tkinter import filedialog as file_diag
from tkinter import messagebox as msg_bx
from PIL import ImageTk, Image

# ==== globals 
DEBUG = True
DEFAULT_OUT_PATH = "output.csv"

# Default sql query in the box
DEFAULT_CMD =  """ /* Example SQL Command */ 
SELECT TREE.INVYR, TREE.TREE, PLOT.PLOT, TREE.SUBP, TREE.DIA, PLOT.LAT, PLOT.LON
FROM TREE
INNER JOIN PLOT ON TREE.PLT_CN=PLOT.CN """


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

# ==== global settings
# ctk.set_appearance_mode("dark")
ctk.set_widget_scaling(1.2)

# the deafult output dir (or make dir)
DEFAULT_OUTPUT_DIR = default_output()
DATAMART_URL = "https://experience.arcgis.com/experience/3641cea45d614ab88791aef54f3a1849/"

# ==== main definition of app (OOP :( but thats how its done )
class App(ctk.CTk):
	def __init__(self):
		super().__init__()

		self.configure_window()

		self.make_side_bar()

		self.make_top_bar()

		self.make_text_box()

		self.make_bottom_bar()

	def make_bottom_bar(self):
		# create output selector 
		self.entry = ctk.CTkEntry(self,
			placeholder_text=DEFAULT_OUTPUT_DIR)
		self.entry.grid(row=3,
			column=1,
			columnspan=1,
			padx=(10, 10),
			pady=(2, 2),
			sticky="nsew")

		self.exe_button = ctk.CTkButton(master=self, # fg_color="transparent",
			border_width=2,
			text="Exec+Output",
			text_color=("gray10", "#DCE4EE"),
			command = self.execute_button_callback )
		self.exe_button.grid(row=3,
			column=3,
			padx=(10, 10),
			pady=(2, 2),
			sticky="nsew")	

	def make_text_box(self):
		# create main text box
		self.sql_command_box = ctk.CTkTextbox(self,
			height = 400,
			corner_radius = 20)
		self.sql_command_box.grid(row=1,
			rowspan=2,
			column=1,
			columnspan=3,
			padx=(10, 10),
			pady=(2, 2),
			sticky="nsew")
		self.sql_command_box.insert("1.0", DEFAULT_CMD, tags=None)

	def make_top_bar(self):
		self.progressbar = ctk.CTkProgressBar(self,
			mode = "indeterminate",
			width=940, # progress_color="grey",
			height=20)
		self.progressbar.grid(row=0,
			column=1,
			columnspan=3,
			padx=(10, 10),
			pady=(2, 2),
			sticky="w")
		self.progressbar.set(0)

	# create sidebar frame with widgets
	def make_side_bar(self): 
		self.sidebar_frame = ctk.CTkFrame(self, 
			width=140, 
			corner_radius=0)
		self.sidebar_frame.grid(row=0,
			column = 0,
			rowspan = 4,
			sticky = "nsew")
		self.sidebar_frame.grid_rowconfigure(4, weight=1)

		self.logo_label = ctk.CTkLabel(self.sidebar_frame,
			text="PySQL",
			font=ctk.CTkFont(size=20, weight="bold"))
		self.logo_label.grid(row=0,
			column=0,
			padx=20,
			pady=(20, 10))

		self.file_button = ctk.CTkButton( self.sidebar_frame,
			text = "Open File(s)",
			command = self.file_button_callback )
		self.file_button.grid(row=1,
			column=0,
			padx=20,
			pady=10)

		self.datamart_button = ctk.CTkButton( self.sidebar_frame,
			text = "Datamart",
			command = self.open_data_mart )
		self.datamart_button.grid(row=2,
			column=0,
			padx=20,
			pady=10)

		self.make_or_reset_scroll_list()
		
	def make_or_reset_scroll_list(self):
		# create scrollable frame
		self.scrollable_frame = ctk.CTkScrollableFrame(self.sidebar_frame,
			label_text="Select Files")
		self.scrollable_frame.grid(row=3,
			column=0,
			padx=(20, 20),
			pady=(20, 0),
			sticky="nsew")
		self.scrollable_frame.grid_columnconfigure(0, weight=1)

	# one day
	# def set_proc_name(self, newname):
	#     from ctypes import cdll, byref, create_string_buffer
	#     libc = cdll.LoadLibrary('libc.so.6')
	#     buff = create_string_buffer(len(newname)+1)
	#     buff.value = newname
	#     libc.prctl(15, byref(buff), 0, 0, 0)

	def configure_window(self):
		# configure window
		self.title("PySQL")
		self.geometry(f"{1100}x{580}")
		# self.set_proc_name("PySQL")
		ico_path = working_dir() + "/src/PySQL.jpg"
		debug(f"ico_path = {ico_path}")
		img = ImageTk.PhotoImage(Image.open(ico_path))  # PIL solution
		self.tk.call('wm', 'iconphoto', self._w, img)
		

		# configure grid layout (4x3) (rowxcol)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure((0, 1, 2), weight=1)

	# ==== util funcs 
	def open_data_mart(self):
		webbrowser.open(DATAMART_URL,
			new=1)

	def file_button_callback(self):
		global current_file_paths
		# restart progress
		self.progressbar.stop() #todo animate decrease
		# self.progressbar.configure(progress_color="grey")
		# getting download dir path 
		start_path = get_os_download_dir() + "/"
		debug(f"file_button_callback, start_path = {start_path}")

		# selecting files
		current_file_paths = file_diag.askopenfilenames(initialdir = start_path,
			filetypes = [(".db", "*.db"), ("All Files", "*")])
		debug(f"current_file_paths = {current_file_paths}")
		
		# clear scrollable frame
		self.make_or_reset_scroll_list()

		# add selected files to scroll-frame
		for i, filepath in enumerate(current_file_paths):
			label = ctk.CTkLabel(master=self.scrollable_frame,
				text = ".../"+filepath.rsplit('/',1)[-1] )
			label.grid(row=i, column=0, padx=10, pady=(0, 20))

	def execute_button_callback(self):
		global current_file_paths
		self.progressbar.start() # start progress
		# self.progressbar.configure(progress_color="blue")
		try:
			cmd_str = self.sql_command_box.get("1.0","end")
			debug(f"sql_cmd = {cmd_str}")
			debug(f"execute_button_callback do_sql({current_file_paths})")
			state = do_sql(current_file_paths, self.progressbar, cmd_str)
			# todo error handling
			# if state == 0 :
				# self.progressbar.configure(progress_color="green")
			# elif state == 1 :
				# self.progressbar.configure(progress_color="yellow")
		except Exception as e:
			# self.progressbar.configure(progress_color="red")
			err(f"Failed to execute due to:\n{str(e)}")


		finally:
			self.progressbar.stop() # stop progress

# ==== main init
if __name__ == "__main__":
	app = App()
	app.mainloop()