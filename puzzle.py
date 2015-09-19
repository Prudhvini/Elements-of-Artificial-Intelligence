'''
 (1) Our idea was to initialize the start state with known data, make an assumption of person-package-street combination and running through a set of rules 
     to check if the assumption is valid
 (2) Our search algorithm works by assuming various combinations and checking for validation
 (3) We solved the problem manually, but were unable to formulate a good model and rules to get the correct solution through program.
  Solution solved manually - Frank-Elephant-Orange Drive
							 George-Banister-Lake Avenue
							 Heather-Amplifier-North Avenue
							 Irene-Candelabrum-Kirkwood Strret
							 Jerry-Doorknobs-Maxwell Street
'''
import sys
import itertools
import operator

class Person:
	package_o = ''
	package_r = ''
	street_s = ''
	street_l = ''
	person_g = ''
	street_g = ''
	package_s = ''
	#which package did this person receive
	def set_package_received(self, package):
		self.package_r = package

	#which package did this person order		
	def set_package_ordered(self, package):
		self.package_o = package

	def get_package_received(self):
		return self.package_r
	
	def get_package_ordered(self):
		return self.package_o

	#where did this person's package go
	def set_street_sent(self, street):
		self.street_s = street
	
	#where does this person stay	
	def set_street_lives(self, street):
		self.street_l = street

	def get_street_sent(self):
		return self.street_s
		
	def get_street_lives(self):
		return self.street_l
		
	def set_got_persons_pkg(self, person):
		self.person_g = person
		
	def get_got_persons_pkg(self):
		return self.person_g
		
	def set_got_street_pkg(self,street):
		self.street_g = street
		
	def get_got_street_pkg(self):
		return self.street_g
	
	def set_pkg_sent_to_pkg(self,package):
		self.package_s = package
		
	def get_pkg_sent_to_pkg(self):
		return self.package_s
class Street:
	package_r = ''
	package_o = ''
	package_s = ''
	person_s = ''
	person_l = ''
	street_g = ''
	person_g = ''
	street_s = ''
	#which package arrived at this street
	def set_package_received(self, package):
		self.package_r = package
	
	#which package was ordered from this street
	def set_package_ordered(self, package):
		self.package_o = package

	def get_package_received(self):
		return self.package_r

	def get_package_ordered(self):
		return self.package_o
	
	#which person got the package ordered from this street
	def set_person_sent(self, person):
		self.person_s = person
	
	#which person ordered the package from this street
	def set_person_lives(self, person):
		self.person_l = person
		
	def get_person_sent(self):
		return self.person_s
		
	def get_person_lives(self):
		return self.person_l
	
	def set_got_street_pkg(self, street):
		self.street_g = street
		
	def get_got_street_pkg(self):
		return self.street_g
		
	def set_got_persons_pkg(self,person):
		self.person_g = person
	
	def get_got_persons_pkg(self):
		return self.person_g
		
	def set_street_pkg_sent(self,street):
		self.street_s = street
	
	def get_street_pkg_sent(self):
		return self.street_s

	def set_sent_to_pkg(self,package):
		self.package_s = package
	
	def get_sent_to_pkg(self):
		return self.package_s
	
class Package:
	street_r = ''
	street_o = ''
	person_r = ''
	person_o = ''
	package_g = ''
	package_s = ''
	person_g = ''
	#which street received this package
	def set_street_received(self, street):
		self.street_r = street
	
	#which street ordered this package
	def set_street_ordered(self, street):
		self.street_o = street

	def get_street_received(self):
		return self.street_r
		
	def get_street_ordered(self):
		return self.street_o

	#which person received this package
	def set_person_received(self, person):
		self.person_r = person
	
	#which person ordered this package
	def set_person_ordered(self, person):
		self.person_o = person

	def get_person_received(self):
		return self.person_r

	def get_person_ordered(self):
		return self.person_o
		
	def set_got_package(self,package):
		self.package_g = package
		
	def get_got_package(self):
		return self.package_g
		
	def set_got_persons_pkg(self,person):
		self.person_g = person
		
	def get_got_persons_pkg(self):
		return self.person_g
		
	def set_sent_to_pkg(self,package):
		self.package_s = package
		
	def get_sent_to_pkg(self):
		return self.package_s

