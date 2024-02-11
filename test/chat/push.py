import pusher


# app key: eb1d5f283081a78b932c

pusher_client = pusher.Pusher(app_id=u'4', key=u'eb1d5f283081a78b932c', secret=u'secret', ssl=True, cluster=u'cluster')

print(pusher_client)