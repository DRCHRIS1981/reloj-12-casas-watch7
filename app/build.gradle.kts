plugins {
    id("com.android.application")
}

android {
    namespace = "com.drchris.reloj12casas"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.drchris.reloj12casas"
        minSdk = 34
        targetSdk = 35
        versionCode = 17
        versionName = "8.2"
    }

    buildTypes {
        debug {
            isMinifyEnabled = true
        }
        release {
            // WFF bundles must be resource-only. Minification removes the
            // generated R classes so the final AAB contains no classes.dex.
            isMinifyEnabled = true
            isShrinkResources = false
        }
    }
}
