command="docker run -d --env-file zinc_app/envs/.env  -p 5000:5000 --name zinc_app_container zinc_app"
echo $command
eval $command