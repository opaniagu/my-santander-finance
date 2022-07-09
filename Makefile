all:
# 	poetry shell
#	make lint
	poetry version patch
	git add .
	git commit -m "patching.."	
	poetry run make bumpversion-patch
	poetry build
	git push
#   then create PR on GitHub web....and merge
# 	on local dir, change to main branch and pull
#	git checkout main
#	git pull

bumpversion-major:
	bumpversion major

bumpversion-minor:
	bumpversion minor

bumpversion-patch:
	bumpversion patch

# make git m="your message"
publish:
	git add .
	git commit -m "$m"

lint: 
	poetry run isort my_santander_finance/
	poetry run black -S -l 120 --target-version py38 my_santander_finance/
	poetry run flake8 my_santander_finance/
