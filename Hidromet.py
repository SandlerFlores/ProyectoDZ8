from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy_garden.mapview import MapView, MapMarker
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
import requests
from kivymd.theming import ThemableBehavior


KV = '''
# Menu item in the DrawerList list.
<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)

    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color

<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "300dp", "100dp"
            source: "../HidroMet/imagen/senamhi.png"

    MDLabel:
        text: "SENAMHIDZ8"
        font_style: "Button"
        adaptive_height: True

    MDLabel:
        text: "SenamhiDZ8@gmail.com"
        font_style: "Caption"
        adaptive_height: True

    ScrollView:

        DrawerList:
            id: md_list

MDScreen:

    MDNavigationLayout:

        ScreenManager:

            MDScreen:

                MDBoxLayout:
                    orientation: 'vertical'

                    MDTopAppBar:
                        title: "SENAMHI"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]

                    MapView:  # Add this MapView widget
                        id: map_view
                        lat: -5.75  # Initial latitude
                        lon: -75.25  # Initial longitude
                        zoom: 5  # Initial zoom level

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                id: content_drawer
'''

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((1, 1, 1, 1))

class DrawerList(ThemableBehavior,MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class ContentNavigationDrawer(MDBoxLayout):
    pass

class Hidromet(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        icons_item = {
            "map-marker": "Mapa",
            "weather-lightning-rainy": "Estaciones Meteorológicas",
            "hydro-power": "Estaciones Hidrológicas",
            "home-automation": "Estaciones Automáticas",
            "application-outline": "Acerca de ",
            "logout": "Salir",
            # ... (Your existing icons)
        }
        for icon_name, text in icons_item.items():
            item_drawer = ItemDrawer(icon=icon_name, text=text)
            item_drawer.bind(on_release=self.on_menu_item_selected)
            self.root.ids.content_drawer.ids.md_list.add_widget(item_drawer)

        # Fetch data from the API
        api_url = "http://etechgroup-001-site2.dtempurl.com/estacion/listardatos"
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()

            # Add markers based on API response
            for fdata in data['Estacion']:
                if fdata['EstColor'] == "VERDE":
                    marker = MapMarker(lat=fdata['EstLatitud'], lon=fdata['EstLongitud'], source='logo/verde.png')
                elif fdata['EstColor'] == "AMARILLO":
                    marker = MapMarker(lat=fdata['EstLatitud'], lon=fdata['EstLongitud'], source='logo/amarillo.png')
                elif fdata['EstColor'] == "NARANJA":
                    marker = MapMarker(lat=fdata['EstLatitud'], lon=fdata['EstLongitud'], source='logo/naranja.png')
                elif fdata['EstColor'] == "ROJO":
                    marker = MapMarker(lat=fdata['EstLatitud'], lon=fdata['EstLongitud'], source='logo/rojo.png')
                self.root.ids.map_view.add_marker(marker)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from the API: {e}")
        except Exception as e:
            print(f"Error: {e}")
    def on_menu_item_selected(self, instance):
        """Callback function for menu item selection."""
        text = instance.text
        if text == "Mapa":
            # Handle "Mapa" button click
            print("Mapa button clicked")
            # Add your logic here
        elif text == "Estaciones Meteorológicas":
            # Handle "Estaciones Meteorológicas" button click
            print("Estaciones Meteorológicas button clicked")
            # Add your logic here
        # Add similar conditions for other buttons

Hidromet().run()
