package com.bangkit.yourney.data.repository

import com.bangkit.yourney.data.NetworkOnlyResource
import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.data.source.remote.RemoteDataSource
import com.bangkit.yourney.data.source.remote.network.ApiResponse
import com.bangkit.yourney.data.source.remote.response.ResponseAuth
import com.bangkit.yourney.data.source.remote.response.ResponseLogin
import com.bangkit.yourney.data.source.remote.response.ResponseRegister
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.domain.repository.IAuthRepository
import com.bangkit.yourney.utils.DataMapper
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class AuthRepository(
    private val remoteDataSource: RemoteDataSource
) : IAuthRepository {
    override fun loginAccount(username: String, password: String): Flow<Resource<User>> =
        object: NetworkOnlyResource<User, ResponseLogin>() {
            override suspend fun createCall(): Flow<ApiResponse<ResponseLogin>> = remoteDataSource.loginAccount(username, password)
            override fun transformData(param: ResponseLogin): Flow<Resource<User>> = flow {
                emit(Resource.Success(DataMapper.mapLoginResponseToDomain(param, username), "Login Success!"))
            }
        }.asFlow()

    override fun registerAccount(user: User): Flow<Resource<User>> =
        object: NetworkOnlyResource<User, ResponseRegister>() {
            override suspend fun createCall(): Flow<ApiResponse<ResponseRegister>> = remoteDataSource.registerAccount(user.username!!, user.email!!, user.password!!, user.tempatLahir!!, user.jenisKelamin!!)
            override fun transformData(param: ResponseRegister): Flow<Resource<User>> = flow {
                emit(Resource.Success(DataMapper.mapRegisterResponseToDomain(param), "Register Success!"))
            }
        }.asFlow()
}