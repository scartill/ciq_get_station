del publish.zip
powershell Compress-Archive src/* publish.zip 
aws lambda update-function-code --function-name ciq_get_station --zip-file "fileb://publish.zip"

