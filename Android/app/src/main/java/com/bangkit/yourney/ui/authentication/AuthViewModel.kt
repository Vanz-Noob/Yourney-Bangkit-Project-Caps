package com.bangkit.yourney.ui.authentication

import androidx.lifecycle.ViewModel
import androidx.lifecycle.asLiveData
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.domain.usecase.AuthUsecase

class AuthViewModel(private val useCase: AuthUsecase) : ViewModel() {
    fun authLogin(username: String, password: String) = useCase.loginAccount(username, password).asLiveData()
    fun authRegister(user: User) = useCase.registerAccount(user).asLiveData()
}