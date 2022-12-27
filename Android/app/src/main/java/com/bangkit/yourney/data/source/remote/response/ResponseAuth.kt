package com.bangkit.yourney.data.source.remote.response

import com.google.gson.annotations.SerializedName
import kotlinx.parcelize.Parcelize
import android.os.Parcelable

@Parcelize
data class ResponseAuth (

    @field:SerializedName("idUser")
    val user_id: Int? = null,
    @field:SerializedName("status")
    val status: String? = null,
    @field:SerializedName("username")
    val username: String? = null,
    @field:SerializedName("access")
    val access: String? = null,
    @field:SerializedName("refresh")
    val refresh: String? = null,
    @field:SerializedName("message")
    val message: String? = null

) : Parcelable
