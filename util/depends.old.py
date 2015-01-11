

item_list = []

options_list = {}

depends_list = {}

def get_list():
	return item_list

	

def add_item(main, requires):

	main_name = main['name']
	
	#main_options = main['options']
	
	# Check if added item is already in list
	if main_name in item_list and main_name in options_list:
		print ("Error: Multiple options found")
	elif main_name in item_list:
		print ("Ignoring adding " + main_name + ", already is in install queue")
	else:
		item_list.append(main_name)
		depends_list[main_name] = requires
	
	#print (requires)
	if isinstance(requires, list):
		for require in requires:
			if require['name'] in item_list and require['name'] in options_list:
				print ("Error: Multiple options found")
			elif require['name'] in item_list and get_location(require['name']) <= get_location(main_name):
				print ("Ignoring adding " + require['name'] + ", already is in install queue")
			elif require['name'] in item_list and get_location(require['name']) > get_location(main_name):
				
				switch_out = require['name']
				
				inner_start = get_location(switch_out)
				inner_end = get_location(main_name) + 1
				
				item_list.remove(switch_out)
				location = get_location(main_name)
				item_list.insert(location, switch_out)
				
				counter = inner_start
				
				while counter >= inner_end:
					
					
					current_item = item_list[counter]
					
					print ("Checking " + current_item)
					
					print (main_name)
					
					print (depends_list)
					
					if switch_out in depends_list:
						for item in depends_list[switch_out]:
							print (item)
							if item['name'] == current_item:
								item_list.remove(current_item)
								item_list.insert(location, current_item)
						
					
					counter = counter - 1
					
			else:
				location = get_location(main_name)
				item_list.insert(location, require['name'])
	else:
		location = get_location(main_name)
		item_list.insert(location, requires['name'])
	
	print()
	print(item_list)
	print()
	
def get_location(item):
	try:
		return item_list.index(item)
	except:
		return -1