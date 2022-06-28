
# ==============================================================================
# CONFIGURACIONES DE COLORES
# ==============================================================================
HEADER = '\033[96m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# ==============================================================================
# CONFIGURACIONES ESTATICAS
# ==============================================================================

PROJECT = services/$(LAMBDA)/core/
RUNTIME_LOCAL_DOCKER_INVOKE = python3.8
STAGE = dev

# ==============================================================================
# DEFAULT COMMANDS
# ==============================================================================

ifdef TEST
	TEST_FILE = $(TEST)
else
	TEST_FILE = test
endif


test_remote: testing_remote_in_aws
test_local_docker: testing_in_local_with_docker
test_local: testing_local

testing_local:
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(HEADER)"Ejecutando prueba local en stage $(STAGE)"
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+cd ${PROJECT}\
		&& serverless invoke local \
		--function ${LAMBDA} \
		--path ../setup/$(STAGE)/test/$(TEST_FILE).json \
		--stage $(STAGE)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(HEADER)"Prueba local finalizada para el stage $(STAGE)"
	@+echo $(HEADER)"---------------------------------------------"$(END)

testing_in_local_with_docker:
	@+echo $(HEADER)"------------------------------------------------"$(END)
	@+echo $(HEADER)"Ejecutando prueba local con docker en stage $(STAGE)"
	@+echo $(HEADER)"------------------------------------------------"$(END)
	@+cd ${PROJECT}\
		&& serverless invoke local \
		--function ${LAMBDA} \
		--path ../setup/$(STAGE)/test/$(TEST_FILE).json \
		--param="runtime=${RUNTIME_LOCAL_DOCKER_INVOKE}" \
		--stage $(STAGE) \
		--docker
	@+echo $(HEADER)"------------------------------------------------------"$(END)
	@+echo $(HEADER)"Prueba local con docker finalizada para el stage $(STAGE)"
	@+echo $(HEADER)"------------------------------------------------------"$(END)

testing_remote_in_aws:
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(HEADER)"Ejecutando prueba remota en stage $(STAGE)"
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+cd ${PROJECT}\
		 && serverless invoke \
		 --function ${LAMBDA} \
		 --path ../setup/$(STAGE)/test/$(TEST_FILE).json \
		 --stage $(STAGE)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(HEADER)"Prueba remota finalizada para el stage $(STAGE)"
	@+echo $(HEADER)"---------------------------------------------"$(END)
