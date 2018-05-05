#gcode_block class and subclasses
class gcode_block:
	def __init__(self, file):
		self.file = file
	def fixes():
		self.data = (self.data).replace("G01 Z-0.0020", "M03 S255 ;line replaced")
		self.data = (self.data).replace("G00 Z0.1000", "M03 S1 ;line replaced")
		self.data = (self.data).replace("F", "G00 F")   #replace feedrate commands with ones Marlin understands
	def delete_ends():
		self.data = (self.data).replace("G00 X0Y0\r\nM05", "")
	def append(gcode_block_to_append, number_of_passes):
		for i in xrange(number_of_passes):
			self.data = self.data + gcode_block_to_append

class operation(gcode_block):
	def __init__(self, file_name):
		gcode_block.__init__(self, open(file_name, "r"))      #open file
		self.data = (self.file).read()                  #read to data 

class sequence(gcode_block):
	def __init__(self, file_name):
		gcode_block.__init__(self, open(file_name, "w+"))       #create new file
		self.data = ""                                          #create blank data variable
	def write_to_file():
		(self.file).write(self.data)

#main functions
def init_operations():
	FCu = operation("F.Cu.gbr_iso_cnc.gcode")

#def modify_operations():
	

def collect_operations():
	output = sequence("PCB.gcode")
	output.append(FCu, 1)
	

#main
def main():
	init_operations()
	#modify_operations()
	collect_operations()
	output.write_to_file()

#run
main()

