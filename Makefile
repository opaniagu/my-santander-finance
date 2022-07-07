all:
	poetry version patch
	git add .
	git commit -m "patching.."	
	poetry run make bumpversion-patch
	poetry build

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
