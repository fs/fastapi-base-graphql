import strawberry
from app.graphql.core.type import strawberry_type
from app.core.permissions import IsAuthenticated
from app.graphql.inputs.aws import AWSPresignInput
from strawberry.types import Info


def presign_file(input: AWSPresignInput, info: Info) -> :
    pass


@strawberry_type
class Mutation:
    presign_file = strawberry.field(
        resolver=presign_file,
        description='Presign file for AWS S3',
        permission_classes=IsAuthenticated,
    )