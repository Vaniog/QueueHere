from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateQueueForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create')


class JoinQueueForm(FlaskForm):
    name_to_print = StringField('Join with name', validators=[DataRequired()])
    submit = SubmitField('Join')


class FindQueueForm(FlaskForm):
    queue_id = StringField('Queue ID', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Find')


class KillQueueForm(FlaskForm):
    queue_id = StringField('Queue ID', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Delete')


class ForgetQueueForm(FlaskForm):
    queue_id = StringField('Queue ID', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Forget')
