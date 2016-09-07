import sys

class Employee(object):
	def __init__(self):
		self.name = ""
		self.age = ""

	def ask(self):
		self.name = raw_input("Name: ")
		self.age = raw_input("Age: ")

	def __lt__(self, other):
		return self.age < other.age
	
	def __repr__(self):
		return 'Name : %s , Age : %i ' % (self.name,self.age)

if __name__=="__main__":
	
	myList = []
	#for i in xrange(2):
	emp = Employee()
	n = raw_input("How many users do you want to enter?")
	for i in xrange(int(n)):
		emp = Employee()
		emp.ask()
		myList.append((emp.name, emp.age))

	print(sorted(myList))	