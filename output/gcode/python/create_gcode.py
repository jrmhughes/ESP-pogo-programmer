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

class setup(gcode_block):
        def __init__(self, file_name):
                gcode_block.__init__(self, open(file_name, "w+"))       #create new file
                self.data = ""                                          #create blank data string
        def write_to_file(self):
                (self.file).write(self.data)
        def add_ends(self, start, end):
                self.data = start.data + self.data + end.data
        def finish(self, start, end):
                self.fixes()
                self.delete_ends()
                self.add_ends(start, end)
                self.write_to_file()
                

#main
def main():
        #initialise operations
        #start and end
        start = operation("start.gcode")
        end = operation("end.gcode")
        #others
        FCu = operation("F.Cu.gbr_iso_cnc.gcode")
        drl_mill = operation("ESP pogo programmer.drl_mill_cnc.gcode")
        cutout = operation("ESP pogo programmer-F.Cu.gbr_cutout_cnc.gcode")
        
        #modify operations

        #collect operations
        paint = setup("PCB_paint.gcode")
        paint.append(FCu, 1)
        paint.append(drl_mill, 1)
        paint.append(cutout, 1)
        #apply modifications and write to file
        paint.finish(start, end)

        drl_mill_1 = operation("ESP pogo programmer.drl_mill_cnc_1.gcode")
        cutout_1 = operation("ESP pogo programmer-F.Cu.gbr_cutout_cnc_1.gcode")
        
        cutting = setup("PCB_cutting.gcode")
        cutting.append(drl_mill_1, 1)
        cutting.append(cutout_1, 1)

        cutting.fixes()
        cutting.delete_ends()
        (cutting.file).write(start.data)
        for i in range(500):
                cutting.write_to_file()
        (cutting.file).write(end.data)

#run
main()

