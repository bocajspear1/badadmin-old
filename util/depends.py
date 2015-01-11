# Logarithm base off of http://www.electricmonk.nl/log/2008/08/07/dependency-resolving-algorithm/

# List of module names
install_list = []

# Dict of module names to objects: {"name": "", "options": {"version": "", ...}}
module_list = {}

# Dict of module names to option
options_list = {}

def add_module(module, module_depends):
	# Add module to list
	module_list[module['name']] = module_depends
	
	# Manage the options of the module
	if 'options' in module:
		resolve_options(module['name'], module['options'] )
		
	for dependency in module_depends:
		if 'options' in dependency:
			resolve_options(dependency['name'], dependency['options'] )
			

def start_resolve():
	for module_name in module_list:
		#print(module_list)
		print ("\nStart resolve for " + module_name)
		__resolve(module_name, [])
	return install_list

def get_options_list():
	pass
	
def resolve_options(module_name, options):
	pass
	
def __resolve(module_name, seen):
	print("Resolving " + module_name)
	if module_name in seen:
		raise Exception("Circular dependency found for " + module_name)
	seen.append(module_name)
	print("Install List: ", install_list)
	print(seen)
	if module_name in module_list and not module_name in install_list:
		for module_dep in module_list[module_name]:
			if not module_dep['name'] in install_list:
				__resolve(module_dep['name'], seen)
	if not module_name in install_list:
		install_list.append(module_name)
		
		
# >1.2.6 and >=1.3.0
def compare_version(ver_string1, ver_string2):
	
	
	done = False
	winner = None
	
	# Get numerical comparison
	comp_1 = get_comparison(ver_string1)
	comp_2 = get_comparison(ver_string2)
	
	c_ver_string1 = clean_ver_string(ver_string1)
	c_ver_string2 = clean_ver_string(ver_string2)
	
	ver_array1 = c_ver_string1.split(".")
	ver_array2 = c_ver_string2.split(".")
	
	if len(ver_array1) != len(ver_array2):
		while len(ver_array1) < len(ver_array2):
			ver_array1.append("0")
		while len(ver_array2) < len(ver_array1):
			ver_array2.append("0")
	index = 0
	
	while index < len(ver_array1) and done == False:
		if ver_array1[index].isdigit() and ver_array2[index].isdigit():
			if int(ver_array1[index]) == int(ver_array2[index]):
				if index + 1 == len(ver_array1):
					# We are exactly the same, check if non-equal is in the comparison
					if comp_1 == 2 or comp_2 == 2 or comp_2 == -2 or comp_1 == -2:
						winner = False
						return winner
					else:
						#winner =
						return winner
				else:
					pass
			elif int(ver_array1[index]) < int(ver_array2[index]):
					
				# if 1 is not > or >= when smaller, we fail out
				if comp_1 != 1 and comp_1 != 2:
					winner = False
					return winner
				else:
					winner = ver_string2
					return winner
					
			elif int(ver_array1[index]) > int(ver_array2[index]):
				# if 2 is not > or >= when smaller, we fail out
				if comp_2 != 1 and comp_2 != 2:
					winner = False
					return winner
				else:
					winner = ver_string1
					return winner


def clean_ver_string(ver_string):
	ver_string = ver_string.replace("<","")
	ver_string = ver_string.replace(">","")
	ver_string = ver_string.replace("=","")

	return ver_string

def get_comparison(ver_string):
	if ver_string[:1] == "<":
		print ("less than")
		if ver_string[1:2] == "=":
			print("and equal to")
			return -1
		else:
			return -2
	elif ver_string[:1] == ">":
		print ("greater than")
		if ver_string[1:2] == "=":
			print("and equal to")
			return 1
		else:
			return 2
	elif ver_string[:1] == "=":
		return 0
	else:
		pass