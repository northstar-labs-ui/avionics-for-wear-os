plugins {
    alias(libs.plugins.android.application)
}

apply(from = rootProject.file("../gradle/release-signing.gradle"))

android {
    namespace = "com.northstarlabs.avionics.helicopter"
    compileSdk {
        version = release(36) {
            minorApiLevel = 1
        }
    }

    defaultConfig {
        applicationId = "com.northstarlabs.avionics.helicopter"
        // WFF v1 and every feature used by this face are available from API 33.
        minSdk = 33
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"

    }

    buildTypes {
        release {
            // R8 removes AGP's otherwise-empty DEX from this resource-only WFF package.
            isMinifyEnabled = true
            // WFF bundles are resource-only; never discard renderer resources.
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
