command="docker run -d --restart=on-failure --env-file zinc_app/envs/.env  -p 5000:5000 --name zinc_app_container nguyennt63/zinc_app"
echo $command
eval $command