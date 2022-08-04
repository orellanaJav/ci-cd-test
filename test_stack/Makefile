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
BACK_TWO_LEVELS=../../
DEFAULT_TEST_FILE="test"
LEGOLAYERS_FOLDER=legolayers
RUNTIME="python3.9"
SHELL=/bin/bash
STAGE="dev"
PROFILE="sso"
LAMBDA_PATH=services/${LAMBDA}
VIRTUALENV="${LAMBDA_PATH}/.env"
PIP_PATH="${VIRTUALENV}/bin/pip"
SITE_PACKAGES_PATH="${VIRTUALENV}/lib/${RUNTIME}/site-packages"
PYTHON_LAYER_PATH="${SITE_PACKAGES_PATH}/python"
BIN_ACTIVATE="${VIRTUALENV}/bin/activate"
LAYERS_CACHE_PATH="${VIRTUALENV}/lib/${RUNTIME}/site-packages/.cache"
CREATE_VIRTUALENV="${RUNTIME} -m venv ${VIRTUALENV}"
PROJECT = services/${LAMBDA}

# ==============================================================================
# DEFAULT COMMANDS
# ==============================================================================

prepare: create_venv install_requirements install_local_layers
install_remote_layers: create_layers_cache install_aws_layers
remove_lambda: remove update_serverless_file

# =============================================================================
# PREPARACIÓN DEL ENTORNO VIRTUAL DE UN LAMBDA
# - CREA EL ENTORNO VIRTUAL CON EL RUNTIME ESPECIFICADO
# - INSTALA LOS REQUIREMENTS DEL LAMBDA EN EL CASO DE TENER
# - INSTALA LAYERS LOCALES (OPCIONAL)
# =============================================================================

create_venv:
	@if [[ ! "${LAMBDA}" ]]; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] DEBES ESPECIFICAR UN LAMBDA"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${LAMBDA_PATH}"; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] LAMBDA INDICADO NO EXISTE EN EL STACK"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
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
		echo ""; \
		echo -e ${HEADER}"ACTUALIZANDO PIP"${END}; \
		if ${PIP_PATH} -q install --upgrade pip; then \
			echo ""; \
			echo -e ${OKGREEN}"[OK] PIP ACTUALIZADO CORRECTAMENTE"${END}; \
		else \
			echo -e ${FAIL}"[ERROR] ERROR AL ACTUALIZAR PIP"${END}; \
		fi
	fi

install_requirements:
	@if [[ ! "${LAMBDA}" ]]; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] DEBES ESPECIFICAR UN LAMBDA"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${LAMBDA_PATH}"; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] LAMBDA INDICADO NO EXISTE EN EL STACK"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${VIRTUALENV}"; then \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] NO EXISTE ENTORNO VIRTUAL CREADO PARA EL LAMBDA INDICADO"${END}; \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		exit 1
	fi
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"INSTALANDO LIBRERIAS EN ENTORNO VIRTUAL"${END};
	@if ! (${PIP_PATH} --no-cache-dir install -Ur ${LAMBDA_PATH}/core/requirements.txt; ${PIP_PATH} -q install wheel); then \
		echo -e ${FAIL}"-----------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] ERROR AL INSTALAR LIBRERIAS"${END}; \
		echo -e ${FAIL}"-----------------------------------------"${END}; \
		exit 1
	else \
		echo ""; \
		echo -e ${OKGREEN}"[OK] LIBRERIAS INSTALADAS CORRECTAMENTE"${END}; \
	fi

