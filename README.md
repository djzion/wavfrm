wavfrm
======

Visual Waveform API

Install
======

sudo aptitude install libsndfile-dev
or
brew install libsndfile

cp settings.py.default settings.py #make your local changes

virtualenv env
source env/bin/activate
pip install -r requirements.txt

You must have lame in /usr/bin/lame.  Use brew or get a binary
brew install lame
sudo ln -s /usr/local/bin/lame /usr/bin/lame
