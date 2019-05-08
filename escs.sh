##############################################################################
cd ~/projects/
git clone git@bitbucket.org:arcamens/paybills.git paybills-code
##############################################################################
# push paybills master.
cd ~/projects/django-paybills-code
# clean up all .pyc files. 
find . -name "*.pyc" -exec rm -f {} \;

git status
git add *
git commit -a
git push -u origin master
##############################################################################
# push paybills staging.
cd ~/projects/django-paybills-code
# clean up all .pyc files. 
find . -name "*.pyc" -exec rm -f {} \;

git status
git add *
git commit -a
git push -u origin staging
##############################################################################
# install, paybills, dependencies, virtualenv.
cd ~/.virtualenvs/
source paybills/bin/activate
cd ~/projects/paybills-code
pip install -r requirements.txt 
##############################################################################
# Merge staging into master.
git checkout master
git merge staging
git push -u origin master
git checkout staging
##############################################################################
# Merge master into staging.
git checkout staging
git merge master
git push -u origin staging
git checkout staging
##############################################################################
# delete last commit.

cd ~/projects/paybills-code
git reset HEAD^ --hard
git push -f
##############################################################################
# create releases.

git tag -a v1.0.0 -m 'Initial release'
git push origin : v1.0.0

git tag -a v2.0.0 -m 'Running on django 2.'
git push origin : v2.0.0





