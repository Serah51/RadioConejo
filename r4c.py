import os
import sys
import locale
import json
import pickle
import requests
import mutagen
from mutagen import File
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TDRC, APIC
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from datetime import datetime
# VERIFICAR VLC AL INICIO (antes de cualquier import relacionado)
def is_vlc_installed():
    """Verifica si VLC está instalado buscando en las ubicaciones comunes"""
    # Método 1: Buscar en el registro de Windows (solo Windows)
    if sys.platform == "win32":
        try:
            import winreg
            # Buscar en el registro de Windows
            reg_paths = [
                r"SOFTWARE\VideoLAN\VLC",
                r"SOFTWARE\WOW6432Node\VideoLAN\VLC"
            ]
            
            for path in reg_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                    winreg.CloseKey(key)
                    return True
                except:
                    continue
        except:
            pass
    
    # Método 2: Buscar en las rutas comunes de instalación
    common_paths = [
        r"C:\Program Files\VideoLAN\VLC",
        r"C:\Program Files (x86)\VideoLAN\VLC",
        os.path.expandvars(r"%PROGRAMFILES%\VideoLAN\VLC"),
        os.path.expandvars(r"%PROGRAMFILES(X86)%\VideoLAN\VLC")
    ]
    
    for path in common_paths:
        if os.path.exists(path) and os.path.isdir(path):
            return True
    
    return False

# Verificar si VLC está instalado antes de continuar
if not is_vlc_installed():
# Importar PyQt5 solo para mostrar el mensaje de error
    from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QHBoxLayout, QFrame
    from PyQt5.QtCore import Qt, QUrl
    from PyQt5.QtGui import QFont
    from PyQt5.QtGui import QDesktopServices
    import sys

    app = QApplication(sys.argv)

    dialog = QDialog()
    dialog.setWindowTitle("VLC Requerido - Radio Conejo")
    dialog.setModal(True)
    dialog.setMinimumSize(700, 550)

    layout = QVBoxLayout(dialog)

    # Título
    title_label = QLabel("❌ VLC Media Player no encontrado")
    title_label.setFont(QFont("Arial", 18, QFont.Bold))
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setStyleSheet("color: #ff6b6b; padding: 15px;")  # Color rojo más visible
    layout.addWidget(title_label)

    # Mensaje explicativo
    message = QLabel(
        "Radio Conejo requiere VLC Media Player para reproducir audio.\n\n"
        "VLC es un reproductor multimedia gratuito y de código abierto que\n"
        "proporciona las capacidades de reproducción para esta aplicación."
    )
    message.setFont(QFont("Arial", 12))
    message.setWordWrap(True)
    message.setAlignment(Qt.AlignCenter)
    message.setStyleSheet("color: #ffffff;")  # Texto blanco para mejor contraste
    layout.addWidget(message)

    # Línea separadora
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setFrameShadow(QFrame.Sunken)
    separator.setStyleSheet("color: #4b5563;")  # Color más visible para la línea
    layout.addWidget(separator)

    # Instrucciones detalladas
    instructions_label = QLabel("📋 Pasos para instalar VLC:")
    instructions_label.setFont(QFont("Arial", 14, QFont.Bold))
    instructions_label.setStyleSheet("color: #ffffff;")  # Texto blanco
    layout.addWidget(instructions_label)

    instructions = QTextEdit()
    instructions.setReadOnly(True)
    instructions.setHtml("""
    <ol style="color: #e5e7eb;">
        <li><b style="color: #93c5fd;">Visita el sitio oficial de VLC:</b><br>
            <a href="https://www.videolan.org/vlc/" style="color: #60a5fa;">https://www.videolan.org/vlc/</a></li>
        <br>
        <li><b style="color: #93c5fd;">Descarga el instalador:</b><br>
            Haz clic en "Download VLC" (Descargar VLC)</li>
        <br>
        <li><b style="color: #93c5fd;">Ejecuta el instalador:</b><br>
            Abre el archivo descargado (vlc-x.x.x-win64.exe)</li>
        <br>
        <li><b style="color: #93c5fd;">Sigue el asistente de instalación:</b><br>
            Puedes usar la configuración predeterminada recomendada</li>
        <br>
        <li><b style="color: #93c5fd;">Completa la instalación:</b><br>
            Espera a que finalice el proceso de instalación</li>
        <br>
        <li><b style="color: #93c5fd;">Reinicia Radio Conejo:</b><br>
            Después de instalar VLC, cierra y vuelve a abrir Radio Conejo</li>
    </ol>

    <h3 style="color: #93c5fd;">💡 Características de VLC:</h3>
    <ul style="color: #e5e7eb;">
        <li>✅ Totalmente gratuito y de código abierto</li>
        <li>✅ Sin anuncios ni software no deseado</li>
        <li>✅ Reproduce la mayoría de formatos de audio y video</li>
        <li>✅ Disponible en español y muchos otros idiomas</li>
        <li>✅ Compatible con Windows, Mac y Linux</li>
    </ul>

    <h3 style="color: #93c5fd;">🔍 ¿Por qué necesito VLC?</h3>
    <p style="color: #e5e7eb;">Radio Conejo utiliza el motor de reproducción de VLC para garantizar 
    compatibilidad con la mayor cantidad de formatos de audio posibles, 
    incluyendo MP3, FLAC, OGG, WAV y muchos más.</p>
    """)
    instructions.setFont(QFont("Arial", 10))
    instructions.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    instructions.setStyleSheet("""
        QTextEdit {
            background-color: #111827;
            color: #e5e7eb;
            border: 1px solid #374151;
            border-radius: 6px;
            padding: 8px;
        }
    """)
    layout.addWidget(instructions)

    # Botones
    button_layout = QHBoxLayout()

    open_url_btn = QPushButton("🌐 Abrir página de descarga de VLC")
    open_url_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.videolan.org/vlc/")))
    open_url_btn.setFont(QFont("Arial", 11, QFont.Bold))
    open_url_btn.setStyleSheet("""
        QPushButton {
            background-color: #3b82f6; 
            color: white; 
            padding: 12px;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #2563eb;
        }
    """)

    exit_btn = QPushButton("🚪 Salir de Radio Conejo")
    exit_btn.clicked.connect(lambda: sys.exit(0))
    exit_btn.setFont(QFont("Arial", 11))
    exit_btn.setStyleSheet("""
        QPushButton {
            background-color: #ef4444;
            color: white;
            padding: 10px;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #dc2626;
        }
    """)

    button_layout.addWidget(exit_btn)
    button_layout.addStretch()
    button_layout.addWidget(open_url_btn)

    layout.addLayout(button_layout)

    # Aplicar estilo con mejor contraste
    dialog.setStyleSheet("""
        QDialog {
            background-color: #1f2937;
            color: #e5e7eb;
        }
        QLabel {
            color: #e5e7eb;
        }
        QFrame {
            color: #4b5563;
        }
    """)

    dialog.exec_()
    sys.exit(0)

# Si VLC está instalado, continuar con las importaciones normales
import vlc
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QListWidget, QFileDialog,
                             QLabel, QSlider, QMessageBox, QListWidgetItem, 
                             QSplitter, QGroupBox, QAbstractItemView, QTreeWidget,
                             QTreeWidgetItem, QAction, QMenu, QDialog, QDialogButtonBox,
                             QLineEdit, QTextEdit, QTabWidget, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QGridLayout, QSizePolicy, QTextEdit)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QImage, QIcon, QDesktopServices
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*sipPyTypeDict.*")
    

try:
    locale.setlocale(locale.LC_TIME, "es_MX.UTF-8")
except:
    try:
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
    except:
        locale.setlocale(locale.LC_TIME, "C")  # fallback

# Función para obtener la ruta correcta de recursos en desarrollo y empaquetado
def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class CustomMessageBox(QDialog):
    """Diálogo personalizado para mensajes que respeta el tema"""
    
    def __init__(self, parent=None, title="", message="", buttons=QMessageBox.Ok):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Mensaje
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("font-size: 14px;")  # Aumentar tamaño de fuente
        layout.addWidget(message_label)
        
        # Botones
        button_box = QDialogButtonBox()
        
        if buttons & QMessageBox.Ok:
            ok_btn = button_box.addButton(QDialogButtonBox.Ok)
            ok_btn.setText("Aceptar")
        if buttons & QMessageBox.Yes:
            yes_btn = button_box.addButton(QDialogButtonBox.Yes)
            yes_btn.setText("Sí")
        if buttons & QMessageBox.No:
            no_btn = button_box.addButton(QDialogButtonBox.No)
            no_btn.setText("No")
        if buttons & QMessageBox.Cancel:
            cancel_btn = button_box.addButton(QDialogButtonBox.Cancel)
            cancel_btn.setText("Cancelar")
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        
        # Aplicar estilo según el tema del padre
        if parent and hasattr(parent, 'config') and parent.config.get('theme') == 'dark':
            self.setStyleSheet("""
                QDialog {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    font-size: 14px;
                }
                QLabel {
                    color: #ffffff;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #3b82f6, stop: 1 #2563eb);
                    border: none;
                    border-radius: 6px;
                    color: white;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2563eb, stop: 1 #1e40af);
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    font-size: 14px;
                }
                QLabel {
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton {
                    font-size: 14px;
                }
            """)


