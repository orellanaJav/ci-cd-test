# ==============================================================================
# CONFIGURACIONES DE COLORES
# ==============================================================================
OKBLUE='\033[94m'
RED='\033[0;31m'
END='\033[0m'
WARNING='\033[93m'
FAIL='\033[91m'
OKGREEN = '\033[92m'
HEADER = '\033[96m'

# ==============================================================================
# CONFIGURACIONES ESTATICAS
# ==============================================================================
VIRTUALENV=".env"
RUNTIME="python3.9"
PIP_PATH="${LAMBDA_PATH}/${VIRTUALENV}/bin/pip"
SITE_PACKAGES_PATH="${LAMBDA_PATH}/${VIRTUALENV}/lib/${RUNTIME}/site-packages"
PYTHON_LAYER_PATH="${SITE_PACKAGES_PATH}/python"
BIN_ACTIVATE="${LAMBDA_PATH}/${VIRTUALENV}/bin/activate"
LAYERS_CACHE_PATH="${LAMBDA_PATH}/${VIRTUALENV}/lib/${RUNTIME}/site-packages/.cache"
LAMBDA_PATH=services/${LAMBDA}
CREATE_VIRTUALENV="${RUNTIME} -m venv ${LAMBDA_PATH}/${VIRTUALENV}"
PROJECT = services/${LAMBDA}
STAGE="dev"
DEFAULT_TEST_FILE="test"
SHELL=/bin/bash

# ==============================================================================
# DEFAULT COMMANDS
# ==============================================================================

invoke_local: create_venv install_requirements create_layers_cache install_layers add_local_layers test_invoke_local
invoke_remote: test_invoke_remote
remove_stack: remove
remove_lambda: remove update_serverless_file

create_venv:
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"CREANDO ENTORNO VIRTUAL"${END};	
	@if test ! -d "${VIRTUALENV}"; then \
		if eval ${CREATE_VIRTUALENV}; then \
			echo ""; \
			echo -e ${OKGREEN}"[OK] ENTORNO VIRTUAL CREADO CORRECTAMENTE"${END}; \
		else \
			echo -e ${FAIL}"-----------------------------------------"${END}; \
			echo -e ${FAIL}"[ERROR] ERROR AL CREAR ENTORNO VIRTUAL"${END}; \
			echo -e ${FAIL}"-----------------------------------------"${END}; \
			exit 1
		fi
	fi

install_requirements:
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"INSTALANDO LIBRERIAS EN ENTORNO VIRTUAL"${END};
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@if ! ${PIP_PATH} --no-cache-dir install -Ur ${LAMBDA_PATH}/core/requirements.txt; then \
		echo -e ${FAIL}"-----------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] ERROR AL INSTALAR LIBRERIAS"${END}; \
		echo -e ${FAIL}"-----------------------------------------"${END}; \
		exit 1
	else \
		echo -e ${HEADER}"-----------------------------------------"${END}; \
		echo -e ${OKGREEN}"[OK] LIBRERIAS INSTALADAS CORRECTAMENTE"${END}; \
	fi

create_layers_cache: $(eval .ONESHELL:)
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"CREANDO CACHÉ PARA LAYERS"${END};	
	@if ! mkdir -p ${LAYERS_CACHE_PATH}; then \
		echo -e ${FAIL}"-----------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] ERROR AL CREAR CACHÉ"${END}; \
		echo -e ${FAIL}"-----------------------------------------"${END}; \
		exit 1
	fi
	@if ! touch ${LAYERS_CACHE_PATH}/layers; then \
		echo -e ${FAIL}"-----------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] ERROR AL CREAR CACHÉ"${END}; \
		echo -e ${FAIL}"-----------------------------------------"${END}; \
		exit 1
	else \
		echo ""; \
		echo -e ${OKGREEN}"[OK] CACHÉ CREADO CORRECTAMENTE"${END}; \
		echo -e ${HEADER}"-----------------------------------------"${END}; \
	fi

