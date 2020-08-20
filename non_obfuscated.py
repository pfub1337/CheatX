import pymem
import pymem.process
import requests
from threading import Thread
import keyboard
import os
from time import sleep


logo = """
                     ..,,,**///((###%%%&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&%%%###((//***,,...                    
                                                                                                                        
                                                                                                                        
.***.           */#/,          */#/.          *((*                &@@@/                                                 
#@@/#@@@.   *@@@&(/#@@@%   *@@@&(/#@#      ,@@&. %@              .@@   .@@                                              
#@@  /@@.  (@@/           /@@/             ,@@@(.       /&&&%,  ,%@@%##%@@%#%#.   /%    (##.  *%&%*(%#  %#//&%   (&&&(  
#@@%%&@@%  %@@    *@@@@@@ %@@                 *#@@@&  @@&,  (@@/ .@@   .@@  /@@* %@@@. &@&  (@@/  ,@@@  @@&.   &@&   #@%
#@@   .@@# .@@@.     (@@. .@@@,     ,       #    #@@,.@@#    @@% .@@   .@@   .@@@@(.@@@@(   %@&    %@@  @@#    @@#......
#@@@@@@@*     &@@@@@@@*      %@@@@@@#       &@@@@@@    %@@@@@@,  .@@   .@@     %@/   &@.     /@@@@@@@@  @@#     %@@@@@& 
                                                                                                                        
                                                                                                                        
                    ...,,,**//(((###%%&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&%%%###((///**,,,..                    
                                                     CODE BY pfub
"""
os.system("cls")
print(logo)
sleep(1)


print("Running cheat...")

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

print("Taking offsets...")

offsets = "https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json"
response = requests.get(offsets).json()

dwGlowObjectManager = int(response["signatures"]["dwGlowObjectManager"])
dwEntityList = int(response["signatures"]["dwEntityList"])
dwForceAttack = int(response["signatures"]["dwForceAttack"])
dwForceJump = int(response["signatures"]["dwForceJump"])
dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])

m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
m_iGlowIndex = int(response["netvars"]["m_iGlowIndex"])
m_iCrosshairId = int(response["netvars"]["m_iCrosshairId"])
m_fFlags = int(response["netvars"]["m_fFlags"])

activateTrigger = False
activateWH = False
activateBHop = False


def check_press_button(e):
    global activateBHop, activateWH, activateTrigger
    if (e.event_type == "up") and (e.name == "insert"):
        activateWH = not activateWH
        console_ui()
    elif (e.event_type == "up") and (e.name == "right alt"):
        activateBHop = not activateBHop
        console_ui()
    elif (e.event_type == "up") and (e.name == "shift"):
        activateTrigger = not activateTrigger
        console_ui()


keyboard.hook(check_press_button)


def console_ui():
    os.system("color a")
    os.system("cls")
    print(logo)
    controls = """
                                               CheatX version test 1.0
                                        ====================================
                                                       CONTROLS             
                                                Insert - On/Off Wallhack     
                                              Right Alt - On/Off Bunnyhop
                                               Caps Lock - On/Off Trigger   
                                        ====================================
    """
    status = """
                                        ====================================
                                                        STATUS             
                                                    Wallhack - {}         
                                                    Bunnyhop - {}
                                                  Trigger Bot - {}         
                                        ====================================
    """.format("enabled" if activateWH else "disabled", "enabled" if activateBHop else "disabled", "enabled" if activateTrigger else "disabled")
    print(controls, status)
    # print("Wallhack - enabled" if activateWH else "Wallhack - disabled")
    # print("Bunnyhop - enabled" if activateBHop else "Bunnyhop - disabled")


def cheat():
    shooting = False
    while True:
        glow_manager = pm.read_int(client + dwGlowObjectManager)
        localplayer = pm.read_int(client + dwLocalPlayer)

        for i in range(1, 32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity and activateWH:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if entity_team_id == 2:     # T-side
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))   # Red
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0.5))     # Green
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # Blue
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)


                if entity_team_id == 3:     # CT-side
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0.5))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)

        if keyboard.is_pressed("space") and activateBHop:
            flags_num = pm.read_int(localplayer + m_fFlags)
            if flags_num == 256:
                pm.write_int(client + dwForceJump, 4)
            else:
                pm.write_int(client + dwForceJump, 5)

        if activateTrigger:  # and activateTrigger keyboard.is_pressed("shift")
            CrosshairEntity = pm.read_int(client + m_iCrosshairId)
            if (CrosshairEntity > 0) and (CrosshairEntity <= 64):
                CrosshairEntity = pm.read_int(client + dwEntityList + (CrosshairEntity - 1) * 0x10)
                CrosshairEntity_team = pm.read_int(CrosshairEntity + m_iTeamNum)
                localplayer_team = pm.read_int(localplayer + m_iTeamNum)
                if localplayer_team != CrosshairEntity_team:
                    shooting = True
                    pm.write_int(client + dwForceAttack, 5)
            if not keyboard.is_pressed("shift") and shooting is True:
                pm.write_int(client + dwForceAttack, 4)
                shooting = False





Thread(target=cheat).start()
console_ui()


secret = """
          ,)(8)).
        (()))())()).
       (()"````"::= )
       )| _    _ ::= )
      (()(o)/ (o) ?(/)
       )(::c ::.( :(/)
      (( \ .__. ;,/(/)
        ) `.___,'/ (/)
           |    | (/)
         _.'    ,\(/)__
     _.-"   ` u    (/) ".
   ,"               ^    \ 
  /                      |
  |           .      `.  |
  |   /,'   _  `.'   _ `.|
  |   ||   (o)  |   (o) ||
  |   |\        ;       /)
  (   \ `.,___,' `.,__,'/
   \   \ |           | /
    \   `;           |/
     `. /            |
       Y             |
      /          (   |
     /               ;
    /               /
   ;       ` .    ,'(
   |          \##'   \ 
   :           Y      \ 
    \           \      \ 
     \           \      \ 
      \           \      \ 
"""


def secret_text():
    os.system("cls")
    print("CONGRATULATIONS!\n U FINDED EASTER EGG!\n U REALLY CRAZY!")
    sleep(2)
    os.system("cls")
    print(secret)
    print("Do u like what u see? :D")
    sleep(5)
    console_ui()

keyboard.add_hotkey("Ctrl + Enter + F1", secret_text)
