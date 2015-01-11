from ..base import base

class apache(base):
	
		
	def __init__(self) :
		print("Loading apache")

		
		self.get_storage_item("stuff")
		
	def name(self):
		return "Test Apache Module"
	
	def version(self):
		return "0.1dev"
		
	def author(self):
		return "Jacob Hartman"
	
	
	def about(self):
	
		about_me = self.header()
		about_me += "A test Apache module"
	
		return 	about_me
		
	def run(self, options=[]):
		print("running")
		
		print(self.my_os())
	

	
		