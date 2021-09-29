
from PySimpleGUI.PySimpleGUI import I, Combo, DropDown, MenuBar, VerticalSeparator
from craigslist import CraigslistForSale
import PySimpleGUI as sg
import webbrowser
from os import path
from json import (load as jsonload, dump as jsondump)


SETTINGS_FILE = path.join(path.dirname(
    __file__), r'craigslistings_settings.cfg')

DEFAULT_SETTINGS = {'category': 'zip',
                    'area': 'sfc',
                    'posted_today': True,
                    'bundle_duplicates': True,
                    'sort_by': 'newest',
                    'search_distance': 10,
                    'zip_code': 94117}

SETTINGS = {'category': 'category', 'area': 'area', 'posted_today': 'posted_today', 'bundle_duplicates': 'bundle_duplicates', 'sort_by': 'sort_by',
            'search_distance': 'search_distance', 'zip_code': 'zip_code'}
CATEGORIES = {

    'ata': 'antiques',
    'ppa': 'appliances',
    'ara': 'arts & crafts',
    'sna': 'atvs, utvs, snowmobiles',
    'pta': 'auto parts',
    'wta': 'auto wheels & tires',
    'ava': 'aviation',
    'baa': 'baby & kid stuff',
    'bar': 'barter',
    'bip': 'bicycle parts',
    'bia': 'bicycles',
    'bpa': 'boat parts & accessories',
    'boo': 'boats',
    'bka': 'books & magazines',
    'bfa': 'business',
    'cta': 'cars & trucks',
    'ema': 'cds / dvds / vhs',
    'moa': 'cell phones',
    'cla': 'clothing & accessories',
    'cba': 'collectibles',
    'syp': 'computer parts',
    'sya': 'computers',
    'ela': 'electronics',
    'gra': 'farm & garden',
    'zip': 'free stuff',
    'fua': 'furniture',
    'gms': 'garage & moving sales',
    'foa': 'general for sale',
    'haa': 'health and beauty',
    'hva': 'heavy equipment',
    'hsa': 'household items',
    'jwa': 'jewelry',
    'maa': 'materials',
    'mpa': 'motorcycle parts & accessories',
    'mca': 'motorcycles/scooters',
    'msa': 'musical instruments',
    'pha': 'photo/video',
    'rva': 'recreational vehicles',
    'sga': 'sporting goods',
    'tia': 'tickets',
    'tla': 'tools',
    'taa': 'toys & games',
    'tra': 'trailers',
    'vga': 'video gaming',
    'waa': 'wanted', }

SORTING_OPTIONS = {'Newest': 'newest', 'Price: Low to High': 'price_asc',
                   'Price: High to Low': 'price_desc', }

sort_by_keys = list(SORTING_OPTIONS.keys())
sort_by_values = list(SORTING_OPTIONS.values())

category_values = list(CATEGORIES.values())
category_keys = list(CATEGORIES.keys())


def OpenPage(url):
    webbrowser.open_new(url)


def LoadOptions(settings_file, default_settings):
    global settings
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you',
                               keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        SaveOptions(settings_file, settings, None)
    return settings


def SaveOptions(settings_file, settings, values):
    if values:      # if there are stuff specified by another window, fill in those values
        for key in SETTINGS:  # update window with the values read from settings file
            try:
                settings[key] = values[SETTINGS[key]]

    # if valid category selected
    # get index of category in category_list_values
    # update the settings category key with the category_list_keys at

                if key in ['category', 'sort_by']:
                    selection = settings[key]
                    index = key + '_values' + index(selection)
                    param = key + '_keys' + [index]

                    settings['key'] = param
            except Exception:
                print(
                    f'Problem updating PySimpleGUI window from settings. Key=        {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)


def OptionsPage(settings):
    optionslayout = [[sg.Combo(key='category', default_value=settings['category'], values=category_values,),
                      sg.Text('Area:'), sg.Input(key='area'),
                      sg.Text('Distance:'), sg.Input(key='search_distance'),
                      sg.Text('Zip:'), sg.Input(key='zip_code'),
                      sg.HorizontalSeparator()],
                     [sg.Checkbox('Posted Today?', key='posted_today'),
                      sg.Checkbox('Bundle Duplicates?',
                                  key='bundle_duplicates'),
                      sg.Combo(key='sort_by', default_value=settings['sort_by'], values=sort_by_values)],
                     [sg.Button('Save', key='-save-')]]

    window = sg.Window('Options', optionslayout,
                       keep_on_top=True, finalize=True)

    return window


settings = LoadOptions(SETTINGS_FILE, DEFAULT_SETTINGS)


def cl(settings):
    cl_listings = CraigslistForSale(site='sfbay', area=settings['area'], category=settings['category'], filters={
        'posted_today': settings['posted_today'], 'bundle_duplicates': settings['bundle_duplicates'], 'search_distance': settings['search_distance'], 'zip_code': settings['zip_code'], })
    sg.theme('DarkBlack')
    sg.set_options(border_width=1, margins=(0, 0), element_padding=(1, 3))
    global layout
    layout = [[sg.Text('CraigslistForSale')], [sg.Button('Settings', key='-settings-',), sg.Button(
        'Exit', key='-quit-', tooltip='Closes window')], ]

    listings = cl_listings.get_results(sort_by=settings['sort_by'], limit=25)
    i = 0
    for listing in listings:

        item = listing['name']
        url = listing['url']

        layout.append([sg.Text(item, size=(45, 1), font='Gotham 12', key=f'-item{i}-'.format(
            i), enable_events=True, tooltip=url, border_width=1, auto_size_text=True, justification='center', )])
        i += 1

    window = sg.Window('Craigslister',
                       layout,
                       no_titlebar=True,
                       grab_anywhere=True,
                       keep_on_top=True,
                       alpha_channel=0.8,
                       finalize=True)
    w, h = window.get_screen_dimensions()
    window.move(w - 410, 0)
    window.refresh()

    return window


def Main():
    window, settings = None, LoadOptions(SETTINGS_FILE, DEFAULT_SETTINGS)
    while True:
        if window is None:

            window = cl(settings)
            event, values = window.read()
        print(event, values)

        if event.startswith("-item"):
            url = None  # reset url to empty on each new click
            url = window[event].Tooltip  # url stored in elements tooltip
            OpenPage(url)
            window = None
        elif event in ('Change Settings', '-settings-'):
            event, values = OptionsPage(settings).read(close=True)
            print(event, values)
            if event == '-save-':
                window.close()

                SaveOptions(SETTINGS_FILE, settings, values)
                window = None

        elif event == '-quit-':
            break
    window.close()


Main()