def validate_assumption(name, package, street, lookup):
	if package.get_street_received() != '' and name.get_pkg_sent_to_pkg() != '':
		if lookup.keys()[lookup.values().index(package.get_street_received())].get_sent_to_pkg() != \
			lookup.keys()[lookup.values().index(name.get_pkg_sent_to_pkg())].get_sent_to_pkg():
			return False			
	if street.get_sent_to_pkg() != '' and name.get_pkg_sent_to_pkg() != '':		
		if street.get_sent_to_pkg() != name.get_pkg_sent_to_pkg():
			return False
	#Rules related to name
	if name.get_package_received() != '' and name.get_package_ordered() != '':
		if name.get_package_received() == name.get_package_ordered():
			return False
	if name.get_street_sent() != '' and name.get_street_lives() != '':
		if name.get_street_sent() == name.get_street_lives():
			return False
	#Rules related to package
	if package.get_person_received() != '' and package.get_person_ordered() != '':
		if package.get_person_received() == package.get_person_ordered():
			return False
	if package.get_street_ordered() != '' and package.get_street_received() != '':
		if package.get_street_ordered() == package.get_street_received():
			return False
	#Rules related to street
	if street.get_person_sent() != '' and street.get_person_lives() != '':
		if street.get_person_sent() == street.get_person_lives():
			return False
	if street.get_package_ordered() != '' and street.get_package_received() != '':
		if street.get_package_ordered() == street.get_package_received():
			return False
	#Linked rules
	#1. name and package
	if package.get_got_persons_pkg() != '':
		if lookup[name] == package.get_got_persons_pkg():
			return False
	if name.get_package_received() != '' and street.get_package_received() != '':
		if name.get_package_received() != street.get_package_received():
			return False
	if name.get_got_persons_pkg() != '' and street.get_got_persons_pkg() != '':
		if name.get_got_persons_pkg() != street.get_got_persons_pkg():
			return False
	if package.get_street_received() != '' and street.get_street_pkg_sent() != '':
		if package.get_street_received() != street.get_street_pkg_sent():
			return False
	if name.get_package_received() != '' and package.get_got_package() != '':
		if name.get_package_received() != package.get_got_package():
			return False
	if street.get_package_received() != '' and package.get_got_package() != '':
		if street.get_package_received() != package.get_got_package():
			return False
	if name.get_street_sent() != '' and package.get_street_received() != '':
		if name.get_street_sent() != package.get_street_received():
			return False
	if package.get_sent_to_pkg() != '' and street.get_sent_to_pkg() != '':
		if package.get_sent_to_pkg() != street.get_sent_to_pkg():
			return False
	if name.get_got_street_pkg() != '' and street.get_got_street_pkg() != '':
		if name.get_got_street_pkg() != street.get_got_street_pkg():
			return False
	if name.get_got_persons_pkg() != '' and package.get_got_persons_pkg() != '':
		if name.get_got_persons_pkg() != package.get_got_persons_pkg():
			return False
	if package.get_got_persons_pkg() != '' and street.get_got_persons_pkg() != '':
		if package.get_got_persons_pkg() != street.get_got_persons_pkg():
			return False
	return True
	
def assign_links(name, package, street, lookup):
	name.set_package_ordered(lookup[package])
	name.set_street_lives(lookup[street])
	package.set_person_ordered(lookup[name])
	package.set_street_ordered(lookup[street])
	street.set_person_lives(lookup[name])
	street.set_package_ordered(lookup[package])
	
#This function makes assumptions and validates them based on rules given in problem
def solve_riddle(names, streets, packages, lookup):
	valid = False
	name_package = {}
	name_street = {}
	
	for i in range(0,5):
		name_package.setdefault(lookup[names[i]], [])
		name_street.setdefault(lookup[names[i]], [])
		for j in range(0,5):
			for k in range(0,5):
				assign_links(names[i], packages[j], streets[k], lookup)
				valid = validate_assumption(names[i], packages[j], streets[k], lookup)
				if valid == True and lookup[streets[k]] not in name_street[lookup[names[i]]]:
					name_street[lookup[names[i]]].append(lookup[streets[k]])
				if valid == True and lookup[packages[j]] not in name_package[lookup[names[i]]]:
					name_package[lookup[names[i]]].append(lookup[packages[j]])
	print "Solved!"
	print "\n", name_package
	print "\n", name_street
	
