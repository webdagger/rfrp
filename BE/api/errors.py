from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException

async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


async def not_found(request, exc):
    """
    Return an HTTP 404.
    """
    detail: str = "Page does not exist."
    return JSONResponse({"detail": detail}, status_code=404)


async def server_error(request, exc):
    """
    Return an HTTP 500.
    """
    detail: str = "Internal Server Error."
    return JSONResponse({"detail": detail}, status_code=500)


async def request_method_not_allowed(request, exc):
    """
    Return exc.status_code. Mainly to handle 405 errors
    """
    detail: str = "Method not allowed."
    return JSONResponse({"detail": detail}, status_code=405)


async def http_exception(request, exc):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
