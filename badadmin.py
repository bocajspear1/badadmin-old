import sys
import importlib
import os
import util.depends as depends

#temp = importlib.import_module("modules.apache.apache")

#something = getattr(temp, "apache")
#new_it = something()

	
VERSION = "0.1dev"
NAME="BadAdmin"

module_list = []

vars_list = {}

def load_module(name):
	
	if name != "":
		if not is_module(name):
			print ("Error loading module '" + name +  "':\nModule does not exist.")
		else:
			print ("Adding module '" + name + "'")
			module_list.append(name)
	else:
		print("No module name given")


def run_modules():
	if not len(module_list) > 0:
		print ("No modules added! Not running...")
		return
	else:
		# Stores references for module classes
		temp_list = {}
		
		# Parse list of modules
		for module in module_list:
			if is_module(module):
				temp_list[module] = get_module_ref(module)
				
				if module in vars_list:
					module_obj = {"name": module, "options": vars_list[module]}
				else:
					module_obj = {"name": module, "options": {}}
				
				depends.add_module(module_obj, temp_list[module].depends())
			else:
				print("Invalid module " + module)
		
		# Get install order, function returns array of strings
		print ("Resolving module dependecies...")
		install_list = depends.start_resolve()
		
		print ("Running modules...")
		for item in install_list:
			current_module = None
			if item in temp_list:
				print("Reuse")
				current_module = temp_list[item]
			else:	
				current_module = get_module_ref(item)
				
			current_module.run()
		print("Module execution complete! Restart for full effect")

# Verify the module exists				
def is_module(module_name):
	if module_name == "__pycache__":
		return False
	if os.path.isdir("modules/" + module_name) and os.path.isfile("modules/" + module_name + "/" + module_name + ".py"):
		return True
	else:
		return False		

def get_module_ref(module_name, options={}):
	if is_module(module_name):
		temp = importlib.import_module("modules." + module_name + "." +  module_name)
		
		ret_module = getattr(temp, module_name)()
		
		return ret_module

	else:
		print("Please specify a valid module")
		


def main():
	os_type = sys.platform
	if os_type != "linux":
		print ("\nOS currently not supported")
		sys.exit()
		
	
	if os.geteuid() != 0:
		print ("\nYou need to be root to run " + NAME)
		sys.exit()
	
	print("\nWelcome to " + NAME + ", a vulnerable OS creator. \nVersion: " + VERSION + "\n\n")
	
	input_val = ""
	
	while True:
		input_val = input("> ")
		
		input_val = input_val.strip()
		
		if input_val == "quit" or input_val == "exit":
			sys.exit()
		elif input_val == "help":
			print("No help yet")
		elif input_val == "run":
			print ("Are you sure you want to run the modules? The changes made by " + NAME + " cannot be reversed!")
			
			valid = False
			
			while valid == False:
				ans = input("(y|n)> ")
				
				ans = ans.strip()
				
				if ans == "y":
					run_modules()
					valid = True
				elif ans == "n":
					print("Not running\n")
					return
				else:
					print("Invalid option")
			
		else:
			input_list = input_val.split(" ")
			
			if input_list[0] == "module":
				if len(input_list) < 2:
					print("Invalid number of parameters")
				elif input_list[1] == "add" and len(input_list) == 3:
					load_module(input_list[2])
					
				elif input_list[1] == "list-added":
					print("Added modules: ")
					for module in module_list:
						print ("\t" + module)
						
				elif input_list[1] == "list-available":
					print("Available modules: ")
					
					for module in os.listdir("modules"):
						if os.path.isdir("modules/" + module) and module != "__pycache__":
							print ("\t" + module)
							
				elif input_list[1] == "show" :
					if len(input_list) == 3 and is_module(input_list[2]):
						
						current_module = get_module_ref(input_list[2])
						
						print (current_module.about())

						current_module = None
					else:
						print("Please specify a available module")
						
				else:
					print("Invalid parameters")
			elif input_list[0] == "run":
				print()
					
			#print(input_list)
	
	


main()
