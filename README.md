# Wallty Bot

Simple pet project with the goal goal of managing the balance of a wallet using a telegram bot and firebase database

## Getting Started

In order to deploy this project to your machine you will need to do the following:

Clone the project to your machine

```
    git clone git@gitlab.com:Highdawn/wallty-bot.git
```

Make a copy of the configuration example file
```
    cp .config.example .config
```


### Prerequisites

The project will require the following packages:
 * python-firebase
 * telepot 
 
In order to install all of the required packages you can run the following command in your command line

```
    pip install -r requirements.txt
```

### Installing

In order to make the project work, we will need add some informations to the configuration file

1. Get the url to the firebase database into the "Url" value

```
    [FIREBASE]
    Url = https://(NAME_OF_YOUR_PROJECT).firebaseio.com/
```

2. Get the token of your telegram bot

```
    [TELEGRAM]
    BotToken = (BOT_TOKEN)
```

After this you can run some tests by running the main.py file and chat with the bot you created

### Project Design Pattern

The project is organized using the services design pattern, this is implemented in order to split the responsability of
each element of the project and make it easier to maintain. For example:

* firebaseService - All functions related to firebase
* telegramService - All functions related to telegram
* walletService - All functions related to the logic of the wallet
* walletTelegramService - All function related to the logic of the wallet with connection to telegram

## Authors

* **[Highdawn](https://gitlab.com/Highdawn)** - *Initial work*


## Future Developments

| Task | Current Status | Finished | 
|------|----------------|----------|
| Refactor project organization | Planned | 
| Add more information to help function  | Planned | 
| Try to add repository design pattern based on firebase   | Planned | 
| Try to add resources design pattern based on telegram bot communication  | Planned | 
| Create wallet ID randomly and not based on firebase doc id  | Planned | 
| Add more inline options   | Planned | 
| Make bot script configuration a easier process   | Planned | 
| Object Cache   | Planned | 