install_layers:	
	@echo -e ${HEADER}"INSTALANDO LAYERS"${END};
	@layers="$$(jq -c '(.LAYERS[])' ${LAMBDA_PATH}/setup/dev/config.json)"
	@layers="$$(sed -e 's/^"//' -e 's/"$$//' <<<"$$layers")"
	@echo "$$layer"
	@if [[ "$$layers" ]]; then \
		while read -r layer; do \
			if $$(! grep -Fxq "$$layer" ${LAYERS_CACHE_PATH}/layers); then \
				layer_url=$$(aws lambda \
					get-layer-version-by-arn \
					--arn $$layer --query \
					Content.Location --output text \
					); \
				echo "$$layer" >> ${LAYERS_CACHE_PATH}/layers; \
				curl $$layer_url -o "${SITE_PACKAGES_PATH}/$$layer.zip"; \
				unzip "${SITE_PACKAGES_PATH}/$$layer.zip" -d "${SITE_PACKAGES_PATH}/"; \
				cp -a "${PYTHON_LAYER_PATH}/." ${SITE_PACKAGES_PATH}; \
				rm -rf "${SITE_PACKAGES_PATH}/$$layer.zip"; \
				rm -rf ${PYTHON_LAYER_PATH}; \
				. ${BIN_ACTIVATE}; \
			fi; \
		done <<< "$$layers"; \
	fi;
	@echo -e ${OKGREEN}"[OK] LAYERS INSTALADOS CORRECTAMENTE "${END};

# test_invoke_local:	
# 	@echo -e ${HEADER}"-----------------------------------------"${END};
# 	@echo -e ${HEADER}"EJECUTANDO PRUEBA LOCAL"${END};
# 	@echo -e ${HEADER}"-----------------------------------------"${END};
# 	@if [[ "${TEST}" ]]; then \
# 		TEST_FILE="${TEST}"; \
# 	else \
# 		TEST_FILE="${DEFAULT_TEST_FILE}"; \
# 	fi	
# 	@. ${BIN_ACTIVATE}
# 	@+cd ${PROJECT}\
# 		&& serverless invoke local \
# 		--function ${LAMBDA} \
# 		--path ../setup/${STAGE}/test/$$TEST_FILE.json \
# 		--stage ${STAGE}
# 	@echo -e ${HEADER}"-----------------------------------------"${END};
# 	@echo -e ${HEADER}"PRUEBA LOCAL FINALIZADA PARA EL STAGE ${STAGE}"${END};
# 	@echo -e ${HEADER}"-----------------------------------------"${END};

test_invoke_remote:
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"EJECUTANDO PRUEBA REMOTA EN STAGE ${STAGE}"${END};	
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@if [[ "${TEST}" ]]; then \
		TEST_FILE="${TEST}"; \
	else \
		TEST_FILE="${DEFAULT_TEST_FILE}"; \
	fi
	@serverless invoke \
		--function ${LAMBDA} \
		--path ${PROJECT}/setup/${STAGE}/test/$$TEST_FILE.json \
		--stage ${STAGE}
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"PRUEBA REMOTA FINALIZADA PARA EL STAGE ${STAGE}"${END};	
	@echo -e ${HEADER}"-----------------------------------------"${END};

remove:
	@if [[ "${LAMBDA}" ]]; then \
		PATH_TO_REMOVE="services/${LAMBDA}"; \
	else \
		PATH_TO_REMOVE="$$(pwd)"; \
	fi
	@echo -e ${WARNING}
	@read -p "¿Estás seguro? (s/n) " yn
	@echo -e ${END}
	@case $$yn in \
        [YysS]* ) \
			rm -rf $$PATH_TO_REMOVE
		;; \
        [Nn]* ) \
			exit 0 \
		;;  \
        * ) \
			echo -e ${WARNING}"------------------------------------"${END}; \
			echo -e ${RED}[ERROR]${END} "Por favor responda (s) o (n)"; \
			echo -e ${WARNING}"------------------------------------"${END}; \
			echo ; \
			exit \
		;;  \
    esac