def main():
	print "Welcome!"
	names = []
	streets = []
	packages = []
	lookup_obj_str = {}
	Frank = Person()
	George = Person()
	Heather = Person()
	Irene = Person()
	Jerry = Person()
	names.append(Frank)
	names.append(George)
	names.append(Heather)
	names.append(Irene)
	names.append(Jerry)
	Kirkwood = Street()
	Lake_Avenue = Street()
	Maxwell_Street = Street()
	North_Avenue = Street()
	Orange_Drive = Street()
	streets.append(Kirkwood)
	streets.append(Lake_Avenue)
	streets.append(Maxwell_Street)
	streets.append(North_Avenue)
	streets.append(Orange_Drive)
	Amplifier = Package()
	Banister = Package()
	Candelabrum = Package()
	Doorknob = Package()
	Elephant = Package()
	packages.append(Amplifier)
	packages.append(Banister)
	packages.append(Candelabrum)
	packages.append(Doorknob)
	packages.append(Elephant)
	
	#Initialize with known data
	Candelabrum.set_got_package('Banister')
	Banister.set_got_persons_pkg('Irene')
	Irene.set_pkg_sent_to_pkg('Banister')
	Candelabrum.set_person_ordered(Banister.get_person_received())
	Banister.set_person_received(Candelabrum.get_person_ordered())
	Banister.set_sent_to_pkg('Candelabrum')
	Irene.set_package_ordered(Banister.get_got_package())
	Doorknob.set_person_received('Frank')
	Frank.set_package_received('Doorknob')
	George.set_street_sent('Kirkwood')
	Kirkwood.set_got_persons_pkg('George')
	Kirkwood.set_package_received(George.get_package_ordered())
	Heather.set_got_street_pkg('Orange_Drive')
	Orange_Drive.set_person_sent('Heather')
	Heather.set_package_received(Orange_Drive.get_package_ordered())
	Orange_Drive.set_package_ordered(Heather.get_package_received())
	Lake_Avenue.set_got_street_pkg('Kirkwood')
	Kirkwood.set_street_pkg_sent('Lake_Avenue')
	Kirkwood.set_package_ordered(Lake_Avenue.get_package_received())
	Lake_Avenue.set_package_received(Kirkwood.get_package_ordered())
	Jerry.set_got_persons_pkg('Heather')
	Jerry.set_package_received(Heather.get_package_ordered())
	Heather.set_package_ordered(Jerry.get_package_received())
	Elephant.set_street_received('North_Avenue')
	North_Avenue.set_package_received('Elephant')
	Elephant.set_got_package(Maxwell_Street.get_package_ordered())
	Elephant.set_person_ordered(Maxwell_Street.get_person_sent())
	Maxwell_Street.set_sent_to_pkg('Elephant')
	Maxwell_Street.set_person_sent(Elephant.get_person_ordered())
	Maxwell_Street.set_package_received('Amplifier')
	Amplifier.set_street_received('Maxwell_Street')
	lookup_obj_str[Frank] = 'Frank'
	lookup_obj_str[George] = 'George'
	lookup_obj_str[Heather] = 'Heather'
	lookup_obj_str[Irene] = 'Irene'
	lookup_obj_str[Jerry] = 'Jerry'
	lookup_obj_str[Amplifier] = 'Amplifier'
	lookup_obj_str[Banister] = 'Banister'
	lookup_obj_str[Candelabrum] = 'Candelabrum'
	lookup_obj_str[Doorknob] = 'Doorknob'
	lookup_obj_str[Elephant] = 'Elephant'
	lookup_obj_str[Kirkwood] = 'Kirkwood'
	lookup_obj_str[Lake_Avenue] = 'Lake_Avenue'
	lookup_obj_str[Maxwell_Street] = 'Maxwell_Street'
	lookup_obj_str[North_Avenue] = 'North_Avenue'
	lookup_obj_str[Orange_Drive] = 'Orange_Drive'

	solve_riddle(names, streets, packages, lookup_obj_str)

if __name__ == "__main__":main()