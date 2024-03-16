from enum import IntEnum
from tortoise import models, fields, validators


class TaskStatus(IntEnum):
    TODO = 0
    DOING = 1
    DONE = 2


class Task(models.Model):
    uuid = fields.UUIDField(pk=True)
    name = fields.TextField(
        validators=[
            validators.MinLengthValidator(1),
            validators.MaxLengthValidator(100),
        ]
    )
    status_value = fields.IntEnumField(TaskStatus, default=TaskStatus.TODO)

    # Timestamps
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    @property
    def status(self) -> str:
        return self.status_value.name

    @status.setter
    def status(self, name: str) -> None:
        self.status_value = TaskStatus[name]

    class PydanticMeta:
        computed = ["status"]
