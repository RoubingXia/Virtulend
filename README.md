# Virtulend
The scraper of Virtulend which will get all VR apps information from Steam

## Usage:
 Check if docker installed in your local environment

`docker -version`

Clone the repo to your local, replace the **git_repo_link** to the actual line of current repo


`git clone git_repo_link`


Execute the scraper by following commands, replace **YourLocalPath** to you actual local path

`docker build -f docker/Dockerfile . -t steamscraper`

`docker run -v /YourLocalPath/Virtulend:/app steamscraper`
## Result:
The result files will be in Virtulend folder

 **games.json** : the information of each VR game in json format

 **notreleased.json** : App ids of games that haven't been released yet
