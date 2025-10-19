# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

print(dir(db))

class ArealSpec(db.Model):
    __tablename__ = 'areal_spec'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(100))



class ArealSpecificity(db.Model):
    __tablename__ = 'areal_specificity'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text_id = db.Column(db.Integer, nullable=False)
    areal_spec_id = db.Column(db.ForeignKey('areal_spec.id'))

    areal_spec = db.relationship('ArealSpec', primaryjoin='ArealSpecificity.areal_spec_id == ArealSpec.id', backref='areal_specificities')



class AssignAuthor(db.Model):
    __tablename__ = 'assign_authors'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    author_id = db.Column(db.ForeignKey('authors.id'), nullable=False)
    text_id = db.Column(db.ForeignKey('texts.id'))

    author = db.relationship('Author', primaryjoin='AssignAuthor.author_id == Author.id', backref='assign_authors')
    text = db.relationship('Text', primaryjoin='AssignAuthor.text_id == Text.id', backref='assign_authors')



class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    author_gender_id = db.Column(db.ForeignKey('gender.id'))
    name = db.Column(db.String(250))

    author_gender = db.relationship('Gender', primaryjoin='Author.author_gender_id == Gender.id', backref='authors')



class Characteristic(db.Model):
    __tablename__ = 'characteristics'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    approval = db.Column(db.Float(53))
    importance = db.Column(db.Float(53))
    aggressiveness = db.Column(db.Float(53))
    closeness = db.Column(db.Float(53))
    text_id = db.Column(db.ForeignKey('texts.id'))

    text = db.relationship('Text', primaryjoin='Characteristic.text_id == Text.id', backref='characteristics')



class ChronologSpec(db.Model):
    __tablename__ = 'chronolog_spec'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(100))



class ChronologSpecificity(db.Model):
    __tablename__ = 'chronolog_specificity'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text_id = db.Column(db.Integer, nullable=False)
    chronolog_spec_id = db.Column(db.ForeignKey('chronolog_spec.id'))

    chronolog_spec = db.relationship('ChronologSpec', primaryjoin='ChronologSpecificity.chronolog_spec_id == ChronologSpec.id', backref='chronolog_specificities')



class Date(db.Model):
    __tablename__ = 'dates'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(50))



class Dictionary(db.Model):
    __tablename__ = 'dictionary'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    word = db.Column(db.String(100), index=True)
    accent = db.Column(db.String(100))
    blob_data = db.Column(db.LargeBinary)



class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(11))



class GenderSpec(db.Model):
    __tablename__ = 'gender_spec'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(100))



class GenderSpecificity(db.Model):
    __tablename__ = 'gender_specificity'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text_id = db.Column(db.Integer, nullable=False)
    gender_spec_id = db.Column(db.ForeignKey('gender_spec.id'))

    gender_spec = db.relationship('GenderSpec', primaryjoin='GenderSpecificity.gender_spec_id == GenderSpec.id', backref='gender_specificities')



class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text_id = db.Column(db.ForeignKey('texts.id'))
    genre_type_id = db.Column(db.ForeignKey('genres_types.id'))

    genre_type = db.relationship('GenresType', primaryjoin='Genre.genre_type_id == GenresType.id', backref='genres')
    text = db.relationship('Text', primaryjoin='Genre.text_id == Text.id', backref='genres')



class GenresType(db.Model):
    __tablename__ = 'genres_types'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(50))



class ProffessionalSpec(db.Model):
    __tablename__ = 'proffessional_spec'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(100))



class ProffessionalSpecificity(db.Model):
    __tablename__ = 'proffessional_specificity'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text_id = db.Column(db.Integer, nullable=False)
    proffessional_spec_id = db.Column(db.ForeignKey('proffessional_spec.id'))

    proffessional_spec = db.relationship('ProffessionalSpec', primaryjoin='ProffessionalSpecificity.proffessional_spec_id == ProffessionalSpec.id', backref='proffessional_specificities')



class SocialAgeSpec(db.Model):
    __tablename__ = 'social_age_spec'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(100))



