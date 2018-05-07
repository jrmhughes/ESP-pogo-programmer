#+ check if there is more efficient alternative to 'self.data = (self.data).replace'
#+?leave original gcode as a comment
class gcode_block:
        def __init__(self, data):
                self.data = data
        def fixes(self, feedrate, travel_feedrate, drill_time = 0):
                self.data = (self.data).replace("G01 Z-0.0020", "M03 S255 ;fixes\n\
G01 F{} ;fixes".format(feedrate))
                self.data = (self.data).replace("G00 Z0.1000", "M03 S1 ;fixes\n\
G00 F{} ;fixes".format(travel_feedrate))
                self.data = (self.data).replace("G01 Z0", "G04 P{} ;fixes".format(drill_time))
        def delete_ends(self):
                self.data = (self.data).replace("G00 X0Y0\nM05", ";G00 X0Y0; delete_ends\r\n;M05; delete_ends")
        def read_from_disk(self, read_file_name, n_iterations = 1):
                with open(read_file_name, "r") as read_file:
                        read_data = read_file.read()  
                        self.data += (read_data + "\n") * n_iterations
        def read_from_gcode_block(self, read_block, n_iterations = 1):
                self.data += (read_block.data + "\n") * n_iterations
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

        paint.fixes("15", "1800", "300")
        paint.delete_ends()
        paint.save_to_disk(output_name)

def create_cutting(output_name):
        
        #cutting_body
        cutting_body = gcode_block("")
        
        cutting_body.read_from_disk("drl_cnc.gcode")
        #cutting_body.read_from_disk("edge cuts.gcode")
        
        cutting_body.fixes("60", "1800", "10000")
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

