from flask import Flask, jsonify, request
from flask.views import MethodView

from models import Session, Advert

import pydantic

app = Flask('app')


class HttpError(Exception):
    def __init__(self, status_code, description):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'status': 'error', 'description': error.description})
    response.status_code = error.status_code
    return response


def get_advert(advert_id: int, session: Session):
    advert = session.get(Advert, advert_id)
    if advert is None:
        raise HttpError(404, f'no advert with id: {advert_id}')
    return advert


class CreateAdvert(pydantic.BaseModel):
    title: str
    description: str
    user_name: str

    @pydantic.validator('title')
    def validate_title(cls, value: str):
        if not value.isascii():
            raise ValueError('wrong title')
        return value

    @pydantic.validator('description')
    def validate_description(cls, value: str):
        if not value.isascii():
            raise ValueError('wrong description')
        return value

    @pydantic.validator('user_name')
    def validate_user_name(cls, value: str):
        if not value.isascii():
            raise ValueError('wrong name')
        return value


def validate(input_data: dict, validation_model):
    try:
        model_item = validation_model(**input_data)
        return model_item.dict()
    except pydantic.ValidationError as er:
        raise HttpError(400, er.errors())


class AdvertsView(MethodView):
    def get(self, advert_id: int):
        with Session() as session:
            advert = get_advert(advert_id, session)
            return jsonify({'id': advert_id, 'title': advert.title, 'description': advert.description,
                            'creation_time': advert.creation_time, 'user_name': advert.user_name})

    def post(self):
        json_data = request.json
        json_data = validate(json_data, CreateAdvert)
        with Session() as session:
            advert = Advert(**json_data)
            session.add(advert)
            session.commit()
            return jsonify({'id': advert.id})

    def delete(self, advert_id: int):
        with Session() as session:
            advert = get_advert(advert_id, session)
            session.delete(advert)
            session.commit()
            return jsonify({'status': 'deleted'})


app.add_url_rule('/advert/<int:advert_id>/', view_func=AdvertsView.as_view('advert'), methods=['GET', 'DELETE'])
app.add_url_rule('/advert/', view_func=AdvertsView.as_view('create_advert'), methods=['POST'])

if __name__ == '__main__':
    app.run()
