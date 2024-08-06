import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from booksum import service_route
from booksum.utils.io_ops import get_settings
from booksum.utils.service_models import BookSumIndex

# todo: generalize the root-path
srv_root_path = './'
settings = get_settings(srv_root_path)

sum_logger = logging.getLogger()
sum_logger.setLevel(logging.WARNING)
console_handler = logging.StreamHandler()
sum_logger.addHandler(console_handler)
# TODO: END OF GLOBAL VARS IMPROVEMENTS NEEDED


# -------------------------------------
# Prepare context
@asynccontextmanager
async def lifespan(my_app: FastAPI):
    # load AI Model
    # for now, we will opt to load during API startup to avoid too much I/O on loading/unloading big files
    # and thus setting the model as a global var

    my_app.state.settings = settings
    themes_utils = (
        BookSumIndex(
            srv_root_path,
            logger=sum_logger
        )
    )
    themes_utils.load_all_models()
    my_app.state.models = themes_utils
    yield
    my_app.state.settings = []


# -------------------------------------
# start the API
app = FastAPI(
    title=settings['booksum_service']['booksum']['api_title'],
    description=settings['booksum_service']['booksum']['api_description'],
    version=settings['booksum_service']['booksum']['api_version'],
    docs_url=settings['booksum_service']['booksum']['docs_url'],
    lifespan=lifespan
)


@app.get('/version')
async def version():
    return {"message": f"I am running version {settings['booksum_service']['booksum']['api_version']}"}


# health check route
@app.get("/health", summary="Health Check", response_description="Health status of the application")
async def health_check():
    return {"status": "UP"}


# Establish routers
app.include_router(service_route.router)


if __name__ == '__main__':
    port = settings['booksum_service']['booksum']['remote']['port']
    host = settings['booksum_service']['booksum']['remote']['host']

    uvicorn.run(
        app,
        port=int(port),
        host=host
    )
