from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(
        min_length: int,
        max_length: int,
        message: Optional[str] = None
):
    """
    The decorator of number's length validate function.
    :param min_length: the minimal length of number
    :param max_length: the maximal length of number
    :param message: the error message if number is not valid
    """

    def validate_number_length(form: FlaskForm, field: Field):
        """
        The function for validation specified field of registration form.
        :param form: Flask registration form
        :param field: the name of checking field
        """

        nonlocal message
        phone_number = str(field.data)
        length = len(phone_number)
        if length < min_length or length > max_length:
            if message is None:
                message = (f"The phone number must be between {min_length} "
                           f"and {max_length} digits long.")
            raise ValidationError(message)

    return validate_number_length


class NumberLength:
    """The class for validation phone number by length."""

    def __init__(
            self,
            min_length: int,
            max_length: int,
            message: Optional[str] = None
    ) -> None:
        """
        The class' constructor.
        :param min_length: the minimal length of number
        :param max_length: the maximal length of number
        :param message: the error message if number is not valid
        """
        self.min_length = min_length
        self.max_length = max_length
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        """
        Called when the instance is “called” as a function.
        :param form: Flask registration form
        :param field: the name of checking field
        """
        phone_number = str(field.data)
        length = len(phone_number)
        if length < self.min_length or length > self.max_length:
            if self.message is None:
                self.message = (f"The phone number must be between {self.min_length} "
                                f"and {self.max_length} digits long.")
            raise ValidationError(self.message)
