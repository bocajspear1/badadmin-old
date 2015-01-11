import abc
import subprocess
import os
import re
import random
import shutil
import string
import platform

class command():
	def run(self, command_string, send_list=[]):
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		
		stdin_string = ""
		for value in send_list:
			stdin_string += value + "\n"
		
		output, error = proc.communicate(stdin_string, timeout=15)
		return (output, error)

# class pkg_manager():
# 	
# 	my_pkg_manager = ""
# 
# 	def __init__(self):
# 		
# 	
# 				
# 	def install(self, names, version):
# 		manager_command = command()
# 		
# 		if "yum" in names and self.my_pkg_manager == "yum":
# 			manager_command.run("yum", ["install", names['yum']])
# 		elif "apt" in names and self.my_pkg_manager == "apt":
# 			manager_command.run("apt-get", ["update"])
# 			manager_command.run("apt-get", ["install", name])
# 			
# 	
# 	def remove(self, version):
# 		pass
# 
# 	def add_repo(self, path):
# 		pass
# 
# 	def remove_repo(self, path):
# 		pass
		
class file():
	
	def __init__(self, filename):
		if filename.strip() != "":
			self.file = filename
		else:
			raise ValueError("File cannot be blank")
	
	def create(self):
		try:
			if self.file != None:
				with open(self.file, 'w+') as content_file:
					pass
		except FileNotFoundError:
			print ("Could not find selected file")
	
	def remove(self):
		try:
			if self.file != None:
				os.remove(self.file)
		except FileNotFoundError:
			print ("Could not find selected file")
	
	def get_contents(self):
		try:
			if self.file != None:
				content = ""
				with open(self.file, 'r') as content_file:
					content = content_file.read()
				return content	
		except FileNotFoundError:
			print ("Could not find selected file")
	
	def write_contents(self, contents):
		try:
			if self.file != None:
				with open(self.file, 'w+') as content_file:
					content_file.write(contents)
		except FileNotFoundError:
			print ("Could not find selected file")
	
	def move(self, to_location):
		shutil.move(self.file, to_location)
	
	def copy(self, to_location, keep=False):
		try:
			if keep == False:
				shutil.copyfile(self.file, to_location)
			else:
				shutil.copy2(self.file, to_location)
		except shutil.Error:
			print("ERROR - Could not copy file")
	
	
	def replace(self, search, replace):
		file_contents = self.get_contents()
		
		file_lines = file_contents.split("\n")
		
		for i in range(len(file_lines)):
			file_lines[i] =file_lines[i].replace(search, replace)
		
		new_contents = "\n".join(file_lines)
		
		self.write_contents(new_contents)
	
	def regex_replace(self, search, replace):
		file_contents = self.get_contents()
		
		file_lines = file_contents.split("\n")
		
		for i in range(len(file_lines)):
			file_lines[i] = re.sub(search, replace, file_lines[i])
		
		new_contents = "\n".join(file_lines)
		
		self.write_contents(new_contents)

	def append_content(self, content):
		try:
			if self.file != None:
				with open(self.file, 'a') as content_file:
					content_file.write(contents)
		except FileNotFoundError:
			print ("Could not find selected file")

		
	def append_file_to(self, content, append_to):
		pass
	
	def exists(self):
		return os.path.isfile(self.file)
	
class dir():
	def __init__(self, dirname):
		if filename.strip() != "":
			self.dir = dirname
		else:
			raise ValueError("Directory cannot be blank")

	def list(self):
		if os.path.isdir(self.dir) and self.dir != None:
			os.listdir(self.dir)
	
	def create(self):
		if self.dir != None:
			os.makedirs(self.dir)

	def remove(self):
		if self.dir != None:
			shutil.rmtree(self.dir)
	
	def copy(self, to_location):
		if self.dir != None:
			shutil.copytree(self.dir, to_location)
			
	def move(self, to_location):
		if self.dir != None:
			shutil.move(self.dir, to_location)
			
	def exists(self):
		return os.path.isdir(self.file)
			
