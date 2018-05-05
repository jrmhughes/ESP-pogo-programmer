#gcode_block class and subclasses
class gcode_block:
	def __init__(self, file):
		self.file = file
	def fixes(self):
		self.data = (self.data).replace("G01 Z-0.0020", "M03 S255 ;fixes")
		self.data = (self.data).replace("G00 Z0.1000", "M03 S1 ;fixes")
		self.data = (self.data).replace("F", "G00 F")   #replace feedrate commands with ones Marlin understands
	def delete_ends(self):
		self.data = (self.data).replace("G00 X0Y0\nM05", ";G00 X0Y0; delete_ends\r\n;M05; delete_ends")
	def append(self, gcode_block_to_append, number_of_passes):
		for i in range(number_of_passes):
			self.data = self.data + gcode_block_to_append.data

class operation(gcode_block):
	def __init__(self, file_name):
		gcode_block.__init__(self, open(file_name, "r"))        #open file
		self.data = (self.file).read()                          #read to data string

class sequence(gcode_block):
	def __init__(self, file_name):
		gcode_block.__init__(self, open(file_name, "w+"))       #create new file
		self.data = ""                                          #create blank data string
	def write_to_file(self):
		(self.file).write(self.data)

#main
def main():
	#initialise operations
	#start and end
	start = operation("start.gcode")
	end = operation("end.gcode")
	#others
	FCu = operation("F.Cu.gbr_iso_cnc.gcode")
	
	#modify operations

	#collect operations
	output = sequence("PCB.gcode")

	output.append(FCu, 1)
	
	#modify sequence
	output.fixes()
	output.delete_ends()
	output.data = start.data + output.data + end.data       #attach start and end gcode

	output.write_to_file()

#run
main()

