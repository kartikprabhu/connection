import requests
from . import ronkyuu

def webmentionsender_http(request):
	"""Acts as an http request front for webmentionsender
	
	Args
	----
	request: http request to be processed

	Returns
	-------

	dictionary with 'source': source URL, 'error': description of error, 'mentions' : list of webmentions found
 
	"""
	# use POST method only
	if request.method == 'POST':
		# parse the request to get params for sender object, send suitable errors for not getting all params
		try:
			source_url = request.POST['source']
		except AttributeError:
			# no source given return an error message
			return {'error': 'No source URL given.' }
			pass

		try:
			ronkyuu.URLValidator()(source_url)
		except ValueError:
			return{'error': 'Invalid URL given.'}
			pass

		# make and use sender object

		try:
			filter_id = request.POST['filter-id']
			if filter_id:
				sender = WebmentionSender(source_url,look_in={'id': filter_id})
			else:
				raise ValueError
		except (AttributeError, ValueError):
			sender = WebmentionSender(source_url)
			pass

		#reply obtained
		answer = {'source': source_url}
		if sender.status == requests.codes.ok:
			#send mentions
			reply = sender.send_present_mentions()
			answer['mentions'] = []
			for x in reply:
				if isinstance(x[1],basestring):
					answer['mentions'].append({'link':x[0], 'status':'', 'content': x[1]})
				else:
					answer['mentions'].append({'link': x[0], 'status': getattr(x[1],"status_code", ''), 'content': getattr(x[1],"content", '')})

		else:
			answer['error'] = 'Source URL could not be retrieved.'

		return answer
	else:
		return None

class WebmentionSender():
	"""Object to help send webmentions to some post. Automatically discovers mentions by scanning content of post. Functions to send mentions to combinations of past and present mentions.

	Args
	----
	source_url : url of the source for webmentions

	Attributes
	----------
	status : status code result of fetching the source
	source_url : url of the post for which webmentions are to be sent
	source_content : content of the post being scanned for links
	present_mentions : set containing urls mentioned in the post currently
	past_mentions : set containing urls mentioned in the past
	

	Public methods
	---------------
	send_present_mentions : send webmentions to all links presently mentioned
	send_past_mentions : send webmentions to all link mentioned in the past
	send_added_mentions : send webmentions to all newly added links
	send_deleted_mentions : send webmentions to all deleted links
	send_modified_mentions : send webmentions to all the links that were modified
	send_unmodified_mentions : send webmentions to all the links that were unchanged
	"""

	def __init__(self, *args, **kwargs ):
		self.past_mentions = kwargs.pop('past_mentions',set())
		# use ronkyuu to parse and findmentions
		result = ronkyuu.findMentions(*args, **kwargs)
		self.status = result['status']
		self.source_url = result['post-url']
		self.source_content = result['content']
		self.present_mentions = result['refs']


	def _send_mentions(self, mentions_set):
		# private method to send mentions to a set of urls
		result = []
		for link in mentions_set:
			try:
				result.append([link, ronkyuu.sendWebmention(self.source_url, link)])
			except:
				result.append([link, "Error"])
				pass

		return result

	def send_present_mentions(self):
		return self._send_mentions(self.present_mentions)

	def send_past_mentions(self):
		return self._send_mentions(self.past_mentions)

	def send_added_mentions(self):
		return self._send_mentions(self.present_mentions - self.past_mentions)

	def send_deleted_mentions(self):
		return self._send_mentions(self.past_mentions - self.present_mentions)

	def send_modified_mentions(self):
		return self._send_mentions(self.present_mentions ^ self.past_mentions)

	def send_unmodified_mentions(self):
		return self._send_mentions(self.present_mentions & self.past_mentions)
