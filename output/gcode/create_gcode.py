class gcode_block:
        def __init__(self, data):
                self.data = data
        def fixes(self):
                self.data = (self.data).replace("G01 Z-0.0020", "M03 S255 ;fixes")
                self.data = (self.data).replace("G00 Z0.1000", "M03 S1 ;fixes")
                self.data = (self.data).replace("F", "G00 F")   #replace feedrate commands with ones Marlin understands
        def delete_ends(self):
                self.data = (self.data).replace("G00 X0Y0\nM05", ";G00 X0Y0; delete_ends\r\n;M05; delete_ends")
        def read_from_disk(self, read_file_name, n_iterations = 1):
                with open(read_file_name, "r") as read_file:
                        read_data = read_file.read()
                        for i in range(n_iterations):   
                                self.data += read_data
        def read_from_gcode_block(self, read_block, n_iterations = 1):
                self.data += read_block.data
        def save_to_disk(self, save_file_name):
                with open(save_file_name, "w+") as save_file:
                        save_file.write(self.data)


#setups

def create_paint(output_name):
        
        #paint
        paint = gcode_block("")

        paint.read_from_disk("start.gcode")
        paint.read_from_disk("F.Cu.gbr_iso_cnc.gcode")
        paint.read_from_disk("drl_cnc.gcode")
        paint.read_from_disk("end.gcode")

        paint.fixes()
        paint.delete_ends()
        paint.save_to_disk(output_name)

def create_cutting(output_name):
        
        #cutting_body
        cutting_body = gcode_block("")
        
        cutting_body.read_from_disk("drl_cnc.gcode")
        #cutting_body.read_from_disk("edge cuts.gcode")
        
        cutting_body.fixes()
        cutting_body.delete_ends()
        
        #cutting
        cutting = gcode_block("")
        
        cutting.read_from_disk("start.gcode")
        cutting.read_from_gcode_block(cutting_body, 500)
        cutting.read_from_disk("end.gcode")

        cutting.save_to_disk(output_name)


#main

def main():
        create_paint("PCB_paint.gcode")
        create_cutting("PCB_cutting.gcode")        


#run

main()

