[app]
title = Flappy Bird
package.name = flappybird
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,mp3,wav
version = 1.0
requirements = python3,kivy,pygame
orientation = portrait
fullscreen = 1

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 23b
android.arch = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1