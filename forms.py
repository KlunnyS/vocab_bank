from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class KanjiForm(FlaskForm):
    kanji = StringField("Kanji",validators=[DataRequired()])
    level = SelectField("JLPT level", choices=[
        ("N5","N5"),
        ("N4","N4"),
        ("N3","N3"),
        ("N2","N2"),
        ("N1","N1")
    ], validators=[DataRequired()])
    change_level = BooleanField('Change level', default=False)
    meanings = StringField("Meaning/s",validators=[DataRequired()])
    kun = StringField("Kun",validators=[DataRequired()])
    on = StringField("On", validators=[DataRequired()])
    radical = StringField("Radical", validators=[DataRequired()])
    stroke_order = FileField("Obrázok receptu", validators=[FileAllowed(["jpg", "png", "jpeg", "avif"], "Povolené formáty: JPG, PNG, AVIF")])
    change_stroke_order = BooleanField('Change stroke order picture', default=False)
    submit = SubmitField('Save')
    
class KanjiSearch(FlaskForm):
    kanji = StringField("Kanji",validators=[DataRequired()])
    submit = SubmitField('🔍︎')
    
class VocabForm(FlaskForm):
    kanji_list = StringField("Kanji list of Vocab (Make sure ASCII code matches with said kanji)",validators=[DataRequired()])
    vocab = StringField("Vocab",validators=[DataRequired()])
    translation = StringField("Translation",validators=[DataRequired()])
    submit = SubmitField('Save')
    
