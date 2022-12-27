package com.bangkit.yourney.data.source.remote.response

import com.google.gson.annotations.SerializedName
import kotlinx.parcelize.Parcelize
import android.os.Parcelable

@Parcelize
data class ResponseFavorite (

    @field:SerializedName("message")
    val message: String? = null,

    @field:SerializedName("liked")
    val liked: Boolean? = false

) : Parcelable
