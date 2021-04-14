# Jonathan Nusantara (jan265), Eric Hall (ewh73), Eric Kahn (edk52)
# Lab 1, 09-27-2020


import subprocess

while True: # Infinite while loop
	command = raw_input("Enter command: ") # Inout as string
	
	if command == 'exit': # Command to exit
		break

    # Create command to pass to terminal	
	send_command = 'echo ' + command + 	" > video_fifo"
	subprocess.check_output(send_command, shell = True)
