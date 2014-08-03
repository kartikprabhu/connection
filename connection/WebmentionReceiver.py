import requests, bs4, mf2util, mf2py, ronkyuu

def parse_mention(doc, mf, source_url, target_url):
	"""Parse the microformat received to generate a mention for target_url
	"""

	mention_dict = mf2util.interpret_comment(mf, source_url, target_url)

	# if no h-entry do last resort from html
	# insert safe default parsings

	mention_dict['comment_type'].append('mention')

	return mention_dict

class WebmentionReceiver():
	"""Object to help receive webmentions to some post.

	Args
	----
	source_url : url of the source for webmentions
	target_url : url of the target for webmentions

	Attributes
	----------
	status : status code result of fetching the source
	source_url : url of the post for which webmentions are to be sent
	source_content : content of the post being scanned for links
	mention_type : string indicating type of mention


	Public methods
	---------------
	??
	"""

	def __init__(self, source_url, target_url):

		self.source_url = source_url
		self.target_url = target_url
		self.error = None
		self.mention = None
		self.__doc__ = None

		# fetch the data from source
		data = requests.get(self.source_url)
		if data.status_code == requests.codes.ok:
			 ## check for charater encodings and use 'correct' data
			if 'charset' in data.headers.get('content-type',''):
				self.__doc__ = bs4.BeautifulSoup(data.text)
			else:
				self.__doc__ = bs4.BeautifulSoup(data.content)

		# use ronkyuu to find target_url
		self.source_result = ronkyuu.findMentions(source_url, content=self.__doc__, targetURL=self.target_url )

		if self.__doc__ is not None:
			# source was retrieved
			if self.target_url in self.source_result['refs']:
				# mention to target found
				mf = mf2py.Parser(doc=self.__doc__, url=self.source_url).to_dict()
				self.mention = parse_mention(self.__doc__, mf, self.source_url, self.target_url)
			else:
				# source does not mention target
				self.mention = None

		else:
			# source could no be retreived
			self.error = {'status':400, 'reason': 'Source URL could not be fetched.'}
