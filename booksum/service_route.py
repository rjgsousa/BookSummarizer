import traceback

from fastapi import APIRouter, HTTPException, status, Request, Body
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from pydantic import Field, BaseModel

from booksum.utils.service_models import BookSumIndex

router = APIRouter()


class BookSumSchema(BaseModel):
    book: str = Field(..., description="book title")


def run_model(model, content) -> dict:
    print(content)
    return model.summarize_given_book_title(content)


async def run_predict(content: str, models: BookSumIndex) -> dict:
    response = await run_in_threadpool(
        run_model,
        models.model,
        content
    )

    return response


@router.post(
    "/summarize",
    status_code=status.HTTP_200_OK,
    summary="Summarize a book.",
    response_description="Returns the book summary."
  )
async def summarize(
        request: Request,
        body: BookSumSchema = Body(
            ..., example={"book": "String"}
        )
):
    models = request.app.state.models

    try:
        response = await run_predict(
            content=body.book,
            models=models
        )

        return JSONResponse(response)

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=traceback.format_exc()
        ) from ex