class MetadataWorker(QThread):
    """Hilo para extraer metadatos sin bloquear la interfaz"""
    metadata_ready = pyqtSignal(dict)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        """Ejecuta la extracción de metadatos en un hilo separado"""
        try:
            metadata = self.extract_metadata(self.file_path)
            self.metadata_ready.emit(metadata)
        except Exception as e:
            print(f"Error extrayendo metadatos: {e}")
            self.metadata_ready.emit({})
    
    def extract_metadata(self, file_path):
        """Extrae metadatos de un archivo de audio"""
        metadata = {
            'title': '',
            'artist': '',
            'album': '',
            'genre': '',
            'year': '',
            'duration': '',
            'bitrate': '',
            'sample_rate': '',
            'channels': '',
            'cover_art': None,
            'length': 0  # Duración en segundos para cálculos precisos
        }
            # Mejorar la extracción de carátula
        try:
            if file_path.lower().endswith('.mp3'):
                audio = ID3(file_path)
                for tag in audio.values():
                    if isinstance(tag, APIC):
                        metadata['cover_art'] = tag.data
                        break
            elif file_path.lower().endswith('.flac'):
                audio = FLAC(file_path)
                if audio.pictures:
                    metadata['cover_art'] = audio.pictures[0].data
            elif file_path.lower().endswith(('.ogg', '.oga')):
                audio = OggVorbis(file_path)
                if 'metadata_block_picture' in audio.tags:
                    import base64
                    metadata['cover_art'] = base64.b64decode(audio.tags['metadata_block_picture'][0])
            elif file_path.lower().endswith(('.m4a', '.mp4')):
                # Para formatos MP4/M4A (no implementado en tu código original)
                try:
                    from mutagen.mp4 import MP4
                    audio = MP4(file_path)
                    if 'covr' in audio:
                        metadata['cover_art'] = audio['covr'][0]
                except:
                    pass
        except Exception as e:
            print(f"Error extrayendo portada: {e}")
        
        try:
            audio = File(file_path, easy=True)
            
            if audio is not None:
                # Información básica
                metadata['title'] = audio.get('title', [''])[0] if audio.get('title') else os.path.splitext(os.path.basename(file_path))[0]
                metadata['artist'] = audio.get('artist', ['Desconocido'])[0]
                metadata['album'] = audio.get('album', ['Desconocido'])[0]
                metadata['genre'] = audio.get('genre', ['Desconocido'])[0]
                metadata['year'] = audio.get('date', [''])[0] if audio.get('date') else ''
                
                # Información técnica
                if hasattr(audio.info, 'length'):
                    metadata['length'] = audio.info.length
                    minutes = int(audio.info.length // 60)
                    seconds = int(audio.info.length % 60)
                    metadata['duration'] = f"{minutes}:{seconds:02d}"
                
                if hasattr(audio.info, 'bitrate'):
                    metadata['bitrate'] = f"{audio.info.bitrate // 1000} kbps" if audio.info.bitrate > 0 else "Desconocido"
                
                if hasattr(audio.info, 'sample_rate'):
                    metadata['sample_rate'] = f"{audio.info.sample_rate // 1000} kHz"
                
                if hasattr(audio.info, 'channels'):
                    metadata['channels'] = str(audio.info.channels)
                
                # Extraer carátula (cover art)
                if hasattr(audio, 'tags'):
                    if 'APIC:' in audio.tags or 'covr' in audio.tags:
                        # Para MP3
                        if file_path.lower().endswith('.mp3'):
                            try:
                                audio_id3 = ID3(file_path)
                                for tag in audio_id3.values():
                                    if isinstance(tag, APIC):
                                        metadata['cover_art'] = tag.data
                                        break
                            except:
                                pass
                        # Para FLAC
                        elif file_path.lower().endswith('.flac'):
                            try:
                                flac = FLAC(file_path)
                                if flac.pictures:
                                    metadata['cover_art'] = flac.pictures[0].data
                            except:
                                pass
                        # Para OGG
                        elif file_path.lower().endswith('.ogg'):
                            try:
                                ogg = OggVorbis(file_path)
                                if 'metadata_block_picture' in ogg.tags:
                                    metadata['cover_art'] = ogg.tags['metadata_block_picture'][0]
                            except:
                                pass
            
            # Si no se pudo extraer el título de los metadatos, usar el nombre del archivo
            if not metadata['title']:
                metadata['title'] = os.path.splitext(os.path.basename(file_path))[0]
                
        except Exception as e:
            print(f"Error procesando metadatos: {e}")
            # Si falla la extracción, al menos usar el nombre del archivo
            metadata['title'] = os.path.splitext(os.path.basename(file_path))[0]
        
        return metadata


class WeatherWorker(QThread):
    """Hilo para obtener datos del clima sin bloquear la interfaz"""
    weather_ready = pyqtSignal(dict)
    
    def __init__(self, weather_manager):
        super().__init__()
        self.weather_manager = weather_manager
    
    def run(self):
        """Ejecuta la obtención del clima en un hilo separado"""
        try:
            weather_data = self.weather_manager.get_weather()
            if weather_data is not None:
                self.weather_ready.emit(weather_data)
            else:
                # Emitir un diccionario vacío para indicar que no hay datos
                self.weather_ready.emit({})
        except Exception as e:
            print(f"Error en el hilo del clima: {e}")
            # Emitir un diccionario vacío en caso de error
            self.weather_ready.emit({})


class ConfigManager:
    """Maneja la configuración de la aplicación"""
    
    def __init__(self, config_file="radio_conejo_config.pkl", folders_file="radio_conejo_folders.pkl"):
        self.config_file = config_file
        self.folders_file = folders_file
    
    def load_config(self):
        """Carga la configuración desde archivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'rb') as f:
                    return pickle.load(f)
            return {'volume': 80, 'theme': 'light'}
        except Exception:
            return {'volume': 80, 'theme': 'light'}
    
    def save_config(self, config):
        """Guarda la configuración en archivo"""
        try:
            with open(self.config_file, 'wb') as f:
                pickle.dump(config, f)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def load_folders(self):
        """Carga las carpetas desde archivo"""
        try:
            if os.path.exists(self.folders_file):
                with open(self.folders_file, 'rb') as f:
                    folders = pickle.load(f)
                    # Asegurarse de que siempre devolvemos una lista
                    return folders if isinstance(folders, list) else []
            return []
        except Exception:
            return []
    
    def save_folders(self, folders):
        """Guarda las carpetas en archivo"""
        try:
            with open(self.folders_file, 'wb') as f:
                pickle.dump(folders, f)
        except Exception as e:
            print(f"Error guardando carpetas: {e}")


class WeatherManager:
    """Maneja las operaciones relacionadas con el clima"""
    
    def __init__(self, api_key, city_id="3515001"):
        self.api_key = api_key
        self.city_id = city_id
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.last_update = None
        self.weather_data = None
    
    def get_weather(self):
        """Obtiene los datos del clima desde la API"""
        try:
            # Verificar si ya tenemos datos recientes (menos de 10 minutos)
            if (self.weather_data and self.last_update and 
                (datetime.now() - self.last_update).total_seconds() < 600):
                return self.weather_data
            
            params = {
                'id': self.city_id,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'es'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            self.weather_data = response.json()
            self.last_update = datetime.now()
            return self.weather_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo datos del clima: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado al obtener clima: {e}")
            return None
    
    def get_weather_icon(self, icon_code):
        """Devuelve un emoji basado en el código de icono del clima"""
        icon_map = {
            '01d': '☀️',  # clear sky day
            '01n': '🌙',  # clear sky night
            '02d': '⛅',  # few clouds day
            '02n': '☁️',  # few clouds night
            '03d': '☁️',  # scattered clouds
            '03n': '☁️',  # scattered clouds
            '04d': '☁️',  # broken clouds
            '04n': '☁️',  # broken clouds
            '09d': '🌧️',  # shower rain
            '09n': '🌧️',  # shower rain
            '10d': '🌦️',  # rain day
            '10n': '🌧️',  # rain night
            '11d': '⛈️',  # thunderstorm
            '11n': '⛈️',  # thunderstorm
            '13d': '❄️',  # snow
            '13n': '❄️',  # snow
            '50d': '🌫️',  # mist
            '50n': '🌫️'   # mist
        }
        return icon_map.get(icon_code, '🌡️')
    
    def format_weather_info(self, weather_data):
        """Formatea la información del clima para mostrar"""
        if not weather_data:
            return "Clima: No disponible"
        
        try:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description'].capitalize()
            icon_code = weather_data['weather'][0]['icon']
            icon = self.get_weather_icon(icon_code)
            
            return f"{icon} {description}, {temp}°C (Sensación: {feels_like}°C) 💧{humidity}%"
        except KeyError as e:
            print(f"Error formateando datos del clima: {e}")
            return "Clima: Datos incompletos"


class PlaylistManager:
    """Maneja las operaciones de la playlist"""
    
    def __init__(self, playlist_widget, config_manager):
        self.playlist = []
        self.current_index = -1
        self.playlist_widget = playlist_widget
        self.config_manager = config_manager
        self.song_metadata = {}  # Diccionario para almacenar metadatos por ruta de archivo
    
    def add_song(self, song_path, song_name, metadata=None):
        """Añade una canción a la playlist"""
        if song_path not in self.playlist:
            self.playlist.append(song_path)
            
            # Guardar metadatos si se proporcionan
            if metadata:
                self.song_metadata[song_path] = metadata
                # Usar el título de los metadatos si está disponible
                display_name = metadata.get('title', song_name)
            else:
                display_name = song_name
                
            playlist_item = QListWidgetItem(f"📀 {display_name}")
            playlist_item.setData(Qt.UserRole, song_path)
            self.playlist_widget.addItem(playlist_item)
            return True
        return False
    
    def add_songs(self, songs):
        """Añade múltiples canciones to the playlist"""
        added_count = 0
        for song_path, song_name in songs:
            if self.add_song(song_path, song_name):
                added_count += 1
        return added_count
    
    def remove_song(self, index):
        """Elimina una canción de la playlist"""
        if 0 <= index < len(self.playlist):
            song_path = self.playlist.pop(index)
            if song_path in self.song_metadata:
                del self.song_metadata[song_path]
            self.playlist_widget.takeItem(index)
            return song_path
        return None
    
    def clear(self):
        """Limpia la playlist completa"""
        self.playlist.clear()
        self.song_metadata.clear()
        self.playlist_widget.clear()
        self.current_index = -1
    
    def get_metadata(self, song_path):
        """Obtiene los metadatos de una canción"""
        return self.song_metadata.get(song_path, {})
    
    def update_metadata(self, song_path, metadata):
        """Actualiza los metadatos de una canción"""
        self.song_metadata[song_path] = metadata
        
        # Actualizar el nombre en la playlist si es necesario
        for i in range(self.playlist_widget.count()):
            item = self.playlist_widget.item(i)
            if item.data(Qt.UserRole) == song_path:
                display_name = metadata.get('title', os.path.splitext(os.path.basename(song_path))[0])
                item.setText(f"📀 {display_name}")
                break
    
    def calculate_total_duration(self):
        """Calcula la duración total de la playlist en segundos"""
        total_seconds = 0
        for song_path in self.playlist:
            metadata = self.song_metadata.get(song_path, {})
            if 'length' in metadata:
                total_seconds += metadata['length']
        return total_seconds
    
    def format_duration(self, total_seconds):
        """Formatea la duración total en formato legible"""
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def export_to_file(self, file_path):
        """Exporta la playlist a un archivo JSON"""
        try:
            playlist_data = {
                'songs': self.playlist, 
                'export_date': datetime.now().isoformat(), 
                'total_songs': len(self.playlist),
                'metadata': self.song_metadata
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(playlist_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            raise Exception(f"No se pudo exportar la playlist: {str(e)}")
    
    def import_from_file(self, file_path):
        """Importa una playlist desde un archivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                playlist_data = json.load(f)
            
            if 'songs' not in playlist_data:
                raise Exception("El archivo no contiene una playlist válida.")
            
            # Devolver tanto las canciones como los metadatos si existen
            songs = playlist_data['songs']
            metadata = playlist_data.get('metadata', {})
            
            return songs, metadata
        except Exception as e:
            raise Exception(f"No se pudo importar la playlist: {str(e)}")


class MetadataDialog(QDialog):
    """Diálogo para mostrar metadatos de la canción"""
    
    def __init__(self, parent=None, metadata=None):
        super().__init__(parent)
        self.setWindowTitle("Metadatos de la Canción")
        self.setModal(True)
        self.setGeometry(100, 100, 600, 500)
        
        layout = QVBoxLayout(self)
        
        # Pestañas para organizar la información
        tab_widget = QTabWidget()
        
        # Pestaña de información básica
        basic_info_tab = QWidget()
        basic_layout = QVBoxLayout(basic_info_tab)
        
        # Carátula
        self.cover_art_label = QLabel()
        self.cover_art_label.setAlignment(Qt.AlignCenter)
        self.cover_art_label.setFixedSize(200, 200)
        self.cover_art_label.setStyleSheet("border: 2px solid #3b82f6; border-radius: 8px;")
        basic_layout.addWidget(self.cover_art_label)
        
        # Tabla de metadatos
        self.metadata_table = QTableWidget()
        self.metadata_table.setColumnCount(2)
        self.metadata_table.setHorizontalHeaderLabels(["Propiedad", "Valor"])
        self.metadata_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.metadata_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        basic_layout.addWidget(self.metadata_table)
        
        tab_widget.addTab(basic_info_tab, "Información Básica")
        
        # Pestaña de información técnica
        tech_info_tab = QWidget()
        tech_layout = QVBoxLayout(tech_info_tab)
        
        self.tech_table = QTableWidget()
        self.tech_table.setColumnCount(2)
        self.tech_table.setHorizontalHeaderLabels(["Propiedad Técnica", "Valor"])
        self.tech_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tech_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tech_layout.addWidget(self.tech_table)
        
        tab_widget.addTab(tech_info_tab, "Información Técnica")
        
        layout.addWidget(tab_widget)
        
        # Botones
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        # Cargar datos si se proporcionan
        if metadata:
            self.load_metadata(metadata)
        
        if parent and hasattr(parent, 'config') and parent.config.get('theme') == 'dark':
            self.setStyleSheet("""
                QDialog {
                    background-color: #1f2937;
                    color: #e5e7eb;
                    font-size: 14px;
                }
                QTableWidget {
                    background-color: #111827;
                    color: #e5e7eb;
                    gridline-color: #374151;
                    border: 1px solid #374151;
                    border-radius: 6px;
                    font-size: 14px;
                }
                QHeaderView::section {
                    background-color: #3b82f6;
                    color: white;
                    padding: 6px;
                    border: none;
                    font-weight: bold;
                    font-size: 14px;
                }
                QTabWidget::pane {
                    border: 1px solid #3b82f6;
                    border-radius: 6px;
                    background-color: #2d2d2d;
                }
                QTabBar::tab {
                    background: #353535;
                    color: #ffffff;
                    padding: 8px 12px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    font-size: 14px;
                }
                QTabBar::tab:selected {
                    background: #3b82f6;
                    color: white;
                    font-size: 14px;
                }
                QLabel {
                    color: #ffffff;
                    font-size: 14px;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    font-size: 14px;
                }
                QTableWidget {
                    background-color: #ffffff;
                    color: #111827;
                    gridline-color: #d1d5db;
                    border: 1px solid #d1d5db;
                    border-radius: 6px;
                    font-size: 14px;
                }
                QHeaderView::section {
                    background-color: #3b82f6;
                    color: white;
                    padding: 6px;
                    border: none;
                    font-weight: bold;
                    font-size: 14px;
                }
                QTabWidget::pane {
                    border: 1px solid #3b82f6;
                    border-radius: 6px;
                    background-color: #ffffff;
                }
                QTabBar::tab {
                    background: #f0f0f0;
                    color: #000000;
                    padding: 8px 12px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    font-size: 14px;
                }
                QTabBar::tab:selected {
                    background: #3b82f6;
                    color: white;
                    font-size: 14px;
                }
                QLabel {
                    font-size: 14px;
                }
            """)
    
    def load_metadata(self, metadata):
        """Carga los metadatos en la interfaz"""
        # Configurar carátula
        cover_art = metadata.get('cover_art')
        if cover_art:
            pixmap = QPixmap()
            pixmap.loadFromData(cover_art)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.cover_art_label.setPixmap(scaled_pixmap)
            else:
                self.cover_art_label.setText("🎵 Sin carátula")
        else:
            self.cover_art_label.setText("🎵 Sin carátula")
        
        # Configurar tabla de metadatos básicos
        basic_data = [
            ("Título", metadata.get('title', 'Desconocido')),
            ("Artista", metadata.get('artist', 'Desconocido')),
            ("Álbum", metadata.get('album', 'Desconocido')),
            ("Género", metadata.get('genre', 'Desconocido')),
            ("Año", metadata.get('year', 'Desconocido'))
        ]
        
        self.metadata_table.setRowCount(len(basic_data))
        for row, (key, value) in enumerate(basic_data):
            self.metadata_table.setItem(row, 0, QTableWidgetItem(key))
            self.metadata_table.setItem(row, 1, QTableWidgetItem(str(value)))
        
        # Configurar tabla de información técnica
        tech_data = [
            ("Duración", metadata.get('duration', 'Desconocido')),
            ("Bitrate", metadata.get('bitrate', 'Desconocido')),
            ("Sample Rate", metadata.get('sample_rate', 'Desconocido')),
            ("Canales", metadata.get('channels', 'Desconocido')),
            ("Formato", metadata.get('format', 'Desconocido'))
        ]
        
        self.tech_table.setRowCount(len(tech_data))
        for row, (key, value) in enumerate(tech_data):
            self.tech_table.setItem(row, 0, QTableWidgetItem(key))
            self.tech_table.setItem(row, 1, QTableWidgetItem(str(value)))


class MusicPlayer(QMainWindow):
    """Ventana principal del reproductor de música"""

    def __init__(self):
        super().__init__()

        try:
            # Lista de posibles rutas para el icono (usando resource_path)
            icon_paths = [
                resource_path("radio_conejo.ico"),  # Primera prioridad: recurso empaquetado
                "radio_conejo.ico",                 # Segunda prioridad: archivo local
                resource_path("icon.ico"),
                "icon.ico",
                resource_path("resources/radio_conejo.ico"),
                "resources/radio_conejo.ico",
                resource_path("resources/icon.ico"),
                "resources/icon.ico",
                resource_path("images/radio_conejo.png"),
                "images/radio_conejo.png",
                resource_path("images/icon.png"),
                "images/icon.png"
            ]
            
            icon_loaded = False
            for path in icon_paths:
                if os.path.exists(path):
                    self.setWindowIcon(QIcon(path))
                    icon_loaded = True
                    print(f"Icono cargado desde: {path}")
                    break
            
            if not icon_loaded:
                # Crear icono programáticamente como fallback
                from PyQt5.QtGui import QPainter
                pixmap = QPixmap(64, 64)
                pixmap.fill(Qt.transparent)
                
                painter = QPainter(pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                
                # Dibujar un círculo de fondo
                painter.setBrush(QColor(59, 130, 246))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(0, 0, 64, 64)
                
                # Dibujar texto con emojis (conejo y nota musical)
                font = QFont("Segoe UI Emoji", 24)
                painter.setFont(font)
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(0, 0, 64, 64, Qt.AlignCenter, "🐰🎵")
                
                painter.end()
                
                self.setWindowIcon(QIcon(pixmap))
                print("Icono creado programáticamente")
                
        except Exception as e:
            print(f"Error al cargar el icono: {e}")
            # Crear un icono mínimo como fallback
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(59, 130, 246))
            self.setWindowIcon(QIcon(pixmap))
                
        except Exception as e:
            print(f"Error al cargar el icono: {e}")
            # Crear un icono mínimo como fallback
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(59, 130, 246))
            self.setWindowIcon(QIcon(pixmap))
        
        # Icono para la barra de tareas (Windows)
        if sys.platform == "win32":
            try:
                import ctypes
                myappid = 'radioconejo.app.1.0'  # Identificador único arbitrario
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except Exception as e:
                print(f"No se pudo establecer el ID de aplicación: {e}")
        
        self.setWindowTitle("Radio Conejo")
        self.setGeometry(100, 100, 1600, 900)
        
        # Inicializar managers
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.folders = self.config_manager.load_folders()
        
        # Inicializar weather manager
        self.weather_manager = WeatherManager("aqui debe ir tu ID de WeatherManager", "#######")
        self.weather_worker = None
        
        # Inicializar VLC
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.is_playing = False
        self.current_media = None
        
        # Almacenar todas las canciones para el filtrado
        self.all_songs = []
        
        # Worker para metadatos
        self.metadata_worker = None
        
        # Inicializar UI
        self.setup_styles()
        self.setup_ui()
        
        # Configurar timers
        self.setup_timers()
        
        # Cargar estado inicial
        self.update_clock()
        self.player.audio_set_volume(self.config.get('volume', 80))
        self.update_counts()
        
        # Aplicar tema inicial
        self.apply_theme(self.config.get('theme', 'light'))
        
        # Mostrar mensaje inicial de clima
        self.weather_label.setText("🌤️ Cargando datos climáticos...")
    
    def show_message(self, title, message, buttons=QMessageBox.Ok):
        """Muestra un mensaje personalizado que respeta el tema actual"""
        dialog = CustomMessageBox(self, title, message, buttons)
        return dialog.exec_()
    
    def show_question(self, title, message):
        """Muestra una pregunta con botones Sí/No en español"""
        dialog = CustomMessageBox(self, title, message, QMessageBox.Yes | QMessageBox.No)
        
        # Traducir los botones al español
        for button in dialog.findChildren(QPushButton):
            if button.text() == "&Yes":
                button.setText("Sí")
            elif button.text() == "&No":
                button.setText("No")
        
        result = dialog.exec_()
        return result == QDialog.Accepted
    
    def show_info(self, title, message):
        """Muestra un mensaje informativo"""
        return self.show_message(title, message, QMessageBox.Ok)
    
    def show_warning(self, title, message):
        """Muestra un mensaje de advertencia"""
        return self.show_message(title, message, QMessageBox.Ok)
    
    def show_error(self, title, message):
        """Muestra un mensaje de error"""
        return self.show_message(title, message, QMessageBox.Ok)
    
    def show_metadata(self, metadata):
        """Muestra los metadatos de la canción en un diálogo"""
        dialog = MetadataDialog(self, metadata)
        dialog.exec_()

    def setup_styles(self):
        """Configura los estilos base de la interfaz"""
        # Los estilos se aplicarán dinámicamente según el tema
        pass
    
    def setup_timers(self):
        """Configura los timers de la aplicación"""
        # Timer para actualizar el progreso de reproducción
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(1000)
        
        # Timer para actualizar el reloj
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        
        # Cargar clima después de un breve delay para no bloquear la interfaz
        QTimer.singleShot(1000, self.update_weather_async)
        
        # Timer para actualizar el clima (cada 10 minutos)
        self.weather_timer = QTimer(self)
        self.weather_timer.timeout.connect(self.update_weather_async)
        self.weather_timer.start(600000)  # 10 minutos
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(15, 10, 15, 10)
        
        # Configurar barra de menú
        self.setup_menu_bar()
        
        # Header con título y reloj
        self.setup_header(main_layout)
        
        # Área principal con splitter
        self.setup_main_area(main_layout)
        
        # Área de información y controles
        self.setup_info_area(main_layout)
        self.setup_controls_area(main_layout)
        
        # Inicializar playlist manager después de crear la UI
        self.playlist_manager = PlaylistManager(self.playlist_list, self.config_manager)
        
        # Actualizar lista de carpetas
        self.update_folders_tree()
    
    def setup_menu_bar(self):
        """Configura la barra de menú"""
        menubar = self.menuBar()
        
        # Menú de tema
        theme_menu = menubar.addMenu('🎨 Tema')
        
        light_theme_action = QAction('🌞 Tema Claro', self)
        light_theme_action.triggered.connect(lambda: self.apply_theme('light'))
        theme_menu.addAction(light_theme_action)
        
        dark_theme_action = QAction('🌙 Tema Oscuro', self)
        dark_theme_action.triggered.connect(lambda: self.apply_theme('dark'))
        theme_menu.addAction(dark_theme_action)
        
        # Menú de clima
        weather_menu = menubar.addMenu('🌤️ Clima')
        
        refresh_weather_action = QAction('🔄 Actualizar Clima', self)
        refresh_weather_action.triggered.connect(self.update_weather_async)
        weather_menu.addAction(refresh_weather_action)
        
        # Menú de metadatos
        metadata_menu = menubar.addMenu('📝 Metadatos')
        
        view_metadata_action = QAction('👁️ Ver Metadatos', self)
        view_metadata_action.triggered.connect(self.view_current_metadata)
        metadata_menu.addAction(view_metadata_action)
        
        extract_all_metadata_action = QAction('⚡ Extraer Todos los Metadatos', self)
        extract_all_metadata_action.triggered.connect(self.extract_all_metadata)
        metadata_menu.addAction(extract_all_metadata_action)
    
    def setup_header(self, main_layout):
        """Configura el encabezado con título y reloj"""
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        # Título de la aplicación
        title_layout = QHBoxLayout()
        radio_label = QLabel("📻 Radio Conejo 🐰")
        radio_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_layout.addWidget(radio_label)
        title_layout.addStretch()
        header_layout.addLayout(title_layout)
        
        # Fecha, hora y clima
        info_layout = QHBoxLayout()
        
        # Fecha y hora a la izquierda
        date_time_layout = QHBoxLayout()
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignLeft)
        self.date_label.setFont(QFont("Arial", 14, QFont.Bold))
        
        date_time_layout.addWidget(self.date_label)

        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignCenter)
        self.clock_label.setFont(QFont("Arial", 14, QFont.Bold))
        
        # Clima a la derecha
        self.weather_label = QLabel()
        self.weather_label.setAlignment(Qt.AlignRight)
        self.weather_label.setFont(QFont("Arial", 14))
        
        info_layout.addLayout(date_time_layout, 1)  # 1 parte de espacio
        info_layout.addWidget(self.clock_label, 1)  # 1 parte de espacio
        info_layout.addWidget(self.weather_label, 1)  # 1 parte de espacio
        
        header_layout.addLayout(info_layout)
        
        main_layout.addLayout(header_layout)
    
    def setup_main_area(self, main_layout):
        """Configura el área principal con carpetas, canciones y playlist"""
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)
        main_layout.addWidget(splitter, 7)
        
        # Panel de carpetas
        folders_group = self.create_folders_group()
        splitter.addWidget(folders_group)
        
        # Panel de canciones
        songs_group = self.create_songs_group()
        splitter.addWidget(songs_group)
        
        # Panel de playlist
        playlist_group = self.create_playlist_group()
        splitter.addWidget(playlist_group)
        
        splitter.setSizes([300, 400, 500])
    
    def create_folders_group(self):
        """Crea el grupo de carpetas"""
        folders_group = QGroupBox("📁 CARPETAS")
        folders_group.setFont(QFont("Arial", 11, QFont.Bold))
        folders_layout = QVBoxLayout(folders_group)
        folders_layout.setSpacing(6)
        folders_layout.setContentsMargins(8, 15, 8, 8)
        
        self.folders_tree = QTreeWidget()
        self.folders_tree.setHeaderLabel("Estructura de carpetas")
        self.folders_tree.itemClicked.connect(self.on_folder_selected)
        self.folders_tree.setFont(QFont("Arial", 11))
        self.folders_tree.setAlternatingRowColors(True)
        folders_layout.addWidget(self.folders_tree)
        
        folder_buttons_layout = QHBoxLayout()
        folder_buttons_layout.setSpacing(4)
        
        add_folder_btn = QPushButton("➕ AGREGAR")
        add_folder_btn.clicked.connect(self.add_folder)
        add_folder_btn.setFont(QFont("Arial", 10))
        folder_buttons_layout.addWidget(add_folder_btn)
        
        remove_folder_btn = QPushButton("🗑️ ELIMINAR")
        remove_folder_btn.clicked.connect(self.remove_folder)
        remove_folder_btn.setFont(QFont("Arial", 10))
        folder_buttons_layout.addWidget(remove_folder_btn)
        
        refresh_btn = QPushButton("🔄 ACTUALIZAR")
        refresh_btn.clicked.connect(self.refresh_folders)
        refresh_btn.setFont(QFont("Arial", 10))
        folder_buttons_layout.addWidget(refresh_btn)
        
        folders_layout.addLayout(folder_buttons_layout)
        
        return folders_group
    
    def create_songs_group(self):
        """Crea el grupo de canciones"""
        songs_group = QGroupBox("📀 CANCIONES")
        songs_group.setFont(QFont("Arial", 11, QFont.Bold))
        songs_layout = QVBoxLayout(songs_group)
        songs_layout.setSpacing(6)
        songs_layout.setContentsMargins(8, 15, 8, 8)
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        search_layout.setSpacing(4)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar canciones...")
        self.search_input.textChanged.connect(self.filter_songs)
        self.search_input.setFont(QFont("Arial", 11))
        search_layout.addWidget(self.search_input)
        
        songs_layout.addLayout(search_layout)
        
        # Lista de canciones
        self.songs_list = QListWidget()
        self.songs_list.itemDoubleClicked.connect(self.add_to_playlist)
        self.songs_list.setFont(QFont("Arial", 11))
        self.songs_list.setAlternatingRowColors(True)
        self.songs_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        songs_layout.addWidget(self.songs_list)
        
        song_buttons_layout = QHBoxLayout()
        song_buttons_layout.setSpacing(4)
        
        add_selected_btn = QPushButton("➕ AGREGAR SELECCIONADAS")
        add_selected_btn.clicked.connect(self.add_selected_to_playlist)
        add_selected_btn.setFont(QFont("Arial", 10))
        song_buttons_layout.addWidget(add_selected_btn)
        
        add_all_btn = QPushButton("📀 AGREGAR TODAS")
        add_all_btn.clicked.connect(self.add_all_to_playlist)
        add_all_btn.setFont(QFont("Arial", 10))
        song_buttons_layout.addWidget(add_all_btn)
        
        songs_layout.addLayout(song_buttons_layout)
        
        return songs_group
    
