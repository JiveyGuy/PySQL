# Jason Ivey 2022 & 2023 for USDA-FS-FIA + Purdue DataMine
import customtkinter as ctk 
import funcs as fn
from tkinter import filedialog as fd


DEFAULT_CMD =  """ /* Example SQL Command */ 
SELECT TREE.INVYR, TREE.TREE, PLOT.PLOT, TREE.SUBP, TREE.DIA, PLOT.LAT, PLOT.LON
FROM TREE
INNER JOIN PLOT ON TREE.PLT_CN=PLOT.CN """

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
	def __init__(self):
		super().__init__()

		self.title("PySQL")
		self.minsize(800, 640)

		self.file_button = ctk.CTkButton( master=self,
			text = "Open File",
			command = self.file_button_callback )

		self.exe_button = ctk.CTkButton( master=self,
			text = "Run SQL",
			command = self.execute_button_callback )

		self.sql_command_box = ctk.CTkTextbox(master=self,
			width = 750,
			height = 500,
			border_spacing = 10,
			corner_radius = 20,
			wrap = "none" )
		self.sql_command_box.insert('1.0', DEFAULT_CMD, tags=None)

		self.progressbar = ctk.CTkProgressBar(master=self,
			width = 750,
			height = 10 )
		self.progressbar.set(0)
		
		self.file_button.grid(row=0,column=0,padx=5,pady=10)
		self.sql_command_box.grid(row=1,column=0,padx=40, pady=10)
		self.exe_button.grid(row=2,column=0,padx=5)
		self.progressbar.grid(row=3,column=0,pady=20)

	def file_button_callback(self):
		global current_file_path
		start_path = fn.get_os_download_dir() + "/"
		fn.debug(f"file_button_callback, start_path = {start_path}")
		current_file_path = fd.askopenfilename(initialdir = start_path,
			filetypes = [('.db', '*.db'), ('All Files', '*')])
		fn.debug(f"current_file_path = {current_file_path}")

	def execute_button_callback(self):
		self.progressbar.set(0)
		global current_file_path
		cmd_str = self.sql_command_box.get('1.0',"end")
		fn.debug(f"sql_cmd = {cmd_str}")
		fn.debug(f"execute_button_callback do_sql({current_file_path})")
		state = fn.do_sql(current_file_path, self.progressbar, cmd_str)

		# todo error handling
		if state == 0 :
			pass

if __name__ == "__main__":
	app = App()
	app.mainloop()