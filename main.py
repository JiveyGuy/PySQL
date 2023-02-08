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
import funcs as fn
import settings 

# ==== standard imports
import customtkinter as ctk
import webbrowser
import tkinter as tk
from tkinter import filedialog as file_diag
from PIL import ImageTk, Image

# ==== global settings
ctk.set_appearance_mode("dark")
ctk.set_widget_scaling(1.2)


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
			placeholder_text=settings.DEFAULT_OUTPUT_DIR)
		self.entry.grid(row=3,
			column=1,
			columnspan=1,
			padx=(10, 10),
			pady=(2, 2),
			sticky="nsew")

		self.exe_button = ctk.CTkButton(master=self,
			fg_color="transparent",
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
		self.sql_command_box.insert("1.0", settings.DEFAULT_CMD, tags=None)

	def make_top_bar(self):
		self.progressbar = ctk.CTkProgressBar(self,
			mode = "indeterminate",
			width=940,
			progress_color="grey",
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
		# ico_path = fn.working_dir() + "/PySQL.ico"
		img = ImageTk.PhotoImage(Image.open("PySQL.jpg"))  # PIL solution
		self.tk.call('wm', 'iconphoto', self._w, img)
		# fn.debug(f"ico_path = {ico_path}")

		# configure grid layout (4x3) (rowxcol)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure((0, 1, 2), weight=1)

	# ==== util funcs 
	def open_data_mart(self):
		webbrowser.open(settings.DATAMART_URL,
			new=1)

	def file_button_callback(self):
		global current_file_paths
		# restart progress
		self.progressbar.stop() #todo animate decrease
		self.progressbar.configure(progress_color="grey")
		# getting download dir path 
		start_path = fn.get_os_download_dir() + "/"
		fn.debug(f"file_button_callback, start_path = {start_path}")

		# selecting files
		current_file_paths = file_diag.askopenfilenames(initialdir = start_path,
			filetypes = [(".db", "*.db"), ("All Files", "*")])
		fn.debug(f"current_file_paths = {current_file_paths}")
		
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
		self.progressbar.configure(progress_color="blue")
		try:
			cmd_str = self.sql_command_box.get("1.0","end")
			fn.debug(f"sql_cmd = {cmd_str}")
			fn.debug(f"execute_button_callback do_sql({current_file_paths})")
			state = fn.do_sql(current_file_paths, self.progressbar, cmd_str)
			# todo error handling
			if state == 0 :
				self.progressbar.configure(progress_color="green")
			elif state == 1 :
				self.progressbar.configure(progress_color="yellow")
		except Exception as e:
			self.progressbar.configure(progress_color="red")
			fn.err(f"Failed to execute due to:\n{str(e)}")


		finally:
			self.progressbar.stop() # stop progress

# ==== main init
if __name__ == "__main__":
	app = App()
	app.mainloop()