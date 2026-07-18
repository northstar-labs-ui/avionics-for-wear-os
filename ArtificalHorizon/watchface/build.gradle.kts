plugins {
    alias(libs.plugins.android.application)
}

apply(from = rootProject.file("../gradle/release-signing.gradle"))

android {
    namespace = "com.northstarlabs.avionics.artificialhorizon"
    compileSdk {
        version = release(36) {
            minorApiLevel = 1
        }
    }

    defaultConfig {
        applicationId = "com.northstarlabs.avionics.artificialhorizon"
        minSdk = 33
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"

    }

    buildTypes {
        debug {
            // WFF packages are resource-only. R8 removes AGP's otherwise-empty
            // synthetic DEX so the debug APK follows the same rule as release.
            isMinifyEnabled = true
        }
        release {
            isMinifyEnabled = true
            // Every declared watch-face resource is referenced by the runtime
            // rather than application code, so resource shrinking must stay off.
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
