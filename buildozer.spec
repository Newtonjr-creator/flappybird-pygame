[app]
title = Flappy Bird
package.name = com.example.flappybird
package.domain = org.example
version = 1.0.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ogg,wav
icon.filename = %(source.dir)s/icon.png
requirements = python3,kivy,kivymd,pillow,pygame

[buildozer]
# This section should contain paths and environment variables
android.sdk_path = /home/runner/android-sdk
android.ndk_path = /home/runner/android-ndk
android.sdk = 33
android.ndk = 25.1.8937393
android.sdk_build_tools = 33.0.2
