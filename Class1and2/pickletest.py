if (pickle.load( open( "save.p", "rb" ) )):
	favorite_color = pickle.load( open( "save.p", "rb" ) )
	# print "colors loaded"
else:
	favorite_color = { "lion": "yellow", "kitty": "red" }
	pickle.dump( favorite_color, open( "save.p", "wb" ) )
	# print "colors saved"