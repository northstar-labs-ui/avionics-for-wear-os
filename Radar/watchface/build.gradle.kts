plugins {
    alias(libs.plugins.android.application)
}

apply(from = rootProject.file("../gradle/release-signing.gradle"))

android {
    namespace = "com.northstarlabs.avionics.radar"
    compileSdk {
        version = release(36) {
            minorApiLevel = 1
        }
    }

    defaultConfig {
        applicationId = "com.northstarlabs.avionics.radar"
        minSdk = 33
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"

    }

    buildTypes {
        release {
            // R8 removes AGP's otherwise-empty DEX from this resource-only WFF package.
            isMinifyEnabled = true
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
