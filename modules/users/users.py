from ..base import base


class users(base):
	
	random_names = [
		{"username": "admin"},
		{"username": "ppiper"},
		{"username": "dvader"},
		{"username": "lskywalker"},
		{"username": "toor"},
		{"username": "ser1vce"},
		{"username": "n0body"},
		{"username": "nob0dy"},
		{"username": "deamon"}
	]
	
	random_password = [
		"password",
		"12345678",
		"changeme",
		"p@ssw0rd",
		"computer",
		"linuxiscool",
		"01234567",
		"0987654321"
	]
	
	def name(self):
		return "Linux User Module"
	
	def version(self):
		return "0.1dev"
		
	def author(self):
		return "Jacob Hartman"
	
	def about(self):
	
		about_me = self.header()
		about_me += "This module creates misconfigurations on users and groups"
	
		return 	about_me
	
	def __init__(self):
		pass
	
	def run(self, maxitems=0, minitems=3, disablelist=[]):
		
		user_list = self.get_user_list()
		
		# Set shells and passwords for accounts
		if not "changeshell" in disablelist:
			for i in range(self.random_number(len(user_list))):
				done_list = []
				
				r_user = self.array_random(user_list)
				
				while r_user[0] in done_list:
					r_user = self.array_random(user_list)
				
				if r_user[1] < 10000 and self.will_do():
					self.set_password(r_user[0], 'password')
					self.change_shell(r_user[0], "/bin/bash")
				
		# Add extra users to device
		if not "randuser" in disablelist:
			if self.will_do():
				random_user = self.array_random(self.random_names)
				self.add_user(random_user)
				
				
		# Add false root user to device
		if not "falseroot" in disablelist:
			if self.will_do():
				random_user = self.array_random(self.random_names)
				
				# Don't override an existing user
				while self.user_exists(random_user):
					random_user = self.array_random(self.random_names)
					
				self.add_user(random_user, uid=0, unique=False)
		
		
		print(self.name() + " done")
	
	# Gets either a preset bas password, or returns a random password
	def random_password(self):
		if self.will_do():
			return self.array_random(random_password)
		else:
			return self.random_string(min=6, max=10)
		

	def user_exists(self, username):
		user_list = get_user_list()
		
		for user in user_list:
			if user[0] == username:
				return True
		return False
		
	def get_user_list(self):
		passwd_file = self.file("/etc/passwd")
		
		passwd_content = passwd_file.get_contents()
		passwd_lines = passwd_content.split("\n")
		
		user_list = []
		
		for line in passwd_lines:
			username = line.split(":")[0]
			uid = line.split(":")[2]
			user_list.append((username, uid))
		
	def change_shell(self, username, shell):
		passwd_file = self.file("/etc/passwd")
		passwd_file.regex_replace("^(" + username + ":.*):[^:]*$", "\\1:" + shell)
	
	def set_password(self, username, password):
		self.command("passwd " + username, [password, password])
	
	def add_user(self, username, uid=-1, gid="" ,homedir="", makehomedir=True, groups=[], unique=True, system=False, makeusergroup=True, shell=""):
		command_string = "useradd"
		
		if uid != -1:
			if isinstance( uid, int ):
					command_string += " -u " + str(uid)
			else:
				raise ValueError("UID must be an integer")
			
		if gid != "":
			command_string += " -g " + str(gid)
		
		if homedir != "":
			command_string += " -d " + str(homedir)
		
		if makehomedir == True:
			command_string += " -m" 
		elif makehomedir == False:
			command_string += " -M"
		else:
			raise ValueError("Invalid makehomedir value")
		
		if len(groups) > 0:
			command_string += " -G "
			for i in range(len(groups)):
				if i == 0:
					command_string += str(groups[i])
				else:
					command_string += "," + str(groups[i])
		
		if unique == False:
			command_string += " -o"
		
		if system == True:
			command_string += " -r"
		
		if makeusergroup == True:
			command_string += " -U"
		elif makeusergroup == False:
			command_string += " -N"
		else:
			raise ValueError("Invalid makeusergroup value")
			
		if shell != "":
			test = self.file(shell)
			if test.exists():
				command_string += " -s " + shell
			else:
				raise ValueError("Shell " + str(shell) + "could not be found")
				
		command_string += " " + username
		