class base():
	__metaclass__ = abc.ABCMeta
	
	dependencies = []
	
	def __init__(self):
		print ("Init base")
	
	@abc.abstractmethod
	def name(self):
		raise NotImplementedError 
	
	@abc.abstractmethod
	def version(self):
		raise NotImplementedError 
	
	@abc.abstractmethod
	def author(self):
		raise NotImplementedError 
	
	def header(self):
		return "\nModule: " + self.name() + "\nVersion: " + self.version() + "\nBy " + self.author() + "\n\n"
	
	def about(self):
		raise NotImplementedError 
	
	def add_dependency(self, name, options={}):
		self.dependencies.append({"name": name, "options": options})
		
	def depends(self):
		return self.dependencies
	
	@abc.abstractmethod
	def req_vars(self):
		raise NotImplementedError
	
	@abc.abstractmethod
	def run(self):
		raise NotImplementedError	
	
	def get_module(self, module_name):
		module_name = module_name.replace(".","").replace("/","").replace("\\", "")
		if self.module_exists(module_name):
			temp = importlib.import_module(module_name + "." +  module_name)
						
			current_module = getattr(temp, module_name)()
			return current_module

	def module_exists(self, module_name):
		module_name = module_name.replace(".","").replace("/","").replace("\\", "")
		if module_name != "__pycache__" and os.path.isdir(module_name):
			return True
		else:
			return False
	
	def pkg_manager(self):
		return pkg_manager()
		
	def command(self, command, send_list=[]):
		return command().run(command,send_list)
	
	def file(self, filename):
		return file(filename)
	
	def dir(self, dirname):
		return dir(dirname)
	
	def array_random(self, array):
		array_size = len(array)
		r_key = random.randrange(0, array_size)
		return array[r_key]
	
	def random_number(self, max):
		return random.randrange(0, max)
		
	def will_do(self):
		r_value = random.randrange(0, 10) + 1
		
		true_val = [1,3,5,7,9]
		false_val = [2,4,6,8,10]
		
		if r_value in true_val:
			return True
		elif r_value in false_val:
			return
	
	def random_string(self, min=2, max=10):
	
		num = self.random_number(max - min)
		
		run_times = num + min
		
		rand_string = ""
		
		for i in range(run_times):
			rand_string += random.choice(string.letters)
	
		return rand_string
	
	# Get items stored in the module /storage directory
	def get_storage_item(self, item):
		storage_dir = os.path.dirname(os.path.realpath(__file__)) + "/" + self.__class__.__name__ + "/storage"
		
		item_path = storage_dir + "/" + item
		
		if os.path.isdir(item_path):
			return dir(item_path)
		elif os.path.isfile(item_path):
			return file(item_path)
	
	
	def download(self, path):
		try:
			response = urllib.request.urlopen(link)

			file_name, headers = urllib.request.urlretrieve(path)
			print("Placed in " + file_name)
			
			return file(file_name)

		except urllib.error.HTTPError as e:
			print (e)
			return None
		except Exception as e:
			print (e)
			return None
		
	def my_os(self):
		
		os_info = {
			"distro_name": None,
			"distro_version": None,
			"distro_codename": None,
			"pkg_manager": None
		}
		
		dist_info = platform.linux_distribution()
		
		os_info["distro_name"] = dist_info[0]
		os_info["distro_version"] = dist_info[1]
		os_info["distro_codename"] = dist_info[2]
		
		pkg_manager_list = [
		'yum',
		'apt-get'
		]
		
		for manager in pkg_manager_list:
			try:
				result = subprocess.call(manager, stdout=subprocess.DEVNULL, stderr=None)
				if result == 0:
					os_info["pkg_manager"] = manager
			except FileNotFoundError:
				pass
		
		return os_info