import requests, mf2util, mf2py
from . import ronkyuu, indietools

def parse_type(props, target_url):

	types = ['mention']

	# check for target link in h-entry properties
	# parse repost-of or repost for url
	if target_url in mf2py.get_url(props.get('repost-of',[])) or target_url in mf2py.get_url(props.get('repost',[])):
		types.append('repost')

	# parse in-reply-to for url
	if target_url in mf2py.get_url(props.get('in-reply-to',[])):
		types.append('reply')

	# parse like-of for url
	if target_url in mf2py.get_url(props.get('like-of',[])):
		types.append('like')

	return types

def parse_author(props, mf):

	author = {}

	poss_author = props.get('author', None)

	if poss_author:
		# possible author found
		if isinstance(poss_author, basestring):
			# if string use as name, skip rest
			author['name'] = poss_author
			return author

		elif isinstance(poss_author, list):
			# if list use the first one
			poss_author = poss_author[0]

		else:
			# not a list or string!
			raise ValueError('author was neither string nor list!')

	else:
		# no author property. find representative hcard from rel=author
		try:
			rel_author_url = mf['rels']['author'][0]
			rel_author_mf = mf2py.Parser(url=rel_author_url).to_dict()
			poss_author = indietools.rep_h_card(rel_author_mf, rel_author_url)

		except (KeyError, IndexError):
			# no rel thing found
			poss_author = None
			pass

	# construct author from h-card
	if poss_author and 'h-card' in poss_author.get('type',[]):
		author['name'] = poss_author.get('properties',{}).get('name',[None])[0]
		author['url'] = poss_author.get('properties',{}).get('url',[None])[0]
		author['photo'] = poss_author.get('properties',{}).get('photo',[None])[0]

	return author

def parse_content(props):

	return props.get('content',[{}])[0].get('value', '')


def parse_mention(html, mf, source_url, target_url):
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
		self.source_result = ronkyuu.findMentions(source_url)

		if self.source_result['status'] == requests.codes.ok:
			# source was retrieved
			if self.target_url in self.source_result['refs']:
				# mention to target found
				html = self.source_result['content']
				mf = mf2py.Parser(doc=html, url=self.source_url).to_dict()
				self.mention = parse_mention(html, mf, self.source_url, self.target_url)
			else:
				# source does not mention target
				self.mention = None
		else:
			# source could no be retreived
			self.error = {'status':400, 'reason': 'Source URL could not be retrieved.'}
