import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((100,100))

def getKey(keyName):
    answer = False
    for eve in pygame.event.get():pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput [myKey]:
        answer = True
    pygame.display.update()+

    return answer+lane
def main():
    if getKey('LEFT'):
        print('Left Key was pressed')
    if getKey('RIGHT'):
        print('Right Key was pressed')

if __name__ == '__main__':
    init()
    while True:
        main()