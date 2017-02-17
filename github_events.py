import sys
def _save_user(store, user):
	if user == None:
		return

	users = store['users']
	if users.get(user['id']) == None:
		users[user['id']] = user

def _save_repo(store, repo):
	if repo == None:
		return

	repos = store['repos']
	if repos.get(repo['id']) == None:
		repos[repo['id']] = repo

def _handle_commit_comment_event(event, store):
	payload = event['payload']

	# for newer api
	_save_user(store, payload.get('sender'))
	_save_user(store, payload.get('comment').get('user'))

	_save_repo(store, payload.get('repository'))
	_save_repo(store, payload.get('repo'))
	if payload.get('repository') != None:
		_save_user(store, payload.get('repository').get('owner'))

	if payload.get('repo') != None:
		_save_user(store, payload.get('repository').get('owner'))



handler = {
	'CommitCommentEvent': _handle_commit_comment_event
}
