call git init
call git config --global user.name "Cristian Alecu"
call git config --global user.email cristian.alecu@gmail.com

call git add --all .
call git commit -m "My Django app, first commit"

call git remote add origin https://github.com/cristianalecu/Django.git

call git push -u origin master
