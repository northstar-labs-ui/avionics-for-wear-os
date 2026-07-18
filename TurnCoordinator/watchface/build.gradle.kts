plugins {
    alias(libs.plugins.android.application)
}

apply(from = rootProject.file("../gradle/release-signing.gradle"))

android {
    namespace = "com.northstarlabs.avionics.turncoordinator"
    compileSdk {
        version = release(36) {
            minorApiLevel = 1
        }
    }

    defaultConfig {
        applicationId = "com.northstarlabs.avionics.turncoordinator"
        minSdk = 33
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"

    }

    buildTypes {
        debug {
            // WFF packages must remain resource-only; R8 removes AGP's empty DEX.
            isMinifyEnabled = true
        }
        release {
            isMinifyEnabled = true
            // Every declared watch-face resource is referenced by the WFF runtime.
            isShrinkResources = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    enableKotlin = false
}

dependencies {
}
