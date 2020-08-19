import Services.walletTelegramService.WalletTelegramService as WalletBotLogic

if __name__ == '__main__':
    WalletBotLogic.start_bot()


# TODO
#   Arranjar forma de organizar melhor os services
#   Apresentar funções disponíveis no comando help, ou quando insere algo nao esperado
#   Criar repository com logica do firebase
#   Criar resources
#   Criar um ID random em vez do ID de registo do firebase
#   Criar mais opções inline
#   Organizar logica de criação dos comandos e opções
