## load and export .env
ifneq (,$(wildcard ./.env))
  include .env
  export
endif

## vars
GMAIL_SENDER_MODULE_PATH := module_gmail_sender

## init project
init: check-submodule
	python3 -m pip install -r requirements.txt
	python3 -m pip install -r $(GMAIL_SENDER_MODULE_PATH)/requirements.txt
	npm install -i
.PHONY: init

# check out git submodules
check-submodule:
	ls
	@if [ ! -f "./module_gmail_sender/.git" ]; then \
		echo "Submodule Gmail Sender not found. Adding submodule..."; \
		git submodule add $(GMAIL_SENDER_MODULE_URL) $(GMAIL_SENDER_MODULE_PATH); \
	fi
	@echo "Checking out tag $(GMAIL_SENDER_MODULE_TAG) in submodule..."; \
	git submodule update --init --recursive $(GMAIL_SENDER_MODULE_PATH); \
	cd $(GMAIL_SENDER_MODULE_PATH) && git checkout $(GMAIL_SENDER_MODULE_TAG)
.PHONY: check-submodule

# fetch newsletter content
fetch: cleanup
	@echo " - Fetching from Gmail"
	python3 fetch.py
.PHONY: fetch

# parse and output newsletter content
parse:
	@echo " - Parsing"
	python3 parse.py
.PHONY: parse

# translate
translate:
	@echo " - Translating"
	python3 translate.py
.PHONY: translate

# stich
stitch:
	@echo " - Stitching"
	python3 stitch.py
.PHONY: stitch

# cleanup
cleanup:
	@echo " - Cleaning up"
	rm -rf publish/*.html publish/*.txt publish/index*
.PHONY: cleanup

# screenshot
screenshot:
	@echo " - Taking screenshot"
	node screenshot.js
.PHONY: screenshot

# sendmail
sendmail:
	@echo " - Sending email"
	python3 sendmail.py
.PHONY: sendmail

run: fetch parse translate stitch screenshot sendmail
