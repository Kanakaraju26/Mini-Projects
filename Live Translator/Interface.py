from translator_modules import *
import googletrans as gt
# from google_trans_new import google_translator  as gt
import dearpygui.dearpygui as dpg
import time
import os
import sys


def setting_conversation(inputted_lang, targeted_lang, flag):
    os.system('cls')
    dpg.set_item_label("Exit Program", "Say Stop To Terminate the the program")
    # print(f"'{inputted_lang}' will speak now.")
    if flag:
        dpg.set_value("label2", "Here Will Be Your First second Conversion")
        dpg.set_value("label1", f"'{inputted_lang}' will speak now.")
        time.sleep(1)
        dpg.set_value("label1", "I'm Listening... ")
    else:
        dpg.set_value("label1", "Here Will Be Your First Person Conversion")
        dpg.set_value("label2", f"'{inputted_lang}' will speak now.")
        time.sleep(1)
        dpg.set_value("label2", "I'm Listening... ")

    text = get_voice_input()
    if text is not None:
        translated = voice_conversion(text, targeted_lang)
        if flag:
            dpg.set_value("first_person_text", text)
            file1 = open("first_person_conversion.txt", "a")
            file1.write("\n"+text)
            file1.close()
        else:
            dpg.set_value("second_person_text", text)
            file2 = open("second_person_conversion.txt", "a")
            file2.write("\n"+text)
            file2.close()
        text_to_voice(translated, targeted_lang)
        play_sound(output_file)
        closing = voice_conversion(text, 'en')
        if "stop" in closing.lower():
            print("Exiting Program....")
            dpg.set_value("last_text", "Exiting Program ...")
            time.sleep(0.5)
            dpg.destroy_context()
            sys.exit()


def find_key(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None


def closing_code():
    dpg.set_value("last_text", "Exiting Program ...")
    time.sleep(1)
    dpg.destroy_context()
    sys.exit()


def on_button_click():
    
    primary_lang = dpg.get_value("pr_lang")
    targeted_lang = dpg.get_value("tar_lang")
    primary_lang = find_key(gt.LANGUAGES, primary_lang)
    targeted_lang = find_key(gt.LANGUAGES, targeted_lang)
    # print(f"Entered Text: {primary_lang}")
    # print(f"Entered Text: {targeted_lang}")
    while True:
        setting_conversation(primary_lang, targeted_lang, flag=True)
        primary_lang, targeted_lang = targeted_lang, primary_lang
        setting_conversation(primary_lang, targeted_lang, flag=False)
        primary_lang, targeted_lang = targeted_lang, primary_lang


dpg.create_context()


dpg.create_viewport(title='Real Time Live Translator', width=600, height=600)

with dpg.window(tag="Primary Window"):
    with dpg.group() as group1:
        dpg.add_text("Enter Your Speaking Language: ")
        dpg.add_input_text(tag="pr_lang", default_value='english')
        dpg.add_text("Enter Your Targeted Language: ")
        dpg.add_input_text(tag="tar_lang", default_value='hindi')
        dpg.add_button(label='Start', callback=on_button_click)
        
    with dpg.group() as group2:
        dpg.add_text(tag='label1', default_value="Here Will Be Your First Person Conversion")
        dpg.add_input_text(tag="first_person_text", default_value='Nothing Speak', multiline=True, readonly=True)
        dpg.add_text(tag='label2', default_value="Here Will Be Your Second Person Conversion")
        dpg.add_input_text(tag="second_person_text", default_value='Nothing Speak', multiline=True, readonly=True)
        
        dpg.add_button(tag="Exit Program", label="Exit Program", callback=closing_code)
        dpg.add_text(tag='last_text', default_value='')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