install_local_layers:
	@if [[ ! "${LAMBDA}" ]]; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] DEBES ESPECIFICAR UN LAMBDA"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${LAMBDA_PATH}"; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] LAMBDA INDICADO NO EXISTE EN EL STACK"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${VIRTUALENV}"; then \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] NO EXISTE ENTORNO VIRTUAL CREADO PARA EL LAMBDA INDICADO"${END}; \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		exit 1
	fi
	@echo -e ${HEADER}
	@echo "¿Deseas instalar un layer local?"
	@PS3='Ingresa tu opción: '
	@options=("SI" "NO")
	@select opt in "$${options[@]}"
	@do \
		case $$REPLY in \
			"1") \
				read -p "Ingresa el nombre del layer: " layer_name
				ACTUAL_PATH="$$(pwd)"
				cd ${BACK_TWO_LEVELS}
				cd ${LEGOLAYERS_FOLDER}
				LAYERS_PATH="$$(pwd)"
				if test -d "$$layer_name"; then \
					echo -e ${HEADER}"------------------------------------"${END};
					echo -e ${HEADER}"INSTALANDO LAYER $$layer_name LOCAL"${END};
					echo -e ${HEADER}"------------------------------------"${END};
					cd $$ACTUAL_PATH
					${PIP_PATH} -q --no-cache-dir install -Ur $$LAYERS_PATH/$$layer_name/setup/requirements
					if eval rsync -av --progress $$LAYERS_PATH/$$layer_name/$$layer_name/ ${SITE_PACKAGES_PATH}; then \
						echo -e ${OKGREEN}"[OK] LAYER INSTALADO CORRECTAMENTE "${END};
						echo -e ${HEADER}"------------------------------------${END}";
						echo -e ${HEADER};
					else \
						echo -e ${FAIL}"-----------------------------------------"${END}; \
						echo -e ${FAIL}"[ERROR] ERROR AL INSTALAR LAYER LOCAL"${END}; \
						echo -e ${FAIL}"-----------------------------------------"${END}; \
						exit 1
					fi
					PS3='¿Deseas instalar otro layer? (1.-SI  -  2.- NO): '
					cd $$ACTUAL_PATH
				else \
					echo -e ${HEADER}"---------------------------------------------"${END}; \
					echo -e ${WARNING}"[INFO] NO SE ENCUENTRA EL LAYER ESPECIFICADO"${END}; \
					echo -e ${HEADER}"---------------------------------------------"${END}; \
					echo -e ${HEADER};
					PS3='¿Deseas instalar otro layer? (1.-SI  -  2.- NO): '
					cd $$ACTUAL_PATH
				fi
				;; \
			"2") \
				echo -e "\n"; \
				echo -e ${HEADER}"----------------------------------------------"${END}; \
				echo -e ${OKGREEN}"[INFO] YA PUEDES REALIZAR INVOCACIONES LOCALES"${END}; \
				echo -e ${HEADER}"----------------------------------------------"${END}; \
				echo -e ${HEADER};
				break
				;; \
			*) echo "$$REPLY opción inválida";;
		esac; \
	done
	@echo -e ${END}


# =============================================================================
# INSTALACIÓN DE LAYERS REMOTOS
# - CREA UN CACHÉ CON LOS LAYERS QUE YA SE HAYAN INSTALADO
# - INSTALA LOS LAYERS DEFINIDOS EN EL SETUP DEL STAGE POR CADA FUNCIÓN LAMBDA
# - LOS LAYERS QUEDAN INTALADOS EN EL ENTORNO VIRTUAL CREADO PREVIAMENTE
# =============================================================================

create_layers_cache: $(eval .ONESHELL:)
	@if [[ ! "${LAMBDA}" ]]; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] DEBES ESPECIFICAR UN LAMBDA"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${LAMBDA_PATH}"; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] LAMBDA INDICADO NO EXISTE EN EL STACK"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${VIRTUALENV}"; then \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] NO EXISTE ENTORNO VIRTUAL CREADO PARA EL LAMBDA INDICADO"${END}; \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		exit 1
	fi
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

