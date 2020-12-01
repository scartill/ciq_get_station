del publish.zip
powershell Compress-Archive src/* publish.zip 
aws lambda update-function-code --function-name ciq-get-station --zip-file "fileb://publish.zip"

