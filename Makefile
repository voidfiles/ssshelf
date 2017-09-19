CWD=$(shell pwd)

clean:
	rm -fR dist
	rm -fRr build

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
		/usr/local/bin/python -m pytest --cov=ssshel tests

shell:
	docker run --rm -it \
		-v "$(CWD)/:/code/" \
		-e "AWS_ACCESS_KEY_ID=test" \
		-e "AWS_SECRET_ACCESS_KEY=test" \
		-e "AWS_DEFAULT_REGION=us-east-1" \
		ssshelf \
		/bin/bash