install_aws_layers:
	@if test ! -f "${LAYERS_CACHE_PATH}/layers"; then \
		echo -e ${FAIL}"---------------------------------------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] NO SE PUEDEN INSTALAR LAYERS SI EL ARCHIVO DE CACHÉ NO ESTÁ CRREADO"${END}; \
		echo -e ${FAIL}"---------------------------------------------------------------------------"${END}; \
		exit 1
	fi
	@if [[ ! "${LAMBDA}" ]]; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] DEBES ESPECIFICAR UN LAMBDA"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${LAMBDA_PATH}"; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] LAMBDA INDICADO NO EXISTE EN EL STACK"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${VIRTUALENV}"; then \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] NO EXISTE ENTORNO VIRTUAL CREADO PARA EL LAMBDA INDICADO"${END}; \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		exit 1
	fi
	@echo -e ${HEADER}"INSTALANDO LAYERS"${END};
	@layers="$$(jq -c '(.LAYERS[])' ${LAMBDA_PATH}/setup/${STAGE}/config.json)"
	@layers="$$(sed -e 's/^"//' -e 's/"$$//' <<<"$$layers")"
	@if [[ "$$layers" ]]; then \
		while read -r layer; do \
			if $$(! grep -Fxq "$$layer" ${LAYERS_CACHE_PATH}/layers); then \
				layer_url=$$(aws lambda \
					get-layer-version-by-arn \
					--arn $$layer --query \
					Content.Location --output text \
					); \
				if [[ ! "$$layer_url" ]]; then \
					echo -e ${FAIL}"---------------------------------------------------"${END}; \
					echo -e ${FAIL}"[ERROR] NO SE HAN PODIDO OBTENER LOS LAYERS REMOTOS"${END}; \
					echo -e ${FAIL}"---------------------------------------------------"${END}; \
					exit 1
				fi
				if ! echo "$$layer" >> ${LAYERS_CACHE_PATH}/layers; then \
					echo -e ${FAIL}"---------------------------------------------------------"${END}; \
					echo -e ${FAIL}"[ERROR] HA OCURRIDO UN ERROR AL CREAR EL ARCHIVO DE CACHÉ"${END}; \
					echo -e ${FAIL}"---------------------------------------------------------"${END}; \
					exit 1
				fi
				if ! curl $$layer_url -o "${SITE_PACKAGES_PATH}/$$layer.zip"; then \
					echo -e ${FAIL}"--------------------------------------------------------------------------"${END}; \
					echo -e ${FAIL}"[ERROR] HA OCURRIDO UN ERROR AL EXTRAER LOS LAYERS A LA CARPETA DE DESTINO"${END}; \
					echo -e ${FAIL}"--------------------------------------------------------------------------"${END}; \
					rm -rf ${LAYERS_CACHE_PATH}/layers
					exit 1
				fi
				if ! unzip -qq "${SITE_PACKAGES_PATH}/$$layer.zip" -d "${SITE_PACKAGES_PATH}/"; then \
					echo -e ${FAIL}"-------------------------------------------------------------------------------"${END}; \
					echo -e ${FAIL}"[ERROR] HA OCURRIDO UN ERROR AL DESCOMPRIMIR LOS LAYERS A LA CARPETA DE DESTINO"${END}; \
					echo -e ${FAIL}"-------------------------------------------------------------------------------"${END}; \
					rm -rf ${LAYERS_CACHE_PATH}/layers
					rm -rf ${SITE_PACKAGES_PATH}/$$layer.zip
					exit 1
				fi
				if ! cp -a "${PYTHON_LAYER_PATH}/." ${SITE_PACKAGES_PATH}; then \
					echo -e ${FAIL}"-------------------------------------------------------------------------"${END}; \
					echo -e ${FAIL}"[ERROR] HA OCURRIDO UN ERROR AL INSTALAR LOS LAYERS EN EL ENTORNO VIRTUAL"${END}; \
					echo -e ${FAIL}"-------------------------------------------------------------------------"${END}; \
					rm -rf ${LAYERS_CACHE_PATH}/layers
					rm -rf ${SITE_PACKAGES_PATH}/$$layer.zip
					exit 1
				fi
				rm -rf "${SITE_PACKAGES_PATH}/$$layer.zip"; \
				rm -rf ${PYTHON_LAYER_PATH}; \
			fi; \
		done <<< "$$layers";
	@echo -e ${OKGREEN}"[OK] LAYERS INSTALADOS CORRECTAMENTE "${END};
	else \
		echo ""; \
		echo -e ${HEADER}"[INFO] NO HAY LAYERS CONFIGURADOS PARA INSTALAR "${END};
	fi;


