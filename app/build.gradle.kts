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
        versionCode = 15
        versionName = "8.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }
}