class SocialAgeSpecificity(db.Model):
    __tablename__ = 'social_age_specificity'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text_id = db.Column(db.Integer, nullable=False)
    social_age_spec_id = db.Column(db.ForeignKey('social_age_spec.id'))

    social_age_spec = db.relationship('SocialAgeSpec', primaryjoin='SocialAgeSpecificity.social_age_spec_id == SocialAgeSpec.id', backref='social_age_specificities')



class SocialCasteSpec(db.Model):
    __tablename__ = 'social_caste_spec'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(100))



class SocialCasteSpecificity(db.Model):
    __tablename__ = 'social_caste_specificity'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text_id = db.Column(db.Integer, nullable=False)
    social_caste_spec_id = db.Column(db.ForeignKey('social_caste_spec.id'))

    social_caste_spec = db.relationship('SocialCasteSpec', primaryjoin='SocialCasteSpecificity.social_caste_spec_id == SocialCasteSpec.id', backref='social_caste_specificities')



class SourceType(db.Model):
    __tablename__ = 'source_types'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(100))



class Source(db.Model):
    __tablename__ = 'sources'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    source_type_id = db.Column(db.ForeignKey('source_types.id'))
    text_id = db.Column(db.ForeignKey('texts.id'))

    source_type = db.relationship('SourceType', primaryjoin='Source.source_type_id == SourceType.id', backref='sources')
    text = db.relationship('Text', primaryjoin='Source.text_id == Text.id', backref='sources')



class SpeechForm(db.Model):
    __tablename__ = 'speech_form'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text_id = db.Column(db.ForeignKey('texts.id'))
    speech_form_type_id = db.Column(db.ForeignKey('speech_form_types.id'))

    speech_form_type = db.relationship('SpeechFormType', primaryjoin='SpeechForm.speech_form_type_id == SpeechFormType.id', backref='speech_forms')
    text = db.relationship('Text', primaryjoin='SpeechForm.text_id == Text.id', backref='speech_forms')



class SpeechFormType(db.Model):
    __tablename__ = 'speech_form_types'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(30))



class Style(db.Model):
    __tablename__ = 'styles'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text_id = db.Column(db.ForeignKey('texts.id'))
    styles_types_id = db.Column(db.ForeignKey('styles_types.id'))

    styles_types = db.relationship('StylesType', primaryjoin='Style.styles_types_id == StylesType.id', backref='styles')
    text = db.relationship('Text', primaryjoin='Style.text_id == Text.id', backref='styles')



class StylesType(db.Model):
    __tablename__ = 'styles_types'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(100))



class Text(db.Model):
    __tablename__ = 'texts'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_id = db.Column(db.ForeignKey('users2.vk_id'))
    text_name = db.Column(db.String(1000))
    text = db.Column(db.Text, nullable=False)
    text_blob = db.Column(db.LargeBinary)
    source_link = db.Column(db.String(1000))
    date_id = db.Column(db.ForeignKey('dates.id'))
    is_checked = db.Column(db.Boolean)

    date = db.relationship('Date', primaryjoin='Text.date_id == Date.id', backref='texts')
    user = db.relationship('User', primaryjoin='Text.user_id == User.vk_id', backref='texts')


''' OLD 
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    email = db.Column(db.String(150))
    age = db.Column(db.Integer)
    status = db.Column(db.String(50))
    access_level = db.Column(db.Integer)
'''

class User(db.Model):
    __tablename__ = 'users2'

    vk_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    last_name = db.Column(db.String(70))
    first_name = db.Column(db.String(70))
    url = db.Column(db.String(1000))
    access_level = db.Column(db.Integer)

class XenologSpec(db.Model):
    __tablename__ = 'xenolog_spec'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(100))



class XenologSpecificity(db.Model):
    __tablename__ = 'xenolog_specificity'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text_id = db.Column(db.Integer, nullable=False)
    xenolog_spec_id = db.Column(db.ForeignKey('xenolog_spec.id'))

    xenolog_spec = db.relationship('XenologSpec', primaryjoin='XenologSpecificity.xenolog_spec_id == XenologSpec.id', backref='xenolog_specificities')
