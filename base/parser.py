class ParserClass():
	
	def __init__(self):
		self.verbs = {
				'help': 'help',
				'exit': 'exit',
				'hosts': 'hosts',
				'players': 'players',
				'rename': 'rename',
				'auth': 'auth',
				'register': 'register',
				'go': 'go',
				'climb': 'climb',
				'say': 'say',
				'look': 'look',
				'status': 'status',
				'wizard': 'wizard',
				'inventory': 'inventory',
				'drop': 'drop'
			}
	
	# verb modifier modifiers
	# TODO will need to escape 'the', etc.
	def processLine(self,line):
		if line.count(" ") >0 :
			verb = line.split(" ",1)[0]
			modifiers = line.split(" ",1)[1]
		else:
			verb = line
			modifiers = ""
		if modifiers.count(" ") >0 :
			modifiers = modifiers.split(" ")
		else:
			modifiers = [modifiers]
		verb = self.verbs.get(verb)
		if not verb:
			return 0
		return [verb,modifiers]
	
