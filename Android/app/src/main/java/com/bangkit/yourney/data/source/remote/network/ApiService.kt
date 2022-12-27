package com.bangkit.yourney.data.source.remote.network

import com.bangkit.yourney.data.source.remote.response.*
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.utils.Constanta.AUTH_LOGIN_PATH
import com.bangkit.yourney.utils.Constanta.AUTH_REG_PATH
import com.bangkit.yourney.utils.Constanta.DESTINATION_PATH
import com.bangkit.yourney.utils.Constanta.DESTINATION_SEARCH_PATH
import com.bangkit.yourney.utils.Constanta.PROFILE_INFO_PATH
import com.bangkit.yourney.utils.Constanta.USER_FAVORITE_DESTINATION
import com.bangkit.yourney.utils.Constanta.USER_UPLOAD_IMAGE_PATH
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.http.*

interface ApiService {
    //    AUTH
    @POST(AUTH_LOGIN_PATH)
    suspend fun authLogin(@Body params: RequestBody): ResponseLogin

    @POST(AUTH_REG_PATH)
    suspend fun authRegister(@Body params: RequestBody): ResponseRegister

    @GET(DESTINATION_PATH)
    suspend fun allDestination(@Header("Authorization") token: String): List<ResponseDestinationItem>

    @GET(DESTINATION_PATH)
    suspend fun destinationFilter(@Header("Authorization") token: String, @Query("category") category: String): List<ResponseDestinationItem>

    @GET(PROFILE_INFO_PATH)
    suspend fun getUser(@Header("Authorization") token: String): ResponseUser

    @PUT(PROFILE_INFO_PATH)
    suspend fun updateUser(@Header("Authorization") token: String, @Body params: RequestBody): UserData

    @GET("${DESTINATION_PATH}/{id}/likes")
    suspend fun checkFavorite(@Header("Authorization") token: String, @Path("id") id:String): ResponseFavorite

    @POST("${DESTINATION_PATH}/{id}/likes")
    suspend fun addFavorite(@Header("Authorization") token: String, @Path("id") id:String): ResponseFavorite

    @POST("${DESTINATION_PATH}/{id}/likes")
    suspend fun removeFavorite(@Header("Authorization") token: String, @Path("id") id:String): ResponseFavorite

    @GET(USER_FAVORITE_DESTINATION)
    suspend fun getFavorite(@Header("Authorization") token: String): List<ResponseDestinationItem>

    @Multipart
    @POST(USER_UPLOAD_IMAGE_PATH)
    suspend fun uploadImage(@Header("Authorization") token: String, @Part image: MultipartBody.Part): ResponseUpload

    @GET(DESTINATION_SEARCH_PATH)
    suspend fun searchDestination(
        @Header("Authorization") token: String,
        @Query("nama_destinasi") search: String
    ): List<ResponseDestinationItem>

}