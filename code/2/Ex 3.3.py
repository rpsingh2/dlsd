def right_justify(s):
	length = len(s)
	space = 70 - length
	spaces = ' '* space
	display = spaces + s
	print display

right_justify('allen')
right_justify('bigfatnoob')
right_justify('fss16rtr')