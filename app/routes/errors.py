from . import routes


@routes.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@routes.errorhandler(502)
def server_error(e):
    return e

