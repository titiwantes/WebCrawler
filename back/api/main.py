import fastapi
import fastapi.middleware
import fastapi.middleware.cors

import api.routers.users_router as users
import api.routers.items_router as items
import core.exeptions.exception as exeptions

app = fastapi.FastAPI(
    title="FastAPI example",
    description="This is a simple FastAPI example",
    version="0.1.0",
    exception_handlers=exeptions.exeption_handlers,
)

app.include_router(users.router)
app.include_router(items.router)

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
