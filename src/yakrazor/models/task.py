from tortoise import models, fields, validators


class Task(models.Model):
    uuid = fields.UUIDField(pk=True)
    name = fields.TextField(
        validators=[
            validators.MinLengthValidator(1),
            validators.MaxLengthValidator(100),
        ]
    )
    done = fields.BooleanField(default=False)

    # Timestamps
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)