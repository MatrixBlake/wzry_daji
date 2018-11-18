import os
from PIL import Image, ImageOps
from pytesseract import *
import numpy as np
import sys

screen_width=1920
screen_height=1080
magic_penetration_value=9

position=int(sys.argv[1])
items=int(sys.argv[2])
level=int(sys.argv[3])

def calculate_damage(level, magic_penetration_value, ability_power, life, magic_resistance, items):
    magic_penetration_percentage=1
    if(items>=2):
        magic_penetration_value+=75
    if(items>=5):
        magic_penetration_percentage=0.55
    first_aibility = 585+1.22*ability_power
    second_ability = 285+0.66*ability_power
    ultra_ability = 325+0.75*ability_power
    if(level>=5):
        first_aibility+=65
        if(level>=6):
            second_ability+=35
            if(level>=7):
                first_aibility+=65
                if(level>=8):
                    ultra_ability += 80
                    if(level>=9):
                        first_aibility+=65
                        if(level>=10):
                            second_ability+=35
                            if(level>=11):
                                first_aibility+=65
                                if(level>=12):
                                    ultra_ability+=80
                                    if(level>=13):
                                        second_ability+=(level-12)*35

    magic_resistance-=27+3*level
    magic_resistance_true = (magic_resistance-magic_penetration_value)*magic_penetration_percentage
    if(magic_resistance_true<0):
        magic_resistance=0
    second_ability_damage=second_ability*601/(magic_resistance_true+601)
    life-=second_ability_damage
    if(items>=2):
        pain_mask = life*0.08*601/(magic_resistance_true+601)
        life-=pain_mask
        if(items>=4):
            echo = (50+0.5*ability_power)*601/(magic_resistance_true+601)
            life -= echo

    magic_resistance-=27+3*level
    magic_resistance_true = (magic_resistance-magic_penetration_value)*magic_penetration_percentage
    if(magic_resistance_true<0):
        magic_resistance=0
    ultra_ability_1=ultra_ability*601/(magic_resistance_true+601)

    magic_resistance-=27+3*level
    magic_resistance_true = (magic_resistance-magic_penetration_value)*magic_penetration_percentage
    if(magic_resistance_true<0):
        magic_resistance=0
    ultra_ability_2=ultra_ability*601/2/(magic_resistance_true+601)
    ultra_ability_3=ultra_ability*601*0.75/2/(magic_resistance_true+601)
    ultra_ability_4=ultra_ability*601/2/(magic_resistance_true+601)
    ultra_ability_5=ultra_ability*601/2/(magic_resistance_true+601)

    life-=ultra_ability_1
    life-=ultra_ability_2
    life-=ultra_ability_3
    life-=ultra_ability_4
    life-=ultra_ability_5

    first_aibility_damage = first_aibility*601/(magic_resistance_true+601)
    life -=first_aibility_damage

    return int(life)




os.system('adb shell screencap -p /sdcard/1.png')
print("截图完毕")
os.system('adb pull /sdcard/1.png .')

img = Image.open('C:\\Users\\wkz\\1.png').convert('RGB')
inverted_image = ImageOps.invert(img)


ability_power_range=np.zeros((6,4))
enemy_life_range=np.zeros((6,4))
enemy_magic_resistance_range=np.zeros((6,4))
level_range=np.zeros((6,4))
for i in range(1,6):
    ability_power_range[i]=np.array([int(474*screen_width/1920), int((133*i+210)*screen_height/1080), int(572*screen_width/1920), int((133*i+273)*screen_height/1080)])
    enemy_life_range[i]=np.array([int(1220*screen_width/1920), int((133*i+210)*screen_height/1080), int(1330*screen_width/1920), int((133*i+273)*screen_height/1080)])
    enemy_magic_resistance_range[i]=np.array([int(1620*screen_width/1920), int((133*i+210)*screen_height/1080), int(1730*screen_width/1920), int((133*i+273)*screen_height/1080)])
    level_range[i]=np.array([int(29*screen_width/1920), int((132*i+246)*screen_height/1080), int(55*screen_width/1920), int((132*i+273)*screen_height/1080)])


ability_power_image=inverted_image.crop(ability_power_range[position])
ability_power_image.save("ability_power.jpg")
ability_power_string=image_to_string(ability_power_image)
ability_power=int(ability_power_string)

print("你现在"+str(level)+"级，你的法强是"+str(ability_power))

for i in range(1,6):
    life_image=inverted_image.crop(enemy_life_range[i])
    life=int(image_to_string(life_image))
    magic_resistance_image=inverted_image.crop(enemy_magic_resistance_range[i])
    magic_resistance=int(image_to_string(magic_resistance_image))

    life_remain=calculate_damage(level, magic_penetration_value, ability_power, life, magic_resistance, items)

    print("第"+str(i)+"个敌人有"+str(life)+"血，他的魔抗是"+str(magic_resistance)+"，你一套三连可以打掉他"+str(life-life_remain)+"的血，百分比为"+str(int((life-life_remain)/life*100))+"%")



