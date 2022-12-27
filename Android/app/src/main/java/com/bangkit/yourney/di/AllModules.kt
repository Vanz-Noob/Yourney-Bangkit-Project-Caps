package com.bangkit.yourney.di

import com.bangkit.yourney.data.repository.AuthRepository
import com.bangkit.yourney.data.repository.DestinationRepository
import com.bangkit.yourney.data.repository.UserRepository
import com.bangkit.yourney.data.source.remote.RemoteDataSource
import com.bangkit.yourney.data.source.remote.network.ApiService
import com.bangkit.yourney.domain.repository.IAuthRepository
import com.bangkit.yourney.domain.repository.IDestinationRepository
import com.bangkit.yourney.domain.repository.IUserRepository
import com.bangkit.yourney.domain.usecase.*
import com.bangkit.yourney.ui.authentication.AuthViewModel
import com.bangkit.yourney.ui.main.MainViewModel
import com.bangkit.yourney.ui.user.UserViewModel
import com.bangkit.yourney.utils.Constanta
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import org.koin.androidx.viewmodel.dsl.viewModel
import org.koin.dsl.module
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object AllModules {

    val networkModule = module {
        single {
            OkHttpClient.Builder()
                .addInterceptor(HttpLoggingInterceptor().setLevel(HttpLoggingInterceptor.Level.BODY))
                .connectTimeout(120, TimeUnit.SECONDS)
                .readTimeout(120, TimeUnit.SECONDS)
                .build()
        }
        single {
            val retrofit = Retrofit.Builder()
                .baseUrl(Constanta.BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .client(get())
                .build()
            retrofit.create(ApiService::class.java)
        }
    }

    val repositoryModule = module {
        single { RemoteDataSource(get()) }
        single<IAuthRepository> {
            AuthRepository(
                get()
            )
        }
        single<IDestinationRepository> {
            DestinationRepository(
                get()
            )
        }
        single<IUserRepository> {
            UserRepository(
                get()
            )
        }
    }

    val useCaseModule = module {
        factory<AuthUsecase> { AuthInteractor(get()) }
        factory<DestinationUsecase> { DestinationInteractor(get()) }
        factory<UserUsecase> { UserInteractor(get()) }
    }

    val viewModelModule = module {
        viewModel { AuthViewModel(get()) }
        viewModel { MainViewModel(get()) }
        viewModel { UserViewModel(get()) }
    }
}