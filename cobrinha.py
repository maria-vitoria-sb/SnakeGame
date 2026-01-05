import pygame
import random

pygame.init()
pygame.display.set_caption("Jogo Snake Python")
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# cores RGB (inicial)
corFundo = (8, 54, 1)  
corPontos = (124, 252, 0)
vermelha = (255, 0, 0)

# fase 1 - verde (padrão)
verdeFundo = (8, 54, 1)
verdePontos = (124, 252, 0)
verdeEscuro = (6, 158, 6)
verdeClaro = (50, 205, 50)

# fase 2 - azul
azulFundo = (2, 27, 71)
azulPontos = (176, 224, 230)
azulEscuro = (0, 71, 171)
azulClaro = (135, 206, 235)

# fase 3 - rosa
rosaFundo = (173, 0, 95)
rosaPontos = (255, 182, 193)
rosaEscuro = (251, 37, 157)
rosaClaro = (255, 192, 203)

# fase 4 - amarelo (final)
amareloFundo = (242, 173, 37)
amareloPontos = (255, 240, 97)
amareloEscuro = (255, 198, 66)
amareloClaro = (251, 236, 93)

# parametros da cobrinha
tamanho_quadrado = 10
velocidade_jogo = 15

# selecao de cor por fase
def selecionar_cores(pontuacao):
    # Retorna: corCobra, corComida, corFundo, corPontos
    if pontuacao < 5:
        return verdeClaro, verdeEscuro, verdeFundo, verdePontos
    elif pontuacao < 10:
        return azulClaro, azulEscuro, azulFundo, azulPontos
    elif pontuacao < 15:
        return rosaClaro, rosaEscuro, rosaFundo, rosaPontos
    else:
        return amareloClaro, amareloEscuro, amareloFundo, amareloPontos

# funcoes auxiliares
def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
    return comida_x, comida_y


def desenhar_comida(tamanho, x, y, cor):
    pygame.draw.rect(tela, cor, [x, y, tamanho, tamanho])


def desenhar_cobra(tamanho, pixels, cor):
    for pixel in pixels:
        pygame.draw.rect(tela, cor, [pixel[0], pixel[1], tamanho, tamanho])


def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontuacao}", True, corPontos)
    tela.blit(texto, [1, 1])


def selecionar_velocidade(tecla):
    if tecla in (pygame.K_DOWN, pygame.K_s):
        return 0, tamanho_quadrado
    elif tecla in (pygame.K_UP, pygame.K_w):
        return 0, -tamanho_quadrado
    elif tecla in (pygame.K_RIGHT, pygame.K_d):
        return tamanho_quadrado, 0
    elif tecla in (pygame.K_LEFT, pygame.K_a):
        return -tamanho_quadrado, 0
    return 0, 0

# tela de fim de jogo
def tela_fim_jogo():
    fonte = pygame.font.SysFont("Helvetica", 50, bold=True)
    fonte_menor = pygame.font.SysFont("Helvetica", 30)

    perdeu_texto = fonte.render("Você perdeu!!!", True, vermelha)
    reiniciar_texto = fonte_menor.render("Pressione ENTER para reiniciar", True, vermelha)

    while True:
        tela.fill((0, 0, 0))

        tela.blit(perdeu_texto, (largura/2 - perdeu_texto.get_width()/2,
                                 altura/2 - perdeu_texto.get_height()))
        
        tela.blit(reiniciar_texto, (largura/2 - reiniciar_texto.get_width()/2,
                                    altura/2 + 20))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: 
                    rodar_jogo()
                    return

# tela de vitoria
def tela_venceu_jogo():
    fonte = pygame.font.SysFont("Helvetica", 50, bold=True)
    fonte_menor = pygame.font.SysFont("Helvetica", 30)

    venceu_texto = fonte.render("Você venceu!!!", True, (255, 255, 255))
    reiniciar_texto = fonte_menor.render("Pressione ENTER para reiniciar", True, (255, 255, 255))

    while True:
        tela.fill((0, 0, 0)) 

        tela.blit(venceu_texto, (largura/2 - venceu_texto.get_width()/2,
                                 altura/2 - venceu_texto.get_height()))
        
        tela.blit(reiniciar_texto, (largura/2 - reiniciar_texto.get_width()/2,
                                    altura/2 + 20))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: 
                    rodar_jogo()
                    return

# loop principal
def rodar_jogo():
    global corFundo, corPontos  # agora são variáveis atualizadas por fase

    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while True:

        # fundo da fase atual
        tela.fill(corFundo)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)

        # colisão borda
        if x < 0 or x >= largura or y < 0 or y >= altura:
            tela_fim_jogo()

        # movimento da cobra
        x += velocidade_x
        y += velocidade_y

        # corpo
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        # colisão com si mesma
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                tela_fim_jogo()

        # pontuação
        pontuacao = tamanho_cobra - 1

        # cores por fases
        corCobra, corComida, corFundo, corPontos = selecionar_cores(pontuacao)

        # desenhar comida e cobra
        desenhar_comida(tamanho_quadrado, comida_x, comida_y, corComida)
        desenhar_cobra(tamanho_quadrado, pixels, corCobra)

        # desenhar pontos
        desenhar_pontuacao(pontuacao)

        # venceu
        if pontuacao == 20:
            tela_venceu_jogo()

        # comeu comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()

        pygame.display.update()
        relogio.tick(velocidade_jogo)

rodar_jogo()
