import pygame, sys
import pygame.freetype

###CONSTS
# Set to true or add 'showevent' in argv to see IME and KEYDOWN events
PRINT_EVENT = False
# frames per second, the general speed of the program
FPS = 50
# size of window
WINDOWWIDTH, WINDOWHEIGHT = 640, 480 
BGCOLOR = (0, 0, 0)

# position of chatlist and chatbox
CHATLIST_POS = pygame.Rect(0, 20, WINDOWWIDTH, 400)
CHATBOX_POS = pygame.Rect(0, 440, WINDOWWIDTH, 40)
CHATLIST_MAXSIZE = 20

TEXTCOLOR = (0,255,0)

#Add fontname for each language, otherwise some text can't be correctly displayed.
FONTNAMES = ["notosanscjktcregular", "notosansmonocjktcregular" ,
            "notosansregular,", 
            "microsoftjhengheimicrosoftjhengheiuilight",
            "microsoftyaheimicrosoftyaheiuilight",
            "msgothicmsuigothicmspgothic",
            "msmincho",
            "Arial"]

#Version check
if (pygame.get_sdl_version() < (2,0,0)):
    raise Exception("This example requires SDL2.")

#Initalize
pygame.init()
Screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption("TextInput example")
FPSClock = pygame.time.Clock()

#Freetype
#"The font name can be a comma separated list of font names to search for."
FONTNAMES = ",".join(str(x) for x in FONTNAMES)
Font = pygame.freetype.SysFont(FONTNAMES, 24)
FontSmall = pygame.freetype.SysFont(FONTNAMES, 16)
print("Using font: " + Font.name)

#Main loop process
def main():
    global BGCOLOR, PRINT_EVENT, CHATBOX_POS, CHATLIST_POS, CHATLIST_MAXSIZE
    global FPSClock , Font, Screen
    
    """
    https://wiki.libsdl.org/SDL_HINT_IME_INTERNAL_EDITING
    https://wiki.libsdl.org/Tutorials/TextInput
    Candidate list not showing due to SDL2 problem ;w;
    """
    pygame.key.start_text_input()
    input_rect = pygame.Rect(80,80,320,40)
    pygame.key.set_text_input_rect(input_rect)

    _IMEEditing = False
    _IMEText = ""
    _IMETextPos = 0
    _IMEEditingText = ""
    _IMEEditingPos = 0
    ChatList = []
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            elif event.type == pygame.KEYDOWN:
                if (PRINT_EVENT):
                    print(event)

                if _IMEEditing:
                    if (len(_IMEEditingText) == 0):
                        _IMEEditing = False
                    continue
                
                if event.key == pygame.K_BACKSPACE:
                    if (len(_IMEText) > 0 and _IMETextPos > 0):
                        _IMEText = _IMEText[0:_IMETextPos-1] + _IMEText[_IMETextPos:]
                        _IMETextPos = max(0,_IMETextPos-1)
                        
                elif event.key == pygame.K_DELETE:
                    _IMEText = _IMEText[0:_IMETextPos] + _IMEText[_IMETextPos+1:]
                elif event.key == pygame.K_LEFT:
                    _IMETextPos = max(0,_IMETextPos-1)
                elif event.key == pygame.K_RIGHT:
                    _IMETextPos = min(len(_IMEText),_IMETextPos+1)
                    
                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER] and len(event.unicode) == 0:
                    #Block if we have no text to append
                    if len(_IMEText) == 0:
                        continue

                    #Append chat list
                    ChatList.append(_IMEText)
                    if (len(ChatList) > CHATLIST_MAXSIZE):
                        ChatList.pop(0)
                    _IMEText = ""
                    _IMETextPos = 0
                    
            elif event.type == pygame.TEXTEDITING:
                if (PRINT_EVENT):
                    print(event)
                _IMEEditing = True
                _IMEEditingText = event.text
                _IMEEditingPos = event.start

            elif event.type == pygame.TEXTINPUT:
                if (PRINT_EVENT):
                    print(event)
                _IMEEditing = False
                _IMEEditingText = ""
                _IMEText = _IMEText[0:_IMETextPos] + event.text + _IMEText[_IMETextPos:]
                _IMETextPos += len(event.text)
                
        #Screen updates
        Screen.fill(BGCOLOR)
        
        #Chat List updates
        chat_height = CHATLIST_POS.height / CHATLIST_MAXSIZE
        for i in range(len(ChatList)):
            FontSmall.render_to(Screen, (CHATLIST_POS.x, CHATLIST_POS.y + i*chat_height), ChatList[i], TEXTCOLOR)
            
        #Chat box updates
        start_pos = CHATBOX_POS.copy()
        ime_textL = ">" + _IMEText[0:_IMETextPos]
        ime_textM = _IMEEditingText[0:_IMEEditingPos] + "|" + _IMEEditingText[_IMEEditingPos:]
        ime_textR = _IMEText[_IMETextPos:]
        
        rect_textL = Font.render_to(Screen, start_pos, ime_textL, TEXTCOLOR)
        start_pos.x += rect_textL.width
        
        #Editing texts should be underlined
        rect_textM = Font.render_to(Screen, start_pos, ime_textM, TEXTCOLOR, None, pygame.freetype.STYLE_UNDERLINE)
        start_pos.x += rect_textM.width
        rect_textr = Font.render_to(Screen, start_pos, ime_textR, TEXTCOLOR)
        
        pygame.display.update()
        
        FPSClock.tick(FPS)
        
if __name__ == '__main__':
    if 'showevent' in sys.argv:
        PRINT_EVENT = True
    
    main()
