LLTK-RESTful
=======

LLTK-RESTful is a [RESTful](http://en.wikipedia.org/wiki/Representational_state_transfer) API for the [Language Learning Toolkit](https://github.com/lltk/lltk) (LLTK). It is based on [Flask](http://flask.pocoo.org/) and delivers [JSON](http://en.wikipedia.org/wiki/JSON) documents by default.

Examples
--------

The API should be self-explanatory after you have had a look at the following examples:

 * **IPA**: `curl -X GET "http://server:port/lltk/ipa/de/Garten"`

 * **Pluralization**: `curl -X GET "http://server:port/lltk/plural/nl/boom"`

 * **Definite/Indefinite articles**: `curl -X GET "http://server:port/lltk/articles/de/Katze"`

 * For **conjugation of verbs**, try the following:
 ```bash
 curl -X GET "http://server:port/lltk/conjugate/de/bauen"
 curl -X GET "http://server:port/lltk/conjugate/de/past/bauen"
 curl -X GET "http://server:port/lltk/conjugate/de/perfect/bauen"
 ```

 * **Audiosamples**: `curl -X GET "http://server:port/lltk/audiosamples/it/mela?key=xxx"`

 * **Samples sentences**: `curl -X GET "http://server:port/lltk/textsamples/es/jardín"`

 * For **images**, try the following:
 ```bash
 curl -X GET "http://server:port/lltk/images/fr/souris"
 curl -X GET "http://server:port/lltk/images/fr/souris?itype=clipart&isize=large"
 curl -X GET "http://server:port/lltk/images/fr/souris?itype=lineart&isize=small"
 ```

To get some basic information about the backend you can `GET` `/lltk/info`.

Requirements
------------

Please install the following Python packages: [lltk](https://pypi.python.org/pypi/lltk), [Flask](https://pypi.python.org/pypi/Flask). You can do that by running:

`sudo pip install -r requirements/base.txt`

If you are a developer, you should install everything from `base.txt`, `extra.txt` and `development.txt`.

License
-------

**GNU Affero General Public License (AGPL)**, see `LICENSE.txt` for further details.
