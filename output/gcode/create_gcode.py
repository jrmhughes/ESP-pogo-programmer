class gcode_block:
        def __init__(self, data):
                self.data = data
        def fixes(self):
                self.data = (self.data).replace("G01 Z-0.0020", "M03 S255 ;fixes")
                self.data = (self.data).replace("G00 Z0.1000", "M03 S1 ;fixes")
                self.data = (self.data).replace("F", "G00 F")   #replace feedrate commands with ones Marlin understands
        def delete_ends(self):
                self.data = (self.data).replace("G00 X0Y0\nM05", ";G00 X0Y0; delete_ends\r\n;M05; delete_ends")
        def read_from_disk(self, read_file_name, n_iterations):
                with open(read_file_name, "r") as read_file:
                        read_data = read_file.read()
                        for i in range(n_iterations):   
                                self.data += read_data
        def save_to_disk(self, save_file_name):
                with open(save_file_name, "w+") as save_file:
                        save_file.write(self.data)


#main
def main():
        paint = gcode_block("")
        #files to collect
        paint.read_from_disk("start.gcode", 1)
        paint.read_from_disk("F.Cu.gbr_iso_cnc.gcode", 1)
        paint.read_from_disk("paint.write_file_to_file", 1)
        paint.read_from_disk("end.gcode", 1)

        paint.fixes()
        paint.delete_ends()
        paint.save_to_disk("PCB_paint.gcode")

        
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
        #cutting.append(drl_mill_1, 1)
        cutting.append(cutout_1, 1)

        cutting.fixes()
        cutting.delete_ends()
        (cutting.file).write(start.data)
        for i in range(500):
                cutting.write_to_file()
        (cutting.file).write(end.data)

#run
main()

