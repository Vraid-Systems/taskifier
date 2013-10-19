taskifier
============

django-nonrel based project for using Google App Engine as a REST-ish taskqueue

taskifier is based on the
[django-testapp](https://github.com/django-nonrel/django-testapp)
template for creating a Google App Engine app with
[django-nonrel](https://github.com/django-nonrel).
Run `./setup.sh APP_ID VERSION_ID` to initialize a development environment;
this will download all dependencies and generate an `app.yaml`.

For use with [taskifier_js](https://github.com/jzerbe/taskifier_js).

Development Dependencies
------------
- a standard [POSIX](http://en.wikipedia.org/wiki/POSIX#POSIX-oriented_operating_systems)
shell with unzip and tar binaries installed
- [git](http://git-scm.com/downloads) and [hg](http://mercurial.selenic.com/wiki/Download) binaries in path
- [pip](http://pypi.python.org/pypi/pip) binary in path

Gotchas
------------
- When using ssh transport
GitHub requires you to have the public-key of the cloning machine on file,
even when cloning from a public repository.

Tested Dev Environments
------------
- Cygwin (bash) on Windows 7 (64 bit)
- OSX 10.8.x (64 bit)

Development Commands
------------
- load example `TaskOwner` for local testing: `python manage.py loaddata taskifier/fixtures/test_data.yaml`
- local dev server: `python manage.py runserver`
- run all unit tests: `python manage.py test taskifier`
- run specific unit test suite: `python manage.py test taskifier.QueueTestSuite`
- run specific unit test: `python manage.py test taskifier.QueueTestSuite.test_ready_and_delete_tasks`

Production Deploy
------------
1. deploy the project to GAE: `python manage.py deploy`. This could take 10
minutes. May want to wait a few more minutes after it finishes for the HRD
to stabilize.
2. Create the first owner by connecting to the remote datastore -
`python manage.py remote shell` - and executing the following with the remote
Python interpreter:

```python
from taskifier.models import TaskOwner
task_owner = TaskOwner(email='example@example.com', key='example')
task_owner.save()
```
