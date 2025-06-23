ibmcloud target -r us-south -g cc-6920005y08-xtkrbmqm
ibmcloud ce project select --id a68dc6ad-2318-41ee-b944-a6172b8bce00
# ibmcloud ce registry create --name nicole-registry-4 --server us.icr.io --username iamapikey --password "$IBM_API_KEY_CR"
# ibmcloud ce secret create --name env-nicole-1 --from-env-file .env
ibmcloud ce build create --name test-build --registry-secret nicole-registry-4 --build-type local --image us.icr.io/cc-6920005y08-xtkrbmqm-cr/hr-skills
ibmcloud ce buildrun submit --build test-build --name test-run --wait