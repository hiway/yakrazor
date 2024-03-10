from enum import IntEnum
from tortoise import models, fields, validators


class TaskStatus(IntEnum):
    DONE = 0
    DOING = 1
    TODO = 2
    WAITING = 3
    ON_HOLD = 4
    CANCELED = 5


class Task(models.Model):
    uuid = fields.UUIDField(pk=True)

    # Basic information
    name = fields.TextField(
        validators=[
            validators.MinLengthValidator(1),
            validators.MaxLengthValidator(100),
        ]
    )
    note = fields.TextField(
        validators=[
            validators.MinLengthValidator(0),
            validators.MaxLengthValidator(1000),
        ],
        default="",
    )
    status_value = fields.IntEnumField(TaskStatus, default=TaskStatus.TODO)
    depends_on = fields.ManyToManyField(
        "yakrazor.Task", related_name="dependents", through="task_dependencies"
    )

    # Metadata for filtering and ranking
    deadline = fields.DatetimeField(null=True)
    urgent = fields.BooleanField(default=False)
    important = fields.BooleanField(default=False)
    estimated_effort = fields.IntField(
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(10)],
        default=3,
    )
    estimated_duration = fields.TimeDeltaField(null=True)

    # Metadata to compare with estimates
    actual_effort = fields.IntField(
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(10)],
        null=True,
    )
    actual_duration = fields.TimeDeltaField(null=True)

    # Timestamps
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    started_at = fields.DatetimeField(null=True)
    completed_at = fields.DatetimeField(null=True)
    status_changed_at = fields.DatetimeField(null=True)

    @property
    def status(self) -> str:
        return self.status_value.name

    @status.setter
    def status(self, name: str) -> None:
        self.status_value = TaskStatus[name]

    class PydanticMeta:
        computed = ["status"]