add_local_layers:
	@echo -e ${HEADER}	
	@echo "¿Deseas agregar layers locales?"	
	@PS3='Ingresa tu opción: '
	@options=("Si" "No")
	@select opt in "$${options[@]}"
	@do \
		case $$opt in \
			"Si") \
				read -p "Ingresa el nombre del layer: " layer_name
				ACTUAL_PATH="$$(pwd)"
				echo $$ACTUAL_PATH
				cd ../../legolayers
				LAYERS_PATH="$$(pwd)"
				if test -d "$$layer_name"; then \
					cd $$ACTUAL_PATH
					${PIP_PATH} --no-cache-dir install -Ur $$LAYERS_PATH/$$layer_name/setup/requirements
					cp -r $$LAYERS_PATH/$$layer_name/$$layer_name/$$layer_name $$ACTUAL_PATH/${SITE_PACKAGES_PATH}
					echo "hola"; \
				else \
					echo -e ${FAIL}"-----------------------------------------"${END}; \
					echo -e ${FAIL}"[ERROR] ERROR AL CREAR ENTORNO VIRTUAL"${END}; \
					echo -e ${FAIL}"-----------------------------------------"${END}; \
					exit 1
				fi
				;; \
			"No") \
				break
				;; \
			"Option 3") \
				echo "you chose choice $$REPLY which is $$opt"
				;; \
			"Quit") \
				break
				;; \
			*) echo "$$REPLY opción inválida";;
		esac; \
	done
	@echo -e ${END}

update_serverless_file:	
	@if test ! -d "services/${LAMBDA}"; then \
		${RUNTIME} -c 'import yaml;\
					f=open("serverless.yml");\
					y=yaml.load(f, Loader=yaml.FullLoader);\
					actual_functions=y["functions"];\
					actual_cmd_removed_arctifacts=y["custom"]["scriptHooks"]["before:package:createDeploymentArtifacts"];\
					lambda_to_delete="file(services/${LAMBDA}/event.yml)";\
					cmd_to_delete="services/${LAMBDA}/core";\
					cleaned_cmd_removed_arctifacts=[ x for x in actual_cmd_removed_arctifacts if cmd_to_delete not in x ];\
					cleaned_functions=[ x for x in actual_functions if lambda_to_delete not in x ];\
					y["custom"]["scriptHooks"]["before:package:createDeploymentArtifacts"]=cleaned_cmd_removed_arctifacts;\
					y["functions"]=cleaned_functions;\
					fu=open("serverless.yml", "w");\
					yaml.dump(y, fu);'
		echo -e ${HEADER}"-----------------------------------------"${END};
		echo -e ${OKGREEN}"[OK] LAMBDA ELIMINADO CORRECTAMENTE "${END};
		echo -e ${HEADER}"-----------------------------------------"${END};
	fi

test_invoke_local:
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"EJECUTANDO PRUEBA LOCAL"${END};
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@cd ${PROJECT}
	@${RUNTIME} -c 'import yaml;\
				f=open("event.yml");\
				y=yaml.load(f, Loader=yaml.FullLoader);\
				y["${LAMBDA}"]["handler"]="services/${LAMBDA}/core/${LAMBDA}.lambda_handler";\
				fu=open("event.yml", "w");\
				yaml.dump(y, fu)'
	@cd ..
	@cd ..
	@if [[ "${TEST}" ]]; then \
		TEST_FILE="${TEST}"; \
	else \
		TEST_FILE="${DEFAULT_TEST_FILE}"; \
	fi
	@. ${BIN_ACTIVATE}
	@pip install pyyaml
	@pip list
	@serverless invoke local \
		--function ${LAMBDA} \
		--path ${PROJECT}/setup/${STAGE}/test/$$TEST_FILE.json \
		--stage ${STAGE}
	@cd ${PROJECT}
	@${RUNTIME} -c 'import yaml;\
				f=open("event.yml");\
				y=yaml.load(f, Loader=yaml.FullLoader);\
				y["${LAMBDA}"]["handler"]="${LAMBDA}.lambda_handler";\
				fu=open("event.yml", "w");\
				yaml.dump(y, fu)'

	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"PRUEBA LOCAL FINALIZADA PARA EL STAGE ${STAGE}"${END};
	@echo -e ${HEADER}"-----------------------------------------"${END};
