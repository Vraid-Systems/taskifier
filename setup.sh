#!/bin/sh

if [ $# -lt 2 ]
then
    echo "usage: $0 APP_ID VERSION_ID"
    exit 1
fi

echo APP_ID will be set to: $1
echo VERSION_ID will be set to: $2

cat app_template.yaml | sed "s/application: REPLACE_ME/application: $1/g" | sed "s/version: REPLACE_ME/version: $2/g" > app.yaml

mkdir -p build

pip install --download='./build' --no-install -e git+ssh://git@github.com/django-nonrel/djangotoolbox.git@toolbox-1.4#egg=djangotoolbox
pip install --download='./build' --no-install -e git+ssh://git@github.com/django-nonrel/djangoappengine.git@appengine-1.4#egg=djangoappengine
pip install --download='./build' --no-install -e git+ssh://git@github.com/django-nonrel/django-dbindexer.git@dbindexer-1.4#egg=django-dbindexer
pip install --download='./build' --no-install -e git+ssh://git@github.com/django-nonrel/django.git@nonrel-1.4#egg=django-nonrel
pip install --download='./build' --no-install -e hg+ssh://hg@bitbucket.org/twanschik/django-autoload#egg=django-autoload

unzip -q build/\*.zip -d build
tar xzf build/*.tar.gz --directory build

cp -r build/django-autoload/autoload ./autoload
cp -r build/django-dbindexer/dbindexer ./dbindexer
cp -r build/django-nonrel/django ./django
cp -r build/djangoappengine/djangoappengine ./djangoappengine
cp -r build/djangotoolbox/djangotoolbox ./djangotoolbox

rm -fr build
rm -fr src
