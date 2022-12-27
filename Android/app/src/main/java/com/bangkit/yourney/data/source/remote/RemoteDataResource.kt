package com.bangkit.yourney.data.source.remote

import android.util.Log
import com.bangkit.yourney.data.source.remote.network.ApiResponse
import com.bangkit.yourney.data.source.remote.network.ApiService
import com.bangkit.yourney.data.source.remote.response.*
import com.google.gson.Gson
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.ResponseBody
import org.json.JSONObject
import retrofit2.HttpException
import java.io.File
import java.io.IOException

class RemoteDataSource(private val apiService: ApiService) {
    //    AUTH
    suspend fun loginAccount(username: String, password: String): Flow<ApiResponse<ResponseLogin>> =
        flow {
            try {
                val response = apiService.authLogin(createJsonRequestBody(
                    "username" to username, "password" to password))
                if (response.status == "success") {
                    emit(ApiResponse.Success(response))
                } else {
                    emit(ApiResponse.Error(response.message ?: "Kesalahan pada server!"))
                }
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    suspend fun registerAccount(username: String, email: String, password: String, pob: String, gender: String): Flow<ApiResponse<ResponseRegister>> =
        flow {
            try {
                val response = apiService.authRegister(createJsonRequestBody(
                    "username" to username, "email" to email, "jenis_kelamin" to gender, "tempat_lahir" to pob, "password" to password))
                if (response.code == "sukses") {
                    emit(ApiResponse.Success(response))
                } else {
                    emit(ApiResponse.Error(response.message.toString()))
                }
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    suspend fun allDestination(token: String): Flow<ApiResponse<List<ResponseDestinationItem?>>> =
        flow {
            try {
                val response = apiService.allDestination(token)
                emit(ApiResponse.Success(response))
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    suspend fun filterDestination(token: String, filter: String): Flow<ApiResponse<List<ResponseDestinationItem?>>> =
        flow {
            try {
                val response = apiService.destinationFilter(token, filter)
                emit(ApiResponse.Success(response))
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    suspend fun searchDestination(token: String,search: String): Flow<ApiResponse<List<ResponseDestinationItem?>>> =
        flow {
            try {
                val response = apiService.searchDestination(token, search)
                if (response.isNotEmpty()) {
                    emit(ApiResponse.Success(response))
                } else {
                    emit(ApiResponse.Error("Data kosong!"))
                }
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    suspend fun getUser(token: String): Flow<ApiResponse<ResponseUser>> =
        flow {
            try {
                val response = apiService.getUser(token)
                if (response.status == "success") {
                    emit(ApiResponse.Success(response))
                } else {
                    emit(ApiResponse.Error("Data not found!"))
                }
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    suspend fun updateUser(token: String, username: String, user_tweet: String, user_pic: String, jenis_kelamin: String, tempat_lahir: String): Flow<ApiResponse<UserData>> =
        flow {
            try {
                val response = apiService.updateUser(token, createJsonRequestBody(
                    "full_name" to username, "username_twitter" to user_tweet, "user_pic" to user_pic, "jenis_kelamin" to jenis_kelamin, "tempat_lahir" to tempat_lahir))

                if (response.username != null) {
                    emit(ApiResponse.Success(response))
                } else {
                    emit(ApiResponse.Error("Data not found!"))
                }
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    suspend fun addFavorite(token: String, id: String): Flow<ApiResponse<ResponseFavorite>> =
        flow {
            try {
                val response = apiService.addFavorite(token, id)
                emit(ApiResponse.Success(response))
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    suspend fun removeFavorite(token: String, id:String): Flow<ApiResponse<ResponseFavorite>> =
        flow {
            try {
                val response = apiService.removeFavorite(token, id)
                emit(ApiResponse.Success(response))
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    suspend fun checkFavorite(token: String, id:String): Flow<ApiResponse<ResponseFavorite>> =
        flow {
            try {
                val response = apiService.checkFavorite(token, id)
                if (response.liked == true) {
                    emit(ApiResponse.Success(response))
                } else {
                    emit(ApiResponse.Error(response.message ?: "Data not found!"))
                }
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    suspend fun getFavorite(token: String): Flow<ApiResponse<List<ResponseDestinationItem?>>> =
        flow {
            try {
                val response = apiService.getFavorite(token)
                emit(ApiResponse.Success(response))
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    suspend fun uploadFile(
        token: String,file: File
    ): Flow<ApiResponse<ResponseUpload>> =
        flow {
            try {
                val fileBody: MultipartBody.Part = MultipartBody.Part.createFormData(
                    "image",
                    file.name.toString(),
                    file.asRequestBody("images/*".toMediaType())
                )
                val response = apiService.uploadImage(token, fileBody)

                if (response.status == "success") {
                    emit(ApiResponse.Success(response))
                } else {
                    emit(ApiResponse.Error(response.message.toString()))
                }
            } catch (e: HttpException) {
                emit(ApiResponse.Error(e.response()?.errorBody()?.string().toString()))
            }
        }.flowOn(Dispatchers.IO)

    private fun createJsonRequestBody(vararg params: Pair<String, String>) =
        RequestBody.create(
            "application/json; charset=utf-8".toMediaTypeOrNull(),
            JSONObject(mapOf(*params)).toString())

}