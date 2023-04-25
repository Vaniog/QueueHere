from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext as _l


class CreateQueueForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired(), Length(max=100)])
    submit = SubmitField(_l('Create'))


class JoinQueueForm(FlaskForm):
    name_to_print = StringField(_l('Join with name'), validators=[DataRequired(), Length(max=30)])
    submit = SubmitField(_l('Join'))


class FindQueueForm(FlaskForm):
    queue_id = StringField(_l('Queue ID'), validators=[DataRequired(), Length(min=5)])
    submit = SubmitField(_l('Find'))


class KillQueueForm(FlaskForm):
    queue_id = StringField(_l('Queue ID'), validators=[DataRequired(), Length(min=5)])
    submit = SubmitField(_l('Delete'))


class ForgetQueueForm(FlaskForm):
    queue_id = StringField(_l('Queue ID'), validators=[DataRequired(), Length(min=5)])
    submit = SubmitField(_l('Forget'))
