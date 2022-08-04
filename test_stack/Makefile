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