# =============================================================================
# INVOCACIÓN DEL LAMBDA DE FORMA LOCAL
# - EDITA EL ARCHIVO event.yml PARA QUE LA INVOCACIÓN SE PUEDA REALIZAR
# - UTILIZA LOS LAYERS INSTALADOS EN EL ENTORNO VIRTUAL
# - UTILIZA LAS VARIABLES DE ENTORNO DEFINIDAS EN LA CARPETA SETUP
# =============================================================================

invoke_local:
	@if [[ ! "${LAMBDA}" ]]; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] DEBES ESPECIFICAR UN LAMBDA"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${LAMBDA_PATH}"; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] LAMBDA INDICADO NO EXISTE EN EL STACK"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${VIRTUALENV}"; then \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] NO EXISTE ENTORNO VIRTUAL CREADO PARA EL LAMBDA INDICADO"${END}; \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		exit 1
	fi
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
	@cd ${BACK_TWO_LEVELS}
	@if [[ "${TEST}" ]]; then \
		TEST_FILE="${TEST}"; \
	else \
		TEST_FILE="${DEFAULT_TEST_FILE}"; \
	fi
	@. ${BIN_ACTIVATE}
	@pip -q install pyyaml
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


# =============================================================================
# REALIZA LA INVOCACIÓN REMOTA DE UN LAMBDA PARA UN STAGE DEFINIDO
# =============================================================================

invoke_remote:
	@if [[ ! "${LAMBDA}" ]]; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] DEBES ESPECIFICAR UN LAMBDA"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${LAMBDA_PATH}"; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] LAMBDA INDICADO NO EXISTE EN EL STACK"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
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


# =============================================================================
# SE ENCARGA DE ELIMINAR EL ENTORNO VIRTUAL CREADO PARA UN LAMBDA
# =============================================================================

clean_env:
	@if [[ ! "${LAMBDA}" ]]; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] DEBES ESPECIFICAR UN LAMBDA"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${LAMBDA_PATH}"; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] LAMBDA INDICADO NO EXISTE EN EL STACK"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"LIMPIANDO ENTORNO VIRTUAL"${END};
	@if test -d "${VIRTUALENV}"; then \
		rm -rf ${VIRTUALENV}; \
		echo -e ${HEADER}"-----------------------------------------"${END};
		echo -e ${HEADER}"SE HA LIMPIADO EL ENTORNO VIRTUAL PARA EL LAMBDA ${LAMBDA}"${END};
		echo -e ${HEADER}"-----------------------------------------"${END};
	else
		echo -e ${HEADER}"-----------------------------------------"${END};
		echo -e ${HEADER}"AUN NO SE HA CREADO EL ENTORNO VIRTUAL"${END};
		echo -e ${HEADER}"-----------------------------------------"${END};
	fi


# =============================================================================
# SE ENCARGA DE ELIMINAR UN LAMBDA DE UN STACK
# - AL ELIMINAR UN LAMBDA, ACTUALIZA EL ARCHIVO serverless.yml del stack
# =============================================================================

