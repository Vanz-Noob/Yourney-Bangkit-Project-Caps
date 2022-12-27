package com.bangkit.yourney.data.repository

import com.bangkit.yourney.data.NetworkOnlyResource
import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.data.source.remote.RemoteDataSource
import com.bangkit.yourney.data.source.remote.network.ApiResponse
import com.bangkit.yourney.data.source.remote.response.ResponseAuth
import com.bangkit.yourney.data.source.remote.response.ResponseDestination
import com.bangkit.yourney.data.source.remote.response.ResponseDestinationItem
import com.bangkit.yourney.data.source.remote.response.ResponseFavorite
import com.bangkit.yourney.domain.model.Destination
import com.bangkit.yourney.domain.model.Favorite
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.domain.repository.IAuthRepository
import com.bangkit.yourney.domain.repository.IDestinationRepository
import com.bangkit.yourney.utils.DataMapper
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import retrofit2.Response

class DestinationRepository(
    private val remoteDataSource: RemoteDataSource
) : IDestinationRepository {
    override fun allDestination(token: String): Flow<Resource<List<Destination>>> =
        object: NetworkOnlyResource<List<Destination>, List<ResponseDestinationItem?>>() {
            override suspend fun createCall(): Flow<ApiResponse<List<ResponseDestinationItem?>>> = remoteDataSource.allDestination(token)
            override fun transformData(param: List<ResponseDestinationItem?>): Flow<Resource<List<Destination>>> = flow {
                emit(Resource.Success(DataMapper.mapListDestinationResponseToDomain(param), "Get Data Success"))
            }
        }.asFlow()

    override fun filterDestination(
        token: String,
        filter: String
    ): Flow<Resource<List<Destination>>> =
        object: NetworkOnlyResource<List<Destination>, List<ResponseDestinationItem?>>() {
            override suspend fun createCall(): Flow<ApiResponse<List<ResponseDestinationItem?>>> = remoteDataSource.filterDestination(token, filter)
            override fun transformData(param: List<ResponseDestinationItem?>): Flow<Resource<List<Destination>>> = flow {
                emit(Resource.Success(DataMapper.mapListDestinationResponseToDomain(param), "Get Data Success"))
            }
        }.asFlow()

    override fun searchDestination(token: String, search: String): Flow<Resource<List<Destination>>> =
        object: NetworkOnlyResource<List<Destination>, List<ResponseDestinationItem?>>() {
            override suspend fun createCall(): Flow<ApiResponse<List<ResponseDestinationItem?>>> = remoteDataSource.searchDestination(token, search)
            override fun transformData(param: List<ResponseDestinationItem?>): Flow<Resource<List<Destination>>> = flow {
                emit(Resource.Success(DataMapper.mapListDestinationResponseToDomain(param), "Get Data Success"))
            }
        }.asFlow()

    override fun addFavorite(token: String, id: String): Flow<Resource<Favorite>> =
        object: NetworkOnlyResource<Favorite, ResponseFavorite>() {
            override suspend fun createCall(): Flow<ApiResponse<ResponseFavorite>> = remoteDataSource.addFavorite(token, id)
            override fun transformData(param: ResponseFavorite): Flow<Resource<Favorite>> = flow {
                emit(Resource.Success(DataMapper.mapFavoriteResponseToDomain(param), "Get Data Success"))
            }
        }.asFlow()

    override fun removeFavorite(token: String, id: String): Flow<Resource<Favorite>> =
        object: NetworkOnlyResource<Favorite, ResponseFavorite>() {
            override suspend fun createCall(): Flow<ApiResponse<ResponseFavorite>> = remoteDataSource.removeFavorite(token, id)
            override fun transformData(param: ResponseFavorite): Flow<Resource<Favorite>> = flow {
                emit(Resource.Success(DataMapper.mapFavoriteResponseToDomain(param), "Get Data Success"))
            }
        }.asFlow()

    override fun checkFavorite(token: String, id: String): Flow<Resource<Favorite>> =
        object: NetworkOnlyResource<Favorite, ResponseFavorite>() {
            override suspend fun createCall(): Flow<ApiResponse<ResponseFavorite>> = remoteDataSource.checkFavorite(token, id)
            override fun transformData(param: ResponseFavorite): Flow<Resource<Favorite>> = flow {
                emit(Resource.Success(DataMapper.mapFavoriteResponseToDomain(param), "Get Data Success"))
            }
        }.asFlow()
}