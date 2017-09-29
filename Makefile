CWD=$(shell pwd)

clean:
	rm -fR dist
	rm -fR build
	rm -fR ssshelf.egg-info

publish:
	python setup.py build sdist
	twine upload dist/*
	git tag v$(shell python setup.py version) || true
	git push origin master --tags

vendor:
	docker run --rm -i \
		-v "$(CWD)/:/code/" \
		-e "AWS_ACCESS_KEY_ID=test" \
		-e "AWS_SECRET_ACCESS_KEY=test" \
		-e "AWS_DEFAULT_REGION=us-east-1" \
		ssshelf \
		/scripts/vendor.sh

build_container:
	docker build . --tag=ssshelf

test:
	docker run --rm -i \
		-v "$(CWD)/:/code/" \
		-e "AWS_ACCESS_KEY_ID=test" \
		-e "AWS_SECRET_ACCESS_KEY=test" \
		-e "AWS_DEFAULT_REGION=us-east-1" \
		ssshelf \
		/usr/local/bin/python -m pytest --cov-report term-missing --cov=ssshelf tests

shell:
	docker run --rm -it \
		-v "$(CWD)/:/code/" \
		-e "AWS_ACCESS_KEY_ID=test" \
		-e "AWS_SECRET_ACCESS_KEY=test" \
		-e "AWS_DEFAULT_REGION=us-east-1" \
		ssshelf \
		/bin/bash
