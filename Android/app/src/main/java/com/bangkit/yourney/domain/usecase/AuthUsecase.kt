package com.bangkit.yourney.domain.usecase

import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.domain.model.User
import kotlinx.coroutines.flow.Flow

interface AuthUsecase {
    fun loginAccount(username: String, password: String): Flow<Resource<User>>
    fun registerAccount(user: User): Flow<Resource<User>>
}