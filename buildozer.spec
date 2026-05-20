[app]

title = Dodge Game
package.name = dodgegame
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,jpeg,wav,mp3,kv

version = 1.0

requirements = python3,kivy==2.1.0,pillow

orientation = portrait
fullscreen = 1

android.api = 31
android.minapi = 21
android.ndk = 23b
android.archs = arm64-v8a

android.permissions = INTERNET

[buildozer]

log_level = 2
warn_on_root = 1
