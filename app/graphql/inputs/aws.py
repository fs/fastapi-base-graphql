from app.graphql.core.type import strawberry_pydantic_input
from app.schemas import aws_upload


@strawberry_pydantic_input(model=aws_upload.FileUpload, all_fields=True)
class AWSPresignInput:
    """File description fields."""
