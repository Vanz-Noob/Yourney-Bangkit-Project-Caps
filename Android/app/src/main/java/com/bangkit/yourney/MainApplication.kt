package com.bangkit.yourney

import android.app.Application
import androidx.appcompat.app.AppCompatDelegate
import com.bangkit.yourney.di.AllModules.networkModule
import com.bangkit.yourney.di.AllModules.repositoryModule
import com.bangkit.yourney.di.AllModules.useCaseModule
import com.bangkit.yourney.di.AllModules.viewModelModule
import org.koin.android.ext.koin.androidContext
import org.koin.android.ext.koin.androidLogger
import org.koin.core.context.startKoin
import org.koin.core.logger.Level

class MainApplication : Application()  {

//    override fun attachBaseContext(base: Context) {
//        super.attachBaseContext(base)
//        MultiDex.install(this)
//    }

    override fun onCreate() {
        super.onCreate()
        AppCompatDelegate.setCompatVectorFromResourcesEnabled(true)
        startKoin {
            androidLogger(Level.NONE)
            androidContext(this@MainApplication)
            modules(
                listOf(
//                    databaseModule,
                    networkModule,
                    repositoryModule,
                    useCaseModule,
                    viewModelModule
                )
            )
        }
    }
}