remove:
	@if [[ ! "${LAMBDA}" ]]; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] DEBES ESPECIFICAR UN LAMBDA"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${LAMBDA_PATH}"; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] LAMBDA INDICADO NO EXISTE EN EL STACK"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if [[ "${LAMBDA}" ]]; then \
		PATH_TO_REMOVE="services/${LAMBDA}"; \
		TOTAL_LAMBDAS="$$(find services/* -maxdepth 0 -type d | wc -l)"
		@if [[ "$$TOTAL_LAMBDAS" == 1 ]]; then \
			echo -e ${WARNING}"-------------------------------------------------"${END};
			echo -e ${HEADER}[INFO]" NO PUEDES DEJAR EL STACK SIN NINGÚN LAMBDA"; \
			echo -e ${HEADER}"* Te sugerimos eliminar el stack completo"; \
			echo -e ${WARNING}"-------------------------------------------------"${END};
			exit
		fi
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

# =============================================================================
# CORRE LOS TESTS ASOCIADOS A UN LAMBDA
# =============================================================================

run_tests:
	@if [[ ! "${LAMBDA}" ]]; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] DEBES ESPECIFICAR UN LAMBDA"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${LAMBDA_PATH}"; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] LAMBDA INDICADO NO EXISTE EN EL STACK"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@if test ! -d "${VIRTUALENV}"; then \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] NO EXISTE ENTORNO VIRTUAL CREADO PARA EL LAMBDA INDICADO"${END}; \
		echo -e ${FAIL}"----------------------------------------------------------------"${END}; \
		exit 1
	fi
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"EJECUTANDO TESTS LOCALES"${END};
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@. ${BIN_ACTIVATE}
	@pip -q install pycodestyle
	@if ! python -m unittest discover ${LAMBDA_PATH}/tests "*_test.py"; then \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		echo -e ${FAIL}"[ERROR] ERRORES EN LOS TESTS EJECUTADOS"${END}; \
		echo -e ${FAIL}"---------------------------------------------"${END}; \
		exit 1
	fi
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"TESTS LOCALES FINALIZADOS"${END};
	@echo -e ${HEADER}"-----------------------------------------"${END};


# =============================================================================
# OBTIENE LA ULTIMA VERSION DE LOS LAYERS ASOCIADOS A UNA REGION
# =============================================================================

get_last_version_layers_cd:
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@echo -e ${HEADER}"OBTENIENDO LAS ULTIMAS VERSIONES DE LAYERS"${END};
	@echo -e ${HEADER}"-----------------------------------------"${END};
	@for dir in services/*/; \
		do \
			lambda="$$( echo $$dir | cut -d'/' -f2 -s )"; \
			INIT_LAYERS="$$(jq -c '(.LAYERS[])' services/$$lambda/setup/${STAGE}/config.json)"; \
		    REGION="$$( jq -c "(.${PROFILE}).REGION" setup/stage/${STAGE}.json )"; \
			REGION="$$( sed -e 's/^"//' -e 's/"$$//' <<<"$$REGION" )"; \
			CONFG_FILE="services/$$lambda/setup/${STAGE}/config.json"; \
			LIST_NEW_LAYERS="["; \
			while read -r layer; do \
				layer_name="$$( echo $$layer | cut -d':' -f7 -s )" \

				last_version=$$(aws lambda \
					list-layer-versions \
					--layer-name $$layer_name \
					--region $$REGION \
					--query 'LayerVersions[0].LayerVersionArn' \
					); \
				
				if [[ ! "$$last_version" ]]; then \
					echo -e ${FAIL}"---------------------------------------------------"${END}; \
					echo -e ${FAIL}"[ERROR] NO FUE POSIBLE OBTENER LAS ULTIMAS VERSIONES PARA EL STAGE ${STAGE}"${END}; \
					echo -e ${FAIL}"---------------------------------------------------"${END}; \
					exit 1
				fi; \

				if [[ "$$last_version" == "null" ]]; then \
					echo -e ${FAIL}"---------------------------------------------------"${END}; \
					echo -e ${FAIL}"[ERROR] NO SE PUDO OBTENER LA VERSION PARA EL LAYER $$layer"${END}; \
					echo -e ${FAIL}"---------------------------------------------------"${END}; \
				else \
					LAYER_LINE="$$last_version,"; \
					LIST_NEW_LAYERS="$$LIST_NEW_LAYERS$$LAYER_LINE"; \
				fi
			done <<< "$$INIT_LAYERS"; \

			if [[ $$LIST_NEW_LAYERS == *, ]]; then
				LIST_NEW_LAYERS=$$( echo "$$LIST_NEW_LAYERS" | sed 's/\(.*\),/\1 /' )			
			fi
			LIST_NEW_LAYERS="$$LIST_NEW_LAYERS]"

			jq "(. ).LAYERS = $$LIST_NEW_LAYERS" "$$CONFG_FILE" > tmp.json
			JSON_FILE=$$(jq . tmp.json)
			echo "$$JSON_FILE" > services/$$lambda/setup/${STAGE}/config.json
			rm -rf tmp.json
	done


# =============================================================================
# GUÍA CON COMANDOS DE AYUDA
# =============================================================================

help:
	@echo ''
	@echo -e ${HEADER}"-------------------------------------------------------------------------"${END};
	@echo  'Commands:'
	@echo -e ${HEADER}"-------------------------------------------------------------------------"${END};
	@echo 'prepare                  - Se encarga de preparar el entorno virtual para'
	@echo '                           realizar invocaciones locales de lambdas.'
	@echo '                           * Parametros:'
	@echo '                             - LAMBDA=lambda_del_stack'
	@echo ''
	@echo 'install_remote_layers    - Encargado de instalar los layers remotos en el'
	@echo '                           entorno virtual local. Estos layers vienen de'
	@echo '                           la configuracion para el stage dev. Es necesario'
	@echo '                           tener el entorno virtual local creado para el'
	@echo '                           lambda definido.'
	@echo '                           * Parametros:'
	@echo '                             - LAMBDA=lambda_del_stack'
	@echo ''
	@echo 'install_local_layers     - Se encarga de instalar layers locales en el'
	@echo '                           entorno virtual local. Para instalarlos, es'
	@echo '                           necesario tener el proyecto legolayers al mismo'
	@echo '                           nivel del repositorio de los stacks, además'
	@echo '                           de tener el entorno virtual local creado para'
	@echo '                           el lambda definido.'
	@echo '                           * Parametros:'
	@echo '                             - LAMBDA=lambda_del_stack'
	@echo ''
	@echo 'invoke_local             - Se encarga de invocar la función en local'
	@echo '                           con todos los layers instalados anteriormente,'
	@echo '                           además de las variables de entorno definidas para'
	@echo '                           el stage dev.'
	@echo '                           * Parametros:'
	@echo '                             - LAMBDA=lambda_del_stack'
	@echo ''
	@echo 'invoke_remote            - Realiza la invocación de un lambda remoto,'
	@echo '                           directamente en la región de aws definida'
	@echo '                           para el stage entregado.'
	@echo '                           * Parametros:'
	@echo '                             - LAMBDA=lambda_del_stack'
	@echo '                             - STAGE=dev'
	@echo ''
	@echo 'clean_env                - Elimina el entorno virtual creado para un'
	@echo '                           lambda.'
	@echo '                           * Parametros:'
	@echo '                             - LAMBDA=lambda_del_stack'
	@echo ''
	@echo 'remove_lambda            - Se encarga de eliminar un lambda de un stack.'
	@echo '                           * Parametros:'
	@echo '                             - LAMBDA=lambda_del_stack'
	@echo ''
	@echo 'run_tests                - Se encarga de ejecutar los tests ubicados en'
	@echo '                           la carpeta core/tests de cada lambda.'
	@echo '                           * Parametros:'
	@echo '                             - LAMBDA=lambda_del_stack'
	@echo ''
	@echo -e ${HEADER}"-------------------------------------------------------------------------"${END};
	