# En la función create_playlist_group, reemplazar el código actual con este:

    def create_playlist_group(self):
        """Crea el grupo de playlist con mejor organización visual"""
        playlist_group = QGroupBox("🎵 PLAYLIST")
        playlist_group.setFont(QFont("Arial", 11, QFont.Bold))
        playlist_layout = QVBoxLayout(playlist_group)
        playlist_layout.setSpacing(8)
        playlist_layout.setContentsMargins(8, 15, 8, 8)
        
        # --- SECCIÓN: INFORMACIÓN DE LA PLAYLIST ---
        info_group = QGroupBox("📊 INFORMACIÓN")
        info_group.setFont(QFont("Arial", 10))
        info_layout = QVBoxLayout(info_group)
        info_layout.setContentsMargins(8, 12, 8, 8)
        
        info_content_layout = QHBoxLayout()
        info_content_layout.setSpacing(10)
        
        self.playlist_count_label = QLabel("Total: 0 canciones")
        self.playlist_count_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.playlist_duration_label = QLabel("Duración: 0:00")
        self.playlist_duration_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        info_content_layout.addWidget(self.playlist_count_label)
        info_content_layout.addWidget(self.playlist_duration_label)
        info_content_layout.addStretch()
        
        info_layout.addLayout(info_content_layout)
        playlist_layout.addWidget(info_group)
        
        # --- SECCIÓN: LISTA DE CANCIONES ---
        songs_group = QGroupBox("📋 CANCIONES EN LA LISTA")
        songs_group.setFont(QFont("Arial", 10))
        songs_layout = QVBoxLayout(songs_group)
        songs_layout.setContentsMargins(0, 12, 0, 8)
        
        self.playlist_list = QListWidget()
        self.playlist_list.itemDoubleClicked.connect(self.play_selected)
        self.playlist_list.setFont(QFont("Arial", 11))
        self.playlist_list.setAlternatingRowColors(True)
        self.playlist_list.setSelectionMode(QAbstractItemView.SingleSelection)
        songs_layout.addWidget(self.playlist_list)
        
        playlist_layout.addWidget(songs_group, 5)  # Mayor espacio para la lista
        
        # --- SECCIÓN: GESTIÓN DE CANCIONES ---
        management_group = QGroupBox("⚙️ GESTIÓN DE CANCIONES")
        management_group.setFont(QFont("Arial", 10))
        management_layout = QVBoxLayout(management_group)
        management_layout.setContentsMargins(8, 12, 8, 8)
        
        # Botones de gestión
        song_buttons_layout = QHBoxLayout()
        song_buttons_layout.setSpacing(4)
        
        remove_btn = QPushButton("🗑️ ELIMINAR")
        remove_btn.clicked.connect(self.remove_from_playlist)
        remove_btn.setFont(QFont("Arial", 9))
        remove_btn.setToolTip("Eliminar la canción seleccionada")
        song_buttons_layout.addWidget(remove_btn)
        
        clear_btn = QPushButton("🧹 LIMPIAR TODO")
        clear_btn.clicked.connect(self.clear_playlist)
        clear_btn.setFont(QFont("Arial", 9))
        clear_btn.setToolTip("Vaciar toda la playlist")
        song_buttons_layout.addWidget(clear_btn)
        
        move_up_btn = QPushButton("⬆️ SUBIR")
        move_up_btn.clicked.connect(self.move_up_in_playlist)
        move_up_btn.setFont(QFont("Arial", 9))
        move_up_btn.setToolTip("Mover canción hacia arriba")
        song_buttons_layout.addWidget(move_up_btn)
        
        move_down_btn = QPushButton("⬇️ BAJAR")
        move_down_btn.clicked.connect(self.move_down_in_playlist)
        move_down_btn.setFont(QFont("Arial", 9))
        move_down_btn.setToolTip("Mover canción hacia abajo")
        song_buttons_layout.addWidget(move_down_btn)
        
        management_layout.addLayout(song_buttons_layout)
        playlist_layout.addWidget(management_group)
        
        # --- SECCIÓN: IMPORTAR/EXPORTAR ---
        io_group = QGroupBox("💾 GESTIÓN DE PLAYLIST")
        io_group.setFont(QFont("Arial", 10))
        io_layout = QVBoxLayout(io_group)
        io_layout.setContentsMargins(8, 12, 8, 8)
        
        io_buttons_layout = QHBoxLayout()
        io_buttons_layout.setSpacing(4)
        
        export_btn = QPushButton("💾 EXPORTAR")
        export_btn.clicked.connect(self.export_playlist)
        export_btn.setFont(QFont("Arial", 9))
        export_btn.setToolTip("Guardar playlist en un archivo")
        io_buttons_layout.addWidget(export_btn)
        
        import_btn = QPushButton("📂 IMPORTAR")
        import_btn.clicked.connect(self.import_playlist)
        import_btn.setFont(QFont("Arial", 9))
        import_btn.setToolTip("Cargar playlist desde un archivo")
        io_buttons_layout.addWidget(import_btn)
        
        io_layout.addLayout(io_buttons_layout)
        playlist_layout.addWidget(io_group)
        
        return playlist_group
    


    def setup_info_area(self, main_layout):
        info_group = QGroupBox("🎵 REPRODUCIENDO")
        info_group.setFont(QFont("Arial", 11, QFont.Bold))
        info_layout = QHBoxLayout(info_group)
        info_layout.setSpacing(12)
        info_layout.setContentsMargins(10, 10, 10, 10)

        # --- Información (izquierda) ---
        info_right = QWidget()
        info_right_layout = QVBoxLayout(info_right)
        info_right_layout.setContentsMargins(0, 0, 0, 0)
        info_right_layout.setSpacing(8)

        song_info_layout = QGridLayout()
        song_info_layout.setColumnStretch(1, 1)
        song_info_layout.setContentsMargins(0, 0, 0, 0)
        song_info_layout.setHorizontalSpacing(10)
        song_info_layout.setVerticalSpacing(6)

        label_font = QFont("Arial", 12, QFont.Bold)
        value_font = QFont("Arial", 12)

        # Título
        title_label = QLabel("🎵 Título:")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.title_value = QLabel("Selecciona una canción")
        self.title_value.setFont(QFont("Arial", 14, QFont.Bold))
        # 👇 solo este usa un color fijo (acento), el resto hereda
        self.title_value.setStyleSheet("color: #3b82f6;")  
        self.title_value.setWordWrap(True)
        song_info_layout.addWidget(title_label, 0, 0, Qt.AlignTop)
        song_info_layout.addWidget(self.title_value, 0, 1)

        # Artista
        artist_label = QLabel("🎤 Artista:")
        artist_label.setFont(label_font)
        self.artist_value = QLabel("Desconocido")
        self.artist_value.setFont(value_font)
        self.artist_value.setWordWrap(True)
        song_info_layout.addWidget(artist_label, 1, 0, Qt.AlignTop)
        song_info_layout.addWidget(self.artist_value, 1, 1)

        # Álbum
        album_label = QLabel("💿 Álbum:")
        album_label.setFont(label_font)
        self.album_value = QLabel("Desconocido")
        self.album_value.setFont(value_font)
        self.album_value.setWordWrap(True)
        song_info_layout.addWidget(album_label, 2, 0, Qt.AlignTop)
        song_info_layout.addWidget(self.album_value, 2, 1)

        # Info técnica
        tech_label = QLabel("📊 Información:")
        tech_label.setFont(label_font)
        self.duration_value = QLabel("0:00")
        self.bitrate_value = QLabel("0 kbps")
        self.sample_rate_value = QLabel("0 kHz")

        tech_layout = QHBoxLayout()
        tech_layout.setSpacing(8)
        for text, widget in [
            ("Duración:", self.duration_value),
            ("•", None),
            ("Bitrate:", self.bitrate_value),
            ("•", None),
            ("Frecuencia:", self.sample_rate_value),
        ]:
            lbl = QLabel(text) if text != "•" else QLabel("•")
            tech_layout.addWidget(lbl)
            if widget:
                tech_layout.addWidget(widget)
        song_info_layout.addWidget(tech_label, 3, 0, Qt.AlignTop)
        song_info_layout.addLayout(tech_layout, 3, 1)

        # Progreso
        progress_label = QLabel("⏱ Progreso:")
        progress_label.setFont(label_font)
        self.progress_label = QLabel("0:00 / 0:00")
        self.progress_bar = QSlider(Qt.Horizontal)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.sliderMoved.connect(self.set_position)

        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(6)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)

        song_info_layout.addWidget(progress_label, 4, 0, Qt.AlignTop)
        song_info_layout.addLayout(progress_layout, 4, 1)

        info_right_layout.addLayout(song_info_layout)

        # --- Portada (derecha) ---
        cover_widget = QWidget()
        cover_layout = QVBoxLayout(cover_widget)
        cover_layout.setContentsMargins(0, 0, 0, 0)
        cover_layout.setSpacing(0)

        self.cover_art_label = QLabel("🎵")
        self.cover_art_label.setAlignment(Qt.AlignCenter)
        self.cover_art_label.setFixedSize(200, 200)
        self.cover_art_label.setStyleSheet("""
            border: 0px;
            background-color: palette(base);
            color: palette(text);
        """)
        cover_layout.addWidget(self.cover_art_label, alignment=Qt.AlignCenter)

        # 👉 primero info, luego portada
        info_layout.addWidget(info_right, 3)
        info_layout.addWidget(cover_widget, 1)

        main_layout.addWidget(info_group)



    
    def setup_controls_area(self, main_layout):
        """Configura el área de controles de reproducción"""
        controls_group = QGroupBox("🎛️ CONTROLES")
        controls_group.setFont(QFont("Arial", 11, QFont.Bold))
        controls_layout = QVBoxLayout(controls_group)
        controls_layout.setSpacing(6)
        controls_layout.setContentsMargins(8, 15, 8, 8)
        
        # Controles de reproducción
        playback_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton("⏮️ ANTERIOR")
        self.prev_btn.clicked.connect(self.play_previous)
        self.prev_btn.setFont(QFont("Arial", 10))
        playback_layout.addWidget(self.prev_btn)
        
        self.play_btn = QPushButton("▶️ REPRODUCIR")
        self.play_btn.clicked.connect(self.toggle_play)
        self.play_btn.setFont(QFont("Arial", 10))
        playback_layout.addWidget(self.play_btn)
        
        self.stop_btn = QPushButton("⏹️ DETENER")
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setFont(QFont("Arial", 10))
        playback_layout.addWidget(self.stop_btn)
        
        self.next_btn = QPushButton("⏭️ SIGUIENTE")
        self.next_btn.clicked.connect(self.play_next)
        self.next_btn.setFont(QFont("Arial", 10))
        playback_layout.addWidget(self.next_btn)
        
        controls_layout.addLayout(playback_layout)
        
        # Controles de volumen
        volume_layout = QHBoxLayout()
        
        volume_layout.addWidget(QLabel("🔈"))
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.config.get('volume', 80))
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        volume_layout.addWidget(self.volume_slider)
        
        volume_layout.addWidget(QLabel("🔊"))
        
        self.volume_label = QLabel(f"{self.config.get('volume', 80)}%")
        self.volume_label.setFont(QFont("Arial", 11))
        volume_layout.addWidget(self.volume_label)
        
        controls_layout.addLayout(volume_layout)
        
        main_layout.addWidget(controls_group)
    
    def update_clock(self):
        """Actualiza la fecha y hora actual"""
        now = datetime.now()
        self.date_label.setText(now.strftime("%A, %d de %B de %Y"))
        hour_12 = now.strftime("%I:%M:%S %p")
        self.clock_label.setText(f"🕒 {hour_12}")
    
    def update_weather_async(self):
        """Actualiza el clima de forma asíncrona"""
        if self.weather_worker and self.weather_worker.isRunning():
            return
            
        self.weather_worker = WeatherWorker(self.weather_manager)
        self.weather_worker.weather_ready.connect(self.update_weather_display)
        self.weather_worker.start()
    
    def update_weather_display(self, weather_data):
        """Actualiza la visualización del clima"""
        if weather_data:
            weather_text = self.weather_manager.format_weather_info(weather_data)
            self.weather_label.setText(weather_text)
        else:
            self.weather_label.setText("🌤️ Clima no disponible")
    
    def update_counts(self):
        """Actualiza los contadores de canciones y duración"""
        total_songs = self.playlist_list.count()
        self.playlist_count_label.setText(f"Total: {total_songs} canciones")
        
        # Calcular duración total usando los metadatos disponibles
        total_seconds = self.playlist_manager.calculate_total_duration()
        
        # Si no hay metadatos disponibles, calcular duración básica
        if total_seconds == 0 and total_songs > 0:
            total_seconds = self.calculate_basic_duration()
        
        duration_text = self.playlist_manager.format_duration(total_seconds)
        self.playlist_duration_label.setText(f"Duración: {duration_text}")

    def calculate_basic_duration(self):
        """Calcula la duración básica de todas las canciones en la playlist"""
        total_seconds = 0
        for song_path in self.playlist_manager.playlist:
            try:
                audio = File(song_path)
                if audio and hasattr(audio.info, 'length'):
                    total_seconds += audio.info.length
            except:
                continue
        return total_seconds
    
    def update_progress(self):
        """Actualiza la barra de progreso de reproducción"""
        if self.player.is_playing():
            media = self.player.get_media()
            if media:
                media.parse()
                duration = media.get_duration()
                if duration > 0:
                    current_time = self.player.get_time()
                    minutes = current_time // 60000
                    seconds = (current_time % 60000) // 1000
                    total_minutes = duration // 60000
                    total_seconds = (duration % 60000) // 1000
                    
                    self.progress_label.setText(f"{minutes}:{seconds:02d} / {total_minutes}:{total_seconds:02d}")
                    progress = int((current_time / duration) * 100)
                    self.progress_bar.setValue(progress)
                    
                    # Verificar si la canción ha terminado y pasar a la siguiente
                    if current_time >= duration - 1000:  # 1 segundo antes del final
                        self.play_next()
    
    def set_position(self, position):
        """Establece la posición de reproducción"""
        if self.player.get_media():
            media = self.player.get_media()
            media.parse()
            duration = media.get_duration()
            if duration > 0:
                self.player.set_time(int(position * duration / 100))
    
    def set_volume(self, volume):
        """Establece el volumen de reproducción"""
        self.player.audio_set_volume(volume)
        self.volume_label.setText(f"{volume}%")
        self.config['volume'] = volume
        self.config_manager.save_config(self.config)
    
    def toggle_play(self):
        """Alterna entre reproducir y pausar"""
        if self.is_playing:
            self.pause()
        else:
            self.play_selected()
    
    def play_selected(self):
        """Reproduce la canción seleccionada en la playlist"""
        current_row = self.playlist_list.currentRow()
        if current_row >= 0:
            self.playlist_manager.current_index = current_row
            self.play_song(self.playlist_manager.playlist[current_row])
        elif self.playlist_list.count() > 0:
            # Si no hay selección pero hay canciones, reproducir la primera
            self.playlist_manager.current_index = 0
            self.play_song(self.playlist_manager.playlist[0])
            self.playlist_list.setCurrentRow(0)
    
    def play_song(self, song_path):
        """Reproduce una canción específica"""
        try:
            # Si ya estamos reproduciendo, pausar primero
            if self.player.is_playing():
                self.player.pause()
            
            # Si es una canción nueva, cargarla
            if self.current_media != song_path:
                media = self.instance.media_new(song_path)
                self.player.set_media(media)
                self.current_media = song_path
            
            self.player.play()
            self.is_playing = True
            self.play_btn.setText("⏸️ PAUSAR")
            
            # Actualizar información de la canción actual
            song_name = os.path.splitext(os.path.basename(song_path))[0]
            
            # Resaltar la canción actual en la playlist
            for i in range(self.playlist_list.count()):
                item = self.playlist_list.item(i)
                if item.data(Qt.UserRole) == song_path:
                    item.setSelected(True)
                    break
            
            # Extraer y mostrar metadatos si están disponibles
            metadata = self.playlist_manager.get_metadata(song_path)
            self.update_song_info(metadata, song_name)
                
        except Exception as e:
            self.show_error("Error de reproducción", f"No se pudo reproducir la canción: {str(e)}")
    
    def update_song_info(self, metadata, song_name):
        """Actualiza la información de la canción en la interfaz"""
        if metadata:
            # Actualizar la información con metadatos
            self.title_value.setText(metadata.get('title', song_name))
            self.artist_value.setText(metadata.get('artist', 'Desconocido'))
            self.album_value.setText(metadata.get('album', 'Desconocido'))
            self.duration_value.setText(metadata.get('duration', '0:00'))
            self.bitrate_value.setText(metadata.get('bitrate', '0 kbps'))
            self.sample_rate_value.setText(metadata.get('sample_rate', '0 kHz'))
            
            # AÑADIR ESTO: Mostrar la portada en la interfaz principal
            cover_art = metadata.get('cover_art')
            if cover_art:
                pixmap = QPixmap()
                pixmap.loadFromData(cover_art)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(
                        self.cover_art_label.width(),
                        self.cover_art_label.height(),
                        Qt.IgnoreAspectRatio,   # <-- clave
                        Qt.SmoothTransformation
                    )
                    self.cover_art_label.setPixmap(scaled_pixmap)
                else:
                    self.cover_art_label.clear()
                    self.cover_art_label.setText("🎵")
            else:
                self.cover_art_label.clear()
                self.cover_art_label.setText("🎵")
        else:
            # Información básica si no hay metadatos
            self.title_value.setText(song_name)
            self.artist_value.setText("Desconocido")
            self.album_value.setText("Desconocido")
            self.duration_value.setText("0:00")
            self.bitrate_value.setText("0 kbps")
            self.sample_rate_value.setText("0 kHz")
            self.cover_art_label.clear()
            self.cover_art_label.setText("🎵")
            
            # Iniciar extracción de metadatos
            self.extract_metadata_for_song(self.current_media)
    
    def pause(self):
        """Pausa la reproducción"""
        if self.player.is_playing():
            self.player.pause()
            self.is_playing = False
            self.play_btn.setText("▶️ REPRODUCIR")
    
    def stop(self):
        """Detiene la reproducción"""
        self.player.stop()
        self.is_playing = False
        self.current_media = None
        self.play_btn.setText("▶️ REPRODUCIR")
        self.progress_bar.setValue(0)
        self.progress_label.setText("0:00 / 0:00")
        
        # Restablecer información de la canción
        self.title_value.setText("Selecciona una canción")
        self.artist_value.setText("Desconocido")
        self.album_value.setText("Desconocido")
        self.duration_value.setText("0:00")
        self.bitrate_value.setText("0 kbps")
        self.sample_rate_value.setText("0 kHz")
    
    def play_previous(self):
        """Reproduce la canción anterior"""
        if self.playlist_manager.current_index > 0:
            self.playlist_manager.current_index -= 1
            self.play_song(self.playlist_manager.playlist[self.playlist_manager.current_index])
            self.playlist_list.setCurrentRow(self.playlist_manager.current_index)
    
    def play_next(self):
        """Reproduce la siguiente canción"""
        if self.playlist_manager.current_index < len(self.playlist_manager.playlist) - 1:
            self.playlist_manager.current_index += 1
            self.play_song(self.playlist_manager.playlist[self.playlist_manager.current_index])
            self.playlist_list.setCurrentRow(self.playlist_manager.current_index)
        elif self.playlist_manager.playlist:
            # Si estamos al final, volver al inicio
            self.playlist_manager.current_index = 0
            self.play_song(self.playlist_manager.playlist[0])
            self.playlist_list.setCurrentRow(0)
    
    def add_folder(self):
        """Añade una carpeta a la lista de carpetas monitoreadas"""
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder_path and folder_path not in self.folders:
            self.folders.append(folder_path)
            self.config_manager.save_folders(self.folders)
            self.update_folders_tree()  # Esto ahora usará el nuevo método
            
            # Análisis del contenido para el mensaje informativo (NO modifica la funcionalidad)
            audio_files = []
            subfolders = []
            
            try:
                audio_extensions = ('.mp3', '.wav', '.ogg', '.flac', '.m4a', '.wma')
                
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    
                    if os.path.isfile(item_path) and item.lower().endswith(audio_extensions):
                        audio_files.append(item)
                    elif os.path.isdir(item_path):
                        subfolders.append(item)
            except:
                pass  # Si hay error en el análisis, igual se añade la carpeta
            
            # Mensaje informativo según el contenido
            folder_name = os.path.basename(folder_path)
            
            if audio_files and subfolders:
                self.show_info("Carpeta añadida", 
                            f"📂 Se añadió: {folder_name}\n\n"
                            f"📊 Contenido:\n"
                            f"• {len(audio_files)} archivo(s) de audio 🎵\n"
                            f"• {len(subfolders)} subcarpeta(s) 📁\n\n"
                            f"📍 Ubicación: {folder_path}")
            
            elif audio_files:
                self.show_info("Carpeta con música añadida", 
                            f"🎵 Se añadió: {folder_name}\n\n"
                            f"📊 Contenido: {len(audio_files)} archivo(s) de audio\n\n"
                            f"📍 Ubicación: {folder_path}")
            
            elif subfolders:
                self.show_info("Carpeta con subcarpetas añadida", 
                            f"📂 Se añadió: {folder_name}\n\n"
                            f"📊 Contenido: {len(subfolders)} subcarpeta(s)\n\n"
                            f"📍 Ubicación: {folder_path}\n\n"
                            f"💡 Explora las subcarpetas para encontrar música.")
            
            else:
                self.show_info("Carpeta añadida", 
                            f"📂 Se añadió: {folder_name}\n\n"
                            f"📊 La carpeta está vacía o no contiene archivos de audio reconocidos.\n\n"
                            f"📍 Ubicación: {folder_path}")

    def remove_folder(self):
        """Elimina una carpeta de la lista de carpetas monitoreadas"""
        current_item = self.folders_tree.currentItem()
        if not current_item:
            return
        
        # Solo permitir eliminar carpetas raíz (sin padre)
        if current_item.parent() is not None:
            folder_name = current_item.text(0)
            parent_path = current_item.parent().data(0, Qt.UserRole)
            parent_name = os.path.basename(parent_path)
            
            self.show_info("No se puede eliminar", 
                        f"❌ No puedes eliminar subcarpetas individualmente.\n\n"
                        f"📂 Subcarpeta: {folder_name}\n"
                        f"📦 Dentro de: {parent_name}\n\n"
                        f"💡 Para eliminar esta subcarpeta, debes eliminar la carpeta principal\n"
                        f"que la contiene: {parent_path}")
            return
        
        # Para carpetas raíz, obtener la ruta completa
        folder_path = current_item.data(0, Qt.UserRole)
        folder_name = current_item.text(0)
        
        if folder_path and folder_path in self.folders:
            # Mensaje de confirmación en español
            reply = self.show_question("Eliminar carpeta", 
                                    f"¿Estás seguro de eliminar esta carpeta de la lista?\n\n"
                                    f"📂 {folder_name}\n"
                                    f"📍 {folder_path}\n\n"
                                    f"⚠️ Esto no elimina los archivos físicos,\n"
                                    f"solo quita la carpeta de la lista monitoreada.")
            
            if reply:  # Si el usuario hizo clic en Sí
                # Eliminar la carpeta de la lista
                self.folders.remove(folder_path)
                self.config_manager.save_folders(self.folders)
                
                # Actualizar la vista
                self.update_folders_tree()
                
                # Limpiar la lista de canciones
                self.songs_list.clear()
                self.all_songs = []
                
                self.show_info("Carpeta eliminada", 
                            f"✅ Se eliminó de la lista:\n\n"
                            f"📂 {folder_name}\n"
                            f"📍 {folder_path}\n\n"
                            f"Los archivos permanecen en su ubicación original.")
        else:
            self.show_warning("Carpeta no encontrada", 
                            f"La carpeta seleccionada no está en la lista monitoreada.\n\n"
                            f"📂 {folder_name}\n"
                            f"📍 {folder_path if folder_path else 'Ruta no disponible'}")
    
    def refresh_folders(self):
        """Actualiza la vista de carpetas y canciones"""
        self.update_folders_tree()
    
    def update_folders_tree(self):
        """Actualiza el árbol de carpetas"""
        self.folders_tree.clear()
        for folder in self.folders:
            # Añadir carpeta raíz con la ruta COMPLETA como texto
            folder_item = QTreeWidgetItem(self.folders_tree, [os.path.basename(folder)])  # Solo mostrar nombre
            folder_item.setData(0, Qt.UserRole, folder)  # Guardar ruta completa en UserRole
            folder_item.setIcon(0, self.style().standardIcon(self.style().SP_DirIcon))
            
            # Añadir subcarpetas (solo nombre para mostrar)
            try:
                for subfolder in os.listdir(folder):
                    subfolder_path = os.path.join(folder, subfolder)
                    if os.path.isdir(subfolder_path):
                        subfolder_item = QTreeWidgetItem(folder_item, [subfolder])  # Solo nombre
                        subfolder_item.setData(0, Qt.UserRole, subfolder_path)  # Guardar ruta completa
                        subfolder_item.setIcon(0, self.style().standardIcon(self.style().SP_DirIcon))
            except:
                pass  # Ignorar errores de permisos
    
    def on_folder_selected(self, item, column):
        """Maneja la selección de una carpeta en el árbol"""
        folder_path = item.data(0, Qt.UserRole)  # Obtener ruta completa desde los datos
        if folder_path and os.path.exists(folder_path):
            self.load_songs_from_folder(folder_path)
    
    def load_songs_from_folder(self, folder_path):
        """Carga las canciones desde una carpeta"""
        self.songs_list.clear()
        self.all_songs = []
        
        try:
            audio_extensions = ('.mp3', '.wav', '.ogg', '.flac', '.m4a', '.wma')
            for file in os.listdir(folder_path):
                if file.lower().endswith(audio_extensions):
                    song_path = os.path.join(folder_path, file)
                    song_name = os.path.splitext(file)[0]
                    self.all_songs.append((song_path, song_name))
                    
                    item = QListWidgetItem(f"🎵 {song_name}")
                    item.setData(Qt.UserRole, song_path)
                    self.songs_list.addItem(item)
        except Exception as e:
            self.show_error("Error", f"No se pudo acceder a la carpeta: {str(e)}")
    
    def filter_songs(self, text):
        """Filtra las canciones según el texto de búsqueda"""
        self.songs_list.clear()
        text = text.lower()
        
        for song_path, song_name in self.all_songs:
            if text in song_name.lower():
                item = QListWidgetItem(f"🎵 {song_name}")
                item.setData(Qt.UserRole, song_path)
                self.songs_list.addItem(item)
    
    def add_to_playlist(self, item):
        """Añade una canción a la playlist al hacer doble clic"""
        song_path = item.data(Qt.UserRole)
        song_name = os.path.splitext(os.path.basename(song_path))[0]
        
        if self.playlist_manager.add_song(song_path, song_name):
            self.update_counts()
            
            # Iniciar extracción de metadatos en segundo plano
            self.extract_metadata_for_song(song_path)
    
    def add_selected_to_playlist(self):
        """Añade las canciones seleccionadas a la playlist"""
        selected_items = self.songs_list.selectedItems()
        
        # Validar si no hay canciones seleccionadas
        if not selected_items:
            self.show_warning("Sin selección", "No hay canciones seleccionadas. Por favor, selecciona al menos una canción.")
            return
        
        added_count = 0
        
        for item in selected_items:
            song_path = item.data(Qt.UserRole)
            song_name = os.path.splitext(os.path.basename(song_path))[0]
            
            if self.playlist_manager.add_song(song_path, song_name):
                added_count += 1
                
                # Iniciar extracción de metadatos en segundo plano
                self.extract_metadata_for_song(song_path)
        
        if added_count > 0:
            self.update_counts()
            if added_count > 3:
                self.show_info("Canciones añadidas", 
                            f"Se añadieron {added_count} canciones a la playlist.\n\n"
                            f"📊 Playlist actual: {self.playlist_list.count()} canciones\n"
                            f"⏱ Duración total: {self.playlist_duration_label.text().replace('Duración: ', '')}")
            else:
                # Para pocas canciones, solo mostrar un mensaje breve
                self.statusBar().showMessage(f"✓ Añadidas {added_count} canciones", 3000)
    
    def add_all_to_playlist(self):
        """Añade todas las canciones a la playlist"""
        if self.songs_list.count() == 0:
            self.show_warning("Sin canciones", "No hay canciones para añadir.")
            return
        
        songs_to_add = []
        total_duration_seconds = 0
        
        for i in range(self.songs_list.count()):
            item = self.songs_list.item(i)
            song_path = item.data(Qt.UserRole)
            song_name = os.path.splitext(os.path.basename(song_path))[0]
            songs_to_add.append((song_path, song_name))
            
            # Obtener duración básica al instante (sin metadatos completos)
            try:
                audio = File(song_path)
                if audio and hasattr(audio.info, 'length'):
                    total_duration_seconds += audio.info.length
            except:
                pass  # Si falla, no sumamos nada a la duración
        
        added_count = self.playlist_manager.add_songs(songs_to_add)
        
        if added_count > 0:
            # Calcular duración formateada
            hours = int(total_duration_seconds // 3600)
            minutes = int((total_duration_seconds % 3600) // 60)
            seconds = int(total_duration_seconds % 60)
            
            if hours > 0:
                duration_text = f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                duration_text = f"{minutes}:{seconds:02d}"
            
            # Iniciar extracción de metadatos completos en segundo plano
            for song_path, song_name in songs_to_add:
                self.extract_metadata_for_song(song_path)
            
            self.update_counts()
            
            self.show_info("Todas las canciones añadidas", 
                        f"Se añadieron {added_count} canciones a la playlist.\n\n"
                        f"📊 Total en playlist: {self.playlist_list.count()} canciones\n"
                        f"⏱ Duración estimada: {duration_text}\n\n"
                        f"💡 Los metadatos se extraerán en segundo plano.")
    
    def remove_from_playlist(self):
        """Elimina la canción seleccionada de la playlist"""
        current_row = self.playlist_list.currentRow()
        if current_row >= 0:
            removed_song = self.playlist_manager.remove_song(current_row)
            if removed_song:
                self.update_counts()
    
    def clear_playlist(self):
        """Limpia toda la playlist"""
        if self.playlist_list.count() > 0:
            total_songs = self.playlist_list.count()
            total_duration = self.playlist_duration_label.text().replace('Duración: ', '')
            
            # Usar show_question que devuelve True si se hizo clic en Sí
            if self.show_question("Limpiar playlist", 
                                f"¿Estás seguro de que quieres limpiar toda la playlist?\n\n"
                                f"📊 Canciones: {total_songs}\n"
                                f"⏱ Duración: {total_duration}\n\n"
                                f"⚠️ Esta acción no se puede deshacer."):
                
                self.playlist_manager.clear()
                self.update_counts()
                self.stop()
                
                self.show_info("Playlist limpiada", 
                            f"Se eliminaron todas las canciones de la playlist.\n\n"
                            f"🗑️ {total_songs} canciones eliminadas\n"
                            f"⏱ {total_duration} de duración eliminada")
    
    def move_up_in_playlist(self):
        """Mueve la canción seleccionada hacia arriba en la playlist"""
        current_row = self.playlist_list.currentRow()
        if current_row > 0:
            # Mover en la lista de canciones
            self.playlist_manager.playlist[current_row], self.playlist_manager.playlist[current_row - 1] = \
                self.playlist_manager.playlist[current_row - 1], self.playlist_manager.playlist[current_row]
            
            # Mover en el widget de lista
            item = self.playlist_list.takeItem(current_row)
            self.playlist_list.insertItem(current_row - 1, item)
            self.playlist_list.setCurrentRow(current_row - 1)
            
            # Actualizar índice actual si es necesario
            if self.playlist_manager.current_index == current_row:
                self.playlist_manager.current_index = current_row - 1
            elif self.playlist_manager.current_index == current_row - 1:
                self.playlist_manager.current_index = current_row
    
    def move_down_in_playlist(self):
        """Move the selected song down in the playlist"""
        current_row = self.playlist_list.currentRow()
        if current_row < self.playlist_list.count() - 1:
            # Mover en la lista de canciones
            self.playlist_manager.playlist[current_row], self.playlist_manager.playlist[current_row + 1] = \
                self.playlist_manager.playlist[current_row + 1], self.playlist_manager.playlist[current_row]
            
            # Mover en el widget de lista
            item = self.playlist_list.takeItem(current_row)
            self.playlist_list.insertItem(current_row + 1, item)
            self.playlist_list.setCurrentRow(current_row + 1)
            
            # Actualizar índice actual si es necesario
            if self.playlist_manager.current_index == current_row:
                self.playlist_manager.current_index = current_row + 1
            elif self.playlist_manager.current_index == current_row + 1:
                self.playlist_manager.current_index = current_row
    
    def export_playlist(self):
        """Exporta la playlist a un archivo"""
        if self.playlist_list.count() == 0:
            self.show_warning("Playlist vacía", "No hay canciones en la playlist para exportar.")
            return
        
        total_songs = self.playlist_list.count()
        total_duration = self.playlist_duration_label.text().replace('Duración: ', '')
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exportar Playlist", "", "Archivos JSON (*.json);;Todos los archivos (*)"
        )
        
        if file_path:
            try:
                if self.playlist_manager.export_to_file(file_path):
                    self.show_info("Playlist exportada", 
                                f"✅ Playlist exportada correctamente.\n\n"
                                f"📊 Canciones: {total_songs}\n"
                                f"⏱ Duración: {total_duration}\n"
                                f"💾 Archivo: {os.path.basename(file_path)}\n\n"
                                f"⚠️ Importante: Si eliminas las canciones originales de tu computadora,\n"
                                f"al importar esta playlist las canciones no podrán ser encontradas.")
            except Exception as e:
                self.show_error("Error al exportar", f"No se pudo exportar la playlist: {str(e)}")

    def import_playlist(self):
        """Importa una playlist desde un archivo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Importar Playlist", "", "Archivos JSON (*.json);;Todos los archivos (*)"
        )
        
        if file_path:
            try:
                songs, metadata = self.playlist_manager.import_from_file(file_path)
                
                # Verificar cuántas canciones existen realmente
                existing_songs = []
                missing_songs = []
                
                for song_path in songs:
                    if os.path.exists(song_path):
                        existing_songs.append(song_path)
                    else:
                        missing_songs.append(song_path)
                
                # Añadir solo las canciones que existen
                added_count = 0
                for song_path in existing_songs:
                    song_name = os.path.splitext(os.path.basename(song_path))[0]
                    song_metadata = metadata.get(song_path, {})
                    if self.playlist_manager.add_song(song_path, song_name, song_metadata):
                        added_count += 1
                
                if added_count > 0:
                    self.update_counts()
                    
                    message = f"Se importaron {added_count} canciones a la playlist."
                    if missing_songs:
                        message += f"\n\n⚠️ {len(missing_songs)} canciones no se encontraron:\n"
                        message += f"• Estas canciones fueron eliminadas o movidas de su ubicación original.\n"
                        message += f"• Revisa la ubicación de los archivos si quieres reproducirlas."
                    
                    self.show_info("Playlist importada", message)
                else:
                    if missing_songs:
                        self.show_warning("Playlist importada - Canciones no encontradas", 
                                    f"No se pudieron importar canciones porque:\n\n"
                                    f"❌ {len(missing_songs)} canciones no se encuentran en su ubicación original.\n\n"
                                    f"💡 Verifica que los archivos de audio todavía existan\n"
                                    f"en las rutas especificadas en el archivo de playlist.")
                    else:
                        self.show_warning("Sin canciones", "No se pudieron importar canciones desde el archivo.")
                        
            except Exception as e:
                self.show_error("Error al importar", f"No se pudo importar la playlist: {str(e)}")
    
    def extract_metadata_for_song(self, song_path):
        """Inicia la extracción de metadatos para una canción en segundo plano"""
        if self.metadata_worker and self.metadata_worker.isRunning():
            # Si ya hay un worker ejecutándose, programar esta extracción para después
            QTimer.singleShot(1000, lambda: self.extract_metadata_for_song(song_path))
            return
            
        self.metadata_worker = MetadataWorker(song_path)
        self.metadata_worker.metadata_ready.connect(
            lambda metadata: self.on_metadata_ready(song_path, metadata)
        )
        self.metadata_worker.start()
    
    def on_metadata_ready(self, song_path, metadata):
        """Maneja los metadatos extraídos para una canción"""
        # Actualizar los metadatos en el playlist manager
        self.playlist_manager.update_metadata(song_path, metadata)
        
        # Si esta es la canción actualmente reproduciéndose, actualizar la información
        if (self.player.is_playing() and 
            self.playlist_manager.current_index >= 0 and
            self.playlist_manager.playlist[self.playlist_manager.current_index] == song_path):
            
            song_name = os.path.splitext(os.path.basename(song_path))[0]
            self.update_song_info(metadata, song_name)
        
        # Actualizar contadores
        self.update_counts()
    
    def extract_all_metadata(self):
        """Extrae metadatos para todas las canciones en la playlist"""
        if self.playlist_list.count() == 0:
            self.show_warning("Playlist vacía", "No hay canciones en la playlist para extraer metadatos.")
            return
        
        # Contador para mostrar progreso
        total = self.playlist_list.count()
        processed = 0
        
        for i in range(total):
            song_path = self.playlist_manager.playlist[i]
            self.extract_metadata_for_song(song_path)
            processed += 1
            
            # Actualizar contador en la interfaz (opcional)
            if i % 5 == 0:  # Actualizar cada 5 canciones para no saturar
                QApplication.processEvents()
        
        self.show_info("Extracción completada", f"Se extrajeron metadatos para {processed} canciones.")
    
    def view_current_metadata(self):
        """Muestra los metadatos de la canción actual o seleccionada"""
        song_path = None
        
        # Obtener la canción actualmente reproduciéndose o seleccionada
        if self.player.is_playing() and self.playlist_manager.current_index >= 0:
            song_path = self.playlist_manager.playlist[self.playlist_manager.current_index]
        else:
            current_row = self.playlist_list.currentRow()
            if current_row >= 0:
                song_path = self.playlist_manager.playlist[current_row]
        
        if song_path:
            metadata = self.playlist_manager.get_metadata(song_path)
            if metadata:
                self.show_metadata(metadata)
            else:
                self.show_info("Sin metadatos", "No hay metadatos disponibles para esta canción. Puedes extraerlos desde el menú Metadatos.")
        else:
            self.show_warning("Sin canción seleccionada", "Selecciona una canción para ver sus metadatos.")
    
    def apply_theme(self, theme):
        """Aplica un tema claro u oscuro a la interfaz"""
        self.config['theme'] = theme
        self.config_manager.save_config(self.config)
        
        if theme == 'dark':
            # Tema oscuro - colores más sutiles
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.Window, QColor(30, 30, 40))  # Fondo más azulado
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(25, 25, 35))
            dark_palette.setColor(QPalette.AlternateBase, QColor(45, 45, 55))
            dark_palette.setColor(QPalette.ToolTipBase, QColor(40, 40, 50))
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(50, 50, 60))
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Link, QColor(100, 150, 255))
            dark_palette.setColor(QPalette.Highlight, QColor(80, 120, 240))
            dark_palette.setColor(QPalette.HighlightedText, Qt.white)
            
            QApplication.setPalette(dark_palette)

            if theme == 'dark':
    # Asegurar que el encabezado del árbol sea visible
                header_style = """
                    QHeaderView::section {
                        background-color: #374151;
                        color: #e5e7eb;
                        padding: 6px;
                        border: none;
                        border-right: 1px solid #4b5563;
                        font-weight: bold;
                    }
                """
                self.folders_tree.header().setStyleSheet(header_style)
            else:
                # Restablecer al estilo por defecto en tema claro
                self.folders_tree.header().setStyleSheet("")
            
            # Estilos adicionales para grupos y botones - más minimalistas
            group_style = """
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #4b5563;
                    border-radius: 8px;
                    margin-top: 1ex;
                    padding-top: 10px;
                    background-color: #1f2937;
                    color: #e5e7eb;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #9ca3af;
                }
            """
            
            button_style = """
                QPushButton {
                    background-color: #374151;
                    border: 1px solid #4b5563;
                    border-radius: 6px;
                    color: #e5e7eb;
                    padding: 8px 16px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #4b5563;
                    border: 1px solid #6b7280;
                }
                QPushButton:pressed {
                    background-color: #1f2937;
                }
                QPushButton:disabled {
                    background-color: #374151;
                    color: #6b7280;
                }
            """
            
            # Botones especiales (reproducir, etc.) con color de acento
            accent_button_style = """
                QPushButton {
                    background-color: #3b82f6;
                    border: none;
                    border-radius: 6px;
                    color: white;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
                QPushButton:pressed {
                    background-color: #1e40af;
                }
            """
            
            list_style = """
                QListWidget, QTreeWidget {
                    background-color: #111827;
                    color: #e5e7eb;
                    border: 1px solid #374151;
                    border-radius: 6px;
                    alternate-background-color: #1f2937;
                }
                QListWidget::item:selected, QTreeWidget::item:selected {
                    background-color: #3b82f6;
                    color: white;
                }
                QListWidget::item:hover, QTreeWidget::item:hover {
                    background-color: #374151;
                }
                QTreeWidget::header {
                    background-color: #374151;
                    color: #e5e7eb;
                    font-weight: bold;
                    border: none;
                    border-bottom: 1px solid #4b5563;
                }
                QTreeWidget::header::section {
                    background-color: #374151;
                    color: #e5e7eb;
                    padding: 6px;
                    border: none;
                    border-right: 1px solid #4b5563;
                }
                QTreeWidget::header::section:last {
                    border-right: none;
                }
            """
            
            slider_style = """
                QSlider::groove:horizontal {
                    border: 1px solid #4b5563;
                    height: 8px;
                    background: #1f2937;
                    margin: 2px 0;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #3b82f6;
                    border: 1px solid #2563eb;
                    width: 18px;
                    margin: -4px 0;
                    border-radius: 9px;
                }
                QSlider::sub-page:horizontal {
                    background: #3b82f6;
                    border: 1px solid #3b82f6;
                    height: 8px;
                    border-radius: 4px;
                }
            """
            
            line_edit_style = """
                QLineEdit {
                    background-color: #1f2937;
                    color: #e5e7eb;
                    border: 1px solid #4b5563;
                    border-radius: 6px;
                    padding: 6px;
                }
                QLineEdit:focus {
                    border: 1px solid #3b82f6;
                }
            """
            
            # Estilos para menús
            menu_style = """
                QMenuBar {
                    background-color: #1f2937;
                    color: #e5e7eb;
                    border-bottom: 1px solid #374151;
                }
                QMenuBar::item {
                    background: transparent;
                    color: #e5e7eb;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background: #374151;
                    border-radius: 4px;
                }
                QMenu {
                    background-color: #1f2937;
                    color: #e5e7eb;
                    border: 1px solid #374151;
                    padding: 4px;
                }
                QMenu::item:selected {
                    background-color: #3b82f6;
                    border-radius: 4px;
                }
            """
            
        else:
            # Tema claro - colores suaves y minimalistas
            light_palette = QPalette()
            light_palette.setColor(QPalette.Window, QColor(240, 241, 245))
            light_palette.setColor(QPalette.WindowText, Qt.black)
            light_palette.setColor(QPalette.Base, QColor(255, 255, 255))
            light_palette.setColor(QPalette.AlternateBase, QColor(243, 244, 246))
            light_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
            light_palette.setColor(QPalette.ToolTipText, Qt.black)
            light_palette.setColor(QPalette.Text, Qt.black)
            light_palette.setColor(QPalette.Button, QColor(229, 231, 235))
            light_palette.setColor(QPalette.ButtonText, Qt.black)
            light_palette.setColor(QPalette.BrightText, Qt.red)
            light_palette.setColor(QPalette.Link, QColor(79, 140, 255))
            light_palette.setColor(QPalette.Highlight, QColor(79, 140, 255))
            light_palette.setColor(QPalette.HighlightedText, Qt.white)
            
            QApplication.setPalette(light_palette)
            
            # Estilos para el tema claro
            group_style = """
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #d1d5db;
                    border-radius: 8px;
                    margin-top: 1ex;
                    padding-top: 10px;
                    background-color: #f9fafb;
                    color: #111827;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #4b5563;
                }
            """
            
            button_style = """
                QPushButton {
                    background-color: #f3f4f6;
                    border: 1px solid #d1d5db;
                    border-radius: 6px;
                    color: #374151;
                    padding: 8px 16px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #e5e7eb;
                    border: 1px solid #9ca3af;
                }
                QPushButton:pressed {
                    background-color: #d1d5db;
                }
                QPushButton:disabled {
                    background-color: #f3f4f6;
                    color: #9ca3af;
                }
            """
            
            # Botones especiales (reproducir, etc.) con color de acento
            accent_button_style = """
                QPushButton {
                    background-color: #4f8cff;
                    border: none;
                    border-radius: 6px;
                    color: white;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3b78e7;
                }
                QPushButton:pressed {
                    background-color: #2b6cdb;
                }
            """
            
            list_style = """
                QListWidget, QTreeWidget {
                    background-color: #ffffff;
                    color: #111827;
                    border: 1px solid #d1d5db;
                    border-radius: 6px;
                    alternate-background-color: #f8f9fa;  /* Color más contrastante */
                }
                QListWidget::item:selected, QTreeWidget::item:selected {
                    background-color: #4f8cff;
                    color: white;
                }
                QListWidget::item:hover, QTreeWidget::item:hover {
                    background-color: #e9ecef;  /* Color de hover más visible */
                }
                QTreeWidget::header {
                    background-color: #e5e7eb;
                    color: #374151;
                    font-weight: bold;
                    border: none;
                    border-bottom: 1px solid #d1d5db;
                }
                QTreeWidget::header::section {
                    background-color: #e5e7eb;
                    color: #374151;
                    padding: 6px;
                    border: none;
                    border-right: 1px solid #d1d5db;
                }
                QTreeWidget::header::section:last {
                    border-right: none;
                }
            """
            
            slider_style = """
                QSlider::groove:horizontal {
                    border: 1px solid #d1d5db;
                    height: 8px;
                    background: #f3f4f6;
                    margin: 2px 0;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #4f8cff;
                    border: 1px solid #3b78e7;
                    width: 18px;
                    margin: -4px 0;
                    border-radius: 9px;
                }
                QSlider::sub-page:horizontal {
                    background: #4f8cff;
                    border: 1px solid #4f8cff;
                    height: 8px;
                    border-radius: 4px;
                }
            """
            
            line_edit_style = """
                QLineEdit {
                    background-color: #ffffff;
                    color: #111827;
                    border: 1px solid #d1d5db;
                    border-radius: 6px;
                    padding: 6px;
                }
                QLineEdit:focus {
                    border: 1px solid #4f8cff;
                }
            """
            
            # Estilos para menús (tema claro)
            menu_style = """
                QMenuBar {
                    background-color: #f9fafb;
                    color: #111827;
                    border-bottom: 1px solid #e5e7eb;
                }
                QMenuBar::item {
                    background: transparent;
                    color: #111827;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background: #e5e7eb;
                    border-radius: 4px;
                }
                QMenu {
                    background-color: #ffffff;
                    color: #111827;
                    border: 1px solid #e5e7eb;
                    padding: 4px;
                }
                QMenu::item:selected {
                    background-color: #4f8cff;
                    color: white;
                    border-radius: 4px;
                }
            """
            tree_header_style = """
                QHeaderView::section {
                    background-color: #e5e7eb;
                    color: #374151;
                    padding: 6px;
                    border: none;
                    border-right: 1px solid #d1d5db;
                    font-weight: bold;
                }
            """
            self.folders_tree.header().setStyleSheet(tree_header_style)

            
        
        # Aplicar estilos a todos los widgets
        for group_box in self.findChildren(QGroupBox):
            group_box.setStyleSheet(group_style)
        
        # Aplicar estilos diferentes a botones normales y especiales
        special_buttons = [self.play_btn, self.stop_btn, self.prev_btn, self.next_btn]
        
        for button in self.findChildren(QPushButton):
            if button in special_buttons:
                button.setStyleSheet(accent_button_style)
            else:
                button.setStyleSheet(button_style)
        
        for list_widget in [self.songs_list, self.playlist_list, self.folders_tree]:
            list_widget.setStyleSheet(list_style)
            list_widget.setAlternatingRowColors(True)  # Asegurar que esté activado
        
        self.progress_bar.setStyleSheet(slider_style)
        self.volume_slider.setStyleSheet(slider_style)
        self.search_input.setStyleSheet(line_edit_style)
        
        # Aplicar estilos a la barra de menú
        self.menuBar().setStyleSheet(menu_style)
        
        # Actualizar el color del título de la canción actual
        title_style = "color: #3b82f6;" if theme == 'dark' else "color: #4f8cff;"
        self.title_value.setStyleSheet(title_style)


def main():
    """Función principal de la aplicación"""
    app = QApplication(sys.argv)
    app.setApplicationName("Radio Conejo")
    app.setApplicationVersion("1.0")
    
    player = MusicPlayer()
    player.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
