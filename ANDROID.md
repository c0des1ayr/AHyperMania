# Android

## Setup

* Install [Android Studio](https://developer.android.com/studio), obviously
* Recursively clone the [RSDKv5 Decompilation](https://github.com/RSDKModding/RSDKv5-Decompilation) **as close to the root of the drive** (`C:\ROOT_OF_DECOMP`) using `git clone --recursive`
* Go to `ROOT_OF_DECOMP\android\app\jni` and recursively clone the [Sonic Mania Decompilation](https://github.com/RSDKModding/RSDKv5-Decompilation) as `Game` with `git clone --recursive https://github.com/RSDKModding/RSDKv5-Decompilation Game`
* Still in `ROOT_OF_DECOMP\android\app\jni`, recursively clone the [AHyperMania](https://github.com/c0des1ayr/AHyperMania) repo

## Download dependencies

* You will need both [libogg and libtheora](https://xiph.org/downloads/). Make sure you download from the section titled "Developer Downloads", and get the ZIPs for easier extraction.
* Extract `libogg-VERSION.zip` to `ROOT_OF_DECOMP\dependencies\android\libogg`, letting the files overwrite the ones already in the `libogg` folder.
* Finally, make a new folder in `ROOT_OF_DECOMP\dependencies\android` and call it `libtheora`, then extract `libtheora-VERSION.zip` into it.

## Build process

* Open Android Studio, then ensure that your SDK version and the NDK are installed.
* Next, open the project `ROOT_OF_DECOMP\android`, wait for the project to be initialized, and build.
* The APK you build will be unsigned, so you'll need to either sign it in Android Studio (hint: Google is your best friend), or you can sideload it using ADB with the command `adb install -t -g app_debug.apk`.