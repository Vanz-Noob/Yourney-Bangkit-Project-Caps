package com.bangkit.yourney.domain.repository

import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.domain.model.Destination
import com.bangkit.yourney.domain.model.Upload
import com.bangkit.yourney.domain.model.User
import kotlinx.coroutines.flow.Flow
import java.io.File

interface IUserRepository {
    fun getUser(token: String): Flow<Resource<User>>
    fun updateUser(token: String, user: User): Flow<Resource<User>>
    fun getFavorite(token: String): Flow<Resource<List<Destination>>>
    fun uploadFile(token: String, file: File): Flow<Resource<Upload>>
}