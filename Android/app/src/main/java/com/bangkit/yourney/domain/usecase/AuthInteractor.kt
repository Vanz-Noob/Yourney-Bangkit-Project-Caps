package com.bangkit.yourney.domain.usecase

import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.domain.repository.IAuthRepository
import kotlinx.coroutines.flow.Flow

class AuthInteractor(private val repository: IAuthRepository) : AuthUsecase {
    override fun loginAccount(username: String, password: String) = repository.loginAccount(username, password)
    override fun registerAccount(user: User): Flow<Resource<User>> = repository.registerAccount(user)
}