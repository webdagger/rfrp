from os import name
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.exceptions import HTTPException
import endpoints
import errors
import settings
from middleware import middleware
import uvicorn




exception_handlers = {
    404: errors.not_found,
    405: errors.request_method_not_allowed,
    500: errors.server_error,
    HTTPException: errors.http_exception
}

routes = [
    Route("/create/user", endpoints.create_user_encodings, name="create", methods=["POST"]),
    Route("/create/organization", endpoints.create_organization, name="create-organization", methods=["POST"]),
    Route("/organization", endpoints.get_organization, name="get-organization", methods=["POST"]),
    Route("/500", errors.error),
    Route("/recognize", endpoints.recognize_user, name="recognize", methods=["POST"]),
    Route("/{userid}", endpoints.fetch, name="fetch", methods=["GET"]),
    Route("/delete/{userid}", endpoints.delete_user, name="delete-user", methods=["POST"]),
    Route("/train/{username}", endpoints.train_user_model, name="train-user", methods=["POST"]),
]

app = Starlette(
    debug=settings.DEBUG,
    routes=routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
    #on_startup=[database.connect],
    #on_shutdown=[database.disconnect],
)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)