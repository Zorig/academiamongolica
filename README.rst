Academia Mongolica
==================

Google code дээрх хувилбараас мөчирлөн авсан агуулах болно.

* Амьд толь бичиг: http://academiamongolica.appspot.com/
* Эх хуудас: http://code.google.com/p/academiamongolica/
* Блог: http://academiamongolica.blogspot.com/
* Төслийн удирдагч: http://twitter.com/dagvadorj


Хөгжүүлэлтэнд оролцох
=====================

Төслийг суулгаж тохируулах
--------------------------

1. `source/secret_keys.py` файлыг үүсгээд дараах утгуудыг оруулна ::

    SESSION_SECRET_KEY = 'any-random-string'

    TWITTER_CONSUMER_KEY = 'your-twitter-app-key' # or 'NNlSFz6gg3S0lZ0CXFiU7w'
    TWITTER_CONSUMER_SECRET = 'your-twitter-secret-key' # or 'j0eRE2AfpcxBSt5blsAdwD0jVc5vG9O0AALYlVOKDI'

    BITLY_LOGIN = 'your-bit.ly-account'
    BITLY_API_KEY = 'your-bit.ly-api-key'

2. `./choppy-admin run` гэсэн коммандыг ажиллуулна.

Төслийг deploy хийх
-------------------

1. `./choppy-admin deploy` гэсэн коммандыг ажиллуулна.

2. `deployed` гэсэн хавтас шинээр үүснэ. Уг хавтсан доторх файлуудыг шууд deploy хийж болно.
   (`appcfg.py update deployed` гэсэн үг)
