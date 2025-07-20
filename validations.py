import re
def validacaoNome(nome,usuarios):
        '''  
        Verifica se o nome está vazio, contém caracteres especiais, ou se já está salvo em outro usuário
        
        Parâmetros:
            nome (str): Nome a ser validado.

        Retorna:
            bool: True se o nome for validado, e False caso não seja.
        '''
        if not nome:
            print("\033[31m[ERRO], o nome não pode estar vazio\033[m")
            return False
        
        for usuario in usuarios:
            if usuario.nome == nome:
                print("\033[31m[ERRO], nome já existente, tente novamente\033[m")
                return False
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', nome): 
            print("\033[31m[ERRO], o nome não pode conter caracteres especiais\033[m")
            return False
        return True
    
def validacaoEmail(email,usuarios):

        """
        Verifica se o email termina com um dos domínios válidos, ou se é um espaço vazio ou se já existe.

        Parâmetros:
            email (str): Email a ser validado.

        Retorna:
            bool: True se o email for válido, False caso contrário.
        """
        if not email:
            print("\033[31m[ERRO],o email não pode estar vazio\033[m")
            return False
        
        for usuario in usuarios:
            if usuario.email == email:
                print("\033[31m[ERRO], Email já existente,tente novamente\033[m")
                return False
        
            
        dominios_validos = ("@gmail.com", "@hotmail.com", "@yahoo.com")
        if not email.endswith(dominios_validos):
            print("\033[31m[ERRO], utilize um domínio válido(@gmail.com,@hotmail.com,@yahoo.com)\033[m")
            return False
        
        return True
             #Verifica se o email termina com os domínios válidos
        

def validacaoSenha(senha):
       
       """
        Verifica se a senha atende aos critérios de complexidade.

        Parâmetros:
            senha (str): Senha a ser validada e que deve conter, 1 letra maiúscula, 1 caractere especial, 1 número e no mínimo 8 digitos.

        Retorna:
            bool: True se a senha for considerada forte, False caso contrário.
        """
       if len(senha) < 8: return False
       if not re.search(r'[A-Z]',senha): return False 
       if not re.search(r'[0-9]', senha): return False
       if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha): return False
       return True
        