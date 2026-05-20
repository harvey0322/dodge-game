[app]

title = Dodge Game

package.name = dodgegame
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,jpeg,wav,mp3,kv

version = 1.0

requirements = python3==3.10,kivy==2.3.0,pillow

orientation = portrait

fullscreen = 1

# Android settings
android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

# Python for Android
p4a.branch = stable

# Permissions
android.permissions = INTERNET

[buildozer]

log_level = 2
warn_on_root = 1
