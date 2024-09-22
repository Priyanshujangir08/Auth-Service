from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi import BackgroundTasks, Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from routers.user_routers import user_router
from routers.stats_routers import stats_router
from core.database import engine, Base

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service",
    docs_url="/",
    openapi_tags=[
        {"name": "User", "description":"User related operations"},
        {"name": "Stats","description": "Provides statistics for the user."}
    ]
)

# Register Routers
app.include_router(user_router, prefix="/user",tags=["User"])
app.include_router(stats_router, prefix="/stats",tags=["Stats"])


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exception: RequestValidationError):
    """
    Custom exception handler for handling validation errors raised by FastAPI.

    Parameters
    ----------
    request : Request
        The request object.
    exception : RequestValidationError
        The instance of RequestValidationError raised by FastAPI.

    Returns
    -------
    JSONResponse
        A JSON response indicating the status and details of the validation error.

        If the payload is empty:
        - Status Code: 400
        - Content: {"status_code": "SCR400", "message": "Empty Payload"}

        If there are invalid fields in the payload:
        - Status Code: 400
        - Content: {
            "status_code": "SCR400",
            "message": "Invalid <field_1>, <field_2>, ...",
            "reason": <validation_error_message>
          }

    Notes
    -----
    This exception handler is specifically designed for handling validation errors, such as empty payloads or invalid
    fields.
    It extracts information from the exception to generate a meaningful response.

    """
    field_errors = exception.errors()
    filed = field_errors[0].get("loc")
    if isinstance(filed[1], int):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                {
                    "status_code": "SCR400",
                    "message": "Empty Payload",
                }
            ),
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                {
                    "status_code": "SCR400",
                    "message": "Invalid " + ", " + " ,".join(str(s) for s in filed[1:]),
                    "reason": field_errors[0].get("msg"),
                }
            ),
        )
