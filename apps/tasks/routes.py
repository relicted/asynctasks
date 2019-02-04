from apps.tasks import endpoints


routes = (
    dict(method='GET', path='/', handler=endpoints.Handler, name='get_task'),
    dict(method='POST', path='/', handler=endpoints.Handler, name='create_task'),

)

