import mf2py

def mfparser_http(request):
	"""Acts as an http request front for mf2py Parser object
	
		Args
		----
		request: http request to be processed

		Returns
		-------

		dictionary with parsed microformats
	 
		"""

	if request.method == 'POST':
		try:
			content = request.POST['content']
		except AttributeError:
			return None
			pass

		p = mf2py.Parser(doc=content)

		return p.to_json(pretty_print=True)

