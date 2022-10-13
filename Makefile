PWD := $(shell pwd)

VENV := .venv
ACTIVATE := $(VENV)/bin/activate
ACTIVATE_VENV := . $(ACTIVATE)

CONTAINER_IMAGE := neo4j:4.4.11-community
CONTAINER_NAME := neo4j-app-python
USERNAME := neo4j
PASSWORD := password
CONTAINER_AUTH := $(USERNAME)/$(PASSWORD)
CONTAINER_DIR := $(PWD)/neo4j
# See https://github.com/neo4j-graph-examples/recommendations
RECOMMENDATIONS_DUMP_FILE := recommendations-43.dump

.PHONY: run
run: venv
	$(ACTIVATE_VENV) && flask run	

# Use a local Neo4j database: Load recommendations
.PHONY: db-init
db-init: db-clean
	docker run -it \
	-v $(CONTAINER_DIR)/data:/data \
	-v $(CONTAINER_DIR)/import:/import \
	--name $(CONTAINER_NAME) \
	--rm $(CONTAINER_IMAGE) \
	neo4j-admin load --from /import/$(RECOMMENDATIONS_DUMP_FILE)

.PHONY: db-start
db-start:
	docker run \
	-p7474:7474 -p7687:7687 \
	-e NEO4J_AUTH=$(CONTAINER_AUTH) \
	-v $(CONTAINER_DIR)/data:/data \
	-v $(CONTAINER_DIR)/logs:/logs \
	-v $(CONTAINER_DIR)/import:/import \
	--name $(CONTAINER_NAME) \
	--rm -d $(CONTAINER_IMAGE)

	@printf "Waiting for database "
	@until curl -s -f -o /dev/null "http://localhost:7474"; do printf "."; sleep 1; done
	@printf " Ready\n"

.PHONY: db-stop
db-stop:
	-docker stop $(CONTAINER_NAME)

.PHONY: db-clean
db-clean: db-stop
	rm -rf $(CONTAINER_DIR)/data
	rm -rf $(CONTAINER_DIR)/logs

.PHONY: venv
venv: $(ACTIVATE)
$(ACTIVATE): requirements.txt
	python3 -m venv $(VENV)
	$(ACTIVATE_VENV) && pip install -r requirements.txt

.PHONY: versions
versions: venv
	$(ACTIVATE_VENV) && pip list

.PHONY: outdated
outdated: venv
	$(ACTIVATE_VENV) && pip list --outdated

.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -name '__pycache__' -exec rm -rf {} +
