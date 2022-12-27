package com.bangkit.yourney.data

import com.bangkit.yourney.data.source.remote.network.ApiResponse
import kotlinx.coroutines.flow.*

abstract class NetworkOnlyResource<ResultType, RequestType> {
    private var result: Flow<Resource<ResultType>> = flow {
        emit(Resource.Loading())
        when (val apiResponse = createCall().first()) {
            is ApiResponse.Success -> {
                emitAll(transformData(apiResponse.data).map { it })
            }
            is ApiResponse.Empty -> {
                emit(Resource.Error<ResultType>("ERROR"))
            }
            is ApiResponse.Error -> {
                emit(Resource.Error<ResultType>(apiResponse.errorMessage))
            }
        }
    }
    protected abstract fun transformData(param : RequestType): Flow<Resource<ResultType>>
    protected abstract suspend fun createCall(): Flow<ApiResponse<RequestType>>
    fun asFlow(): Flow<Resource<ResultType>> = result
}