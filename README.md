# TweetsTake

Application to get tweets of Twitter on specific topics. Specially designed for Big Data collection.
<br>
<br>

---


## Execution without installation (docker)
Requirements: Docker Engine installed (https://docs.docker.com/engine/installation)
```sh
To pending ...
```

## Installation (Linux and Mac OSX)
*NOTE: it is recommended to run the application without installing. Look above.*  
Requirements: 3.6.1+ installed and available MongoDB database

### Requirements
* Python 3.6.1+
* python3.6-dev
* python3-setuptools
* python3-pip
* MongoDB database (local or remote)

### Installation steps
```sh
clone or download and unzip this project
$ cd tweetstake
$ sudo python3.6 setup.py install
$ tweetstake -h       # -h show help
```

## Before starting: csv file
You must go to [https://apps.twitter.com/](https://apps.twitter.com/), create an app with your account and generate tokens. If you are going to collect tweets with several search criteria at the same time it is preferable that you create several accounts with their respective apps and tokens.
Then, you must create a **.csv file** and write the tokens in the following format. The first line must be the same. The rest of the lines represent an account with their respective tokens. Each token must be separated by a comma.

*example_file.scv*
```sh
consumer_key,consumer_secret,token_key,token_secret
uGvo8uIN2wg5nKvWfmBuSjmTv,bx4yTUiav6dJvqkWo8VvxSORyrRHApUMPldrZrHcAmTg6AXl6X,150147078634094680-WItRgONsdhhZc6C7q8n9NWDvYG94aVB,qQ7qj6dbfhbqc69EPSVFzMvPpjy1Rl91RdiJ6WzzKUIas
```

## Before starting: mongodb database

You must have a **mongodb** database available. By default the name of the database and the host are 'tweetscollector' and 'localhost:27017'. These values can be changed.

## Examples

**Collect tweets with '#hello' for 6 hours:**
```console
 tweetstake -accounts_file ~/file2.csv -filter '#hello' -hours 6
```

**Collect tweets with '#hello' for 15 minutes, specifying parameters of the mongodb database:**
```console
 tweetstake -accounts_file ~/file2.csv -filter '#hello' -minutes 15 -db_name 'mydbname' -db_host 'mongodb://db1.example.net:27017'
```

**Collect tweets with '#hello' or '#bye' for 6 hours and 30 minutes:**
```console
 tweetstake -accounts_file ~/file2.csv -filter '#hello' '#bye' -hours 6 -minutes 30
```


## License
[MIT](LICENSE) (Massachusetts Institute of Technology)
