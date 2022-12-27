package com.bangkit.yourney.domain.usecase

import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.domain.model.Destination
import com.bangkit.yourney.domain.model.Upload
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.domain.repository.IAuthRepository
import com.bangkit.yourney.domain.repository.IUserRepository
import kotlinx.coroutines.flow.Flow
import java.io.File

class UserInteractor(private val repository: IUserRepository) : UserUsecase {
    override fun getUser(token: String): Flow<Resource<User>> = repository.getUser(token)
    override fun updateUser(token: String, user: User): Flow<Resource<User>> = repository.updateUser(token, user)
    override fun getFavorite(token: String): Flow<Resource<List<Destination>>> = repository.getFavorite(token)
    override fun uploadFile(token: String, file: File): Flow<Resource<Upload>> = repository.uploadFile(token, file)
}