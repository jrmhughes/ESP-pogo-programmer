
class gcode_block:
        def __init__(self, file):
                self.file = file
        def fixes():
                self.data = (self.data).replace("G01 Z-0.0020", "M03 S255 ;line replaced")
                self.data = (self.data).replace("G00 Z0.1000", "M03 S1 ;line replaced")
                self.data = (self.data).replace("F", "G00 F")   #replace feedrate commands with ones Marlin understands
        def delete_ends():
                self.data = (self.data).replace("G00 X0Y0\r\nM05", "")

class operation(gcode_block):
        def __init__(self, file_name):
                gcode_block.__init__(open(file_name, "r"))
                self.data = (self.file).read()

class sequence(gcode_block):
        def __init__(self, file_name):
                gcode_block.__init__(open(file_name, "w+"))
                self.data = ""

def init_operations():
        FCu = operation("F.Cu.gbr_iso_cnc.gcode")

def modify_operations():
        

def collect_operations():
        output = operation(open("PCB.gcode", "w+"))
        output.data = ""

def main():
	define_operations()
	modify_operations()
	write_operations()

main()

