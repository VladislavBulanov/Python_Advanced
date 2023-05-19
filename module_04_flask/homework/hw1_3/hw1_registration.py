from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, Email, NumberRange
from hw2_validators import number_length, NumberLength

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    email = StringField(validators=[
        InputRequired("The field 'email' is required"),
        Email("The field 'email' is invalid format"),
    ])
    phone = IntegerField(validators=[
        InputRequired("The field 'phone' is required"),
        NumberRange(
            min=1000000000,
            max=9999999999,
            message="The phone number must consist of ten digits",
        ),
    ])
    name = StringField(validators=[
        InputRequired("The field 'name' is required"),
    ])
    address = StringField(validators=[
        InputRequired("The field 'address' is required"),
    ])
    index = IntegerField(validators=[
        InputRequired("The field 'index' is required"),
    ])
    comment = StringField()


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
