package com.bangkit.yourney.data.repository

import com.bangkit.yourney.data.NetworkOnlyResource
import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.data.source.remote.RemoteDataSource
import com.bangkit.yourney.data.source.remote.network.ApiResponse
import com.bangkit.yourney.data.source.remote.response.*
import com.bangkit.yourney.domain.model.Destination
import com.bangkit.yourney.domain.model.Upload
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.domain.repository.IAuthRepository
import com.bangkit.yourney.domain.repository.IUserRepository
import com.bangkit.yourney.utils.DataMapper
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import java.io.File

class UserRepository(
    private val remoteDataSource: RemoteDataSource
) : IUserRepository {

    override fun getUser(token: String): Flow<Resource<User>> =
        object: NetworkOnlyResource<User, ResponseUser>() {
            override suspend fun createCall(): Flow<ApiResponse<ResponseUser>> = remoteDataSource.getUser(token)
            override fun transformData(param: ResponseUser): Flow<Resource<User>> = flow {
                emit(Resource.Success(DataMapper.mapUserResponseToDomain(param), "Get Data Success!"))
            }
        }.asFlow()

    override fun updateUser(token: String, user: User): Flow<Resource<User>> =
        object: NetworkOnlyResource<User, UserData>() {
            override suspend fun createCall(): Flow<ApiResponse<UserData>> = remoteDataSource.updateUser(token, user.full_name ?: "", user.username_twitter ?: "", user.avatar ?: "", user.jenisKelamin ?: "", user.tempatLahir ?: "")
            override fun transformData(param: UserData): Flow<Resource<User>> = flow {
                emit(Resource.Success(DataMapper.mapUserDataResponseToDomain(param), "Register Success!"))
            }
        }.asFlow()

    override fun getFavorite(token: String): Flow<Resource<List<Destination>>> =
        object: NetworkOnlyResource<List<Destination>, List<ResponseDestinationItem?>>() {
            override suspend fun createCall(): Flow<ApiResponse<List<ResponseDestinationItem?>>> = remoteDataSource.getFavorite(token)
            override fun transformData(param: List<ResponseDestinationItem?>): Flow<Resource<List<Destination>>> = flow {
                emit(Resource.Success(DataMapper.mapListDestinationResponseToDomain(param), "Get Data Success!"))
            }
        }.asFlow()

    override fun uploadFile(token: String, file: File): Flow<Resource<Upload>> =
        object: NetworkOnlyResource<Upload, ResponseUpload>() {
            override suspend fun createCall(): Flow<ApiResponse<ResponseUpload>> = remoteDataSource.uploadFile(token, file)
            override fun transformData(param: ResponseUpload): Flow<Resource<Upload>> = flow {
                emit(Resource.Success(DataMapper.mapUploadeResponseToDomain(param), "Upload Success!"))
            }
        }.asFlow()
}