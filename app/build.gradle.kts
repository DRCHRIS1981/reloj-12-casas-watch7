plugins {
    id("com.android.application")
}

android {
    namespace = "com.drchris.reloj12casas"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.drchris.reloj12casas"
        minSdk = 33
        targetSdk = 35
        versionCode = 12
        versionName = "7.5"
    }
}

val prepareWatchFace by tasks.registering(Exec::class) {
    workingDir(rootProject.projectDir)
    commandLine("python3", "tools/build_v75.py")
}

tasks.matching { it.name == "preBuild" }.configureEach {
    dependsOn(prepareWatchFace